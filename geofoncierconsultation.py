# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoFoncierConsultationDetails
                                 A QGIS plugin
 Plugin  de diffusion des dossiers aux clients GéoFoncier
                              -------------------
        begin                : 2013-11-12
        copyright            : (C) 2013 by Etienne Trimaille
        email                : etienne@trimaille.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
#from PyQt4.QtCore import *
from PyQt4.QtCore import SIGNAL, Qt, QSettings, QTranslator, qVersion, QCoreApplication, QObject, QVariant, QFileInfo, QUrl
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from geofoncierconsultationdialog import GeoFoncierConsultationDialog
from connexion_client_GF import ConnexionClientGF
from dossier import Dossier
from exception import *
import unicodedata
import os.path
#from fileinput import close, filename


class GeoFoncierConsultationDetails:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.resources_dir = os.path.join(self.plugin_dir, "resources")
        
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'geofoncierconsultation_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GeoFoncierConsultationDialog()
        self.window = self.iface.mainWindow()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/resources/icon_png"),
            u"GéoFoncier", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Mes dossiers GéoFoncier", self.action)
        
        #Dictionnaire des couches
        self.layers = {}

        #Ajout du connecteur bouton d'aide
        QObject.connect(self.dlg.ui.pushButton_help, SIGNAL("clicked()"), self.aboutWindow)
        QObject.connect(self.dlg.ui.pushButton_listerDossiers, SIGNAL("clicked()"), self.listerDossiers)
        QObject.connect(self.dlg.ui.pushButton_enregistrer_dossiers, SIGNAL("clicked()"), self.enregistrerDossiers)
        QObject.connect(self.dlg.ui.pushButton_telecharger_kml, SIGNAL("clicked()"), self.telechargerKML)
        QObject.connect(self.dlg.ui.pushButton_ZIP, SIGNAL("clicked()"), self.enregistrerZIP)
        QObject.connect(self.dlg.ui.pushButton_couche_osm, SIGNAL("clicked()"), self.ajouterCoucheOSM)
        QObject.connect(self.dlg.ui.pushButton_couche_gsat, SIGNAL("clicked()"), self.ajouterCoucheGSAT)
        QObject.connect(self.dlg.ui.pushButton_site_geofoncier, SIGNAL("clicked()"), self.siteGeoFoncier)
        
        QObject.connect(self.dlg.ui.lineEdit_login, SIGNAL("textChanged(QString)"), self.checkLineEdits)
        QObject.connect(self.dlg.ui.lineEdit_password, SIGNAL("textChanged(QString)"), self.checkLineEdits)

        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerRemoved(QString)"), self.layerDeleted)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Mes dossiers GéoFoncier", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        if self.iface:
            self.iface.removeDockWidget(self.dlg)
        
          
    def aboutWindow(self):
        msg = self.dlg.tr(u"Plugin QGIS pour la consultation des dossiers GéoFoncier<br /><br />Auteur: Etienne Trimaille<br />Mail: <a href=\"mailto:etienne@trimaille.eu\">etienne@trimaille.eu</a>\n<br /><strong>Ce plugin est expérimental !</strong><br /><br />Source cartographique : les contributeurs d'<a href='http://www.openstreetmap.org'>OpenStreetMap</a><br/>Fonctionne avec l'API GéoFoncier version 1.2c<br />Licence : A DEFINIR")
        infoString = QCoreApplication.translate('GéoFoncier', msg)
        QMessageBox.information(self.dlg,u"GéoFoncier", infoString)
        
    def errorWindow(self,message):
        QMessageBox.critical(self.dlg, u"GéoFoncier", message)
        
    def informationWindow(self,message):
        QMessageBox.information(self.dlg, u"GéoFoncier", message)

    def checkLineEdits(self):
        if self.dlg.ui.lineEdit_login.text() != "" and self.dlg.ui.lineEdit_password.text() != "":
            self.dlg.ui.pushButton_listerDossiers.setEnabled(True)
        else:
            self.dlg.ui.pushButton_listerDossiers.setEnabled(False)
            
    def listerDossiers(self):
        self.dlg.setCursor(Qt.WaitCursor)
        msgBox = QProgressDialog("Chargement","Annuler",0,0)
        msgBox.setValue(-1)
        msgBox.setWindowTitle("Chargement des dossiers")
        msgBox.setAutoReset(True)
        msgBox.setAutoClose(False)
        msgBox.open()
        QApplication.processEvents()
        
        self.dlg.ui.label_login.setDisabled(True)
        self.dlg.ui.label_password.setDisabled(True)
        self.dlg.ui.label_zone.setDisabled(True)
        self.dlg.ui.lineEdit_login.setDisabled(True)
        self.dlg.ui.lineEdit_password.setDisabled(True)
        self.dlg.ui.comboBox_zone.setDisabled(True)
        self.dlg.ui.pushButton_listerDossiers.setDisabled(True)
        QApplication.processEvents()
        
        login = self.dlg.ui.lineEdit_login.text()
        password = self.dlg.ui.lineEdit_password.text()
        zone = str(self.dlg.ui.comboBox_zone.currentText())
        
        self.saveZone(zone)
        
        self.connexionAPI = ConnexionClientGF(login, password, zone)
        listeDossierCSV = ''
        try:
            listeDossierCSV = self.connexionAPI.getListeDossiers()
        except LoginException:
            self.errorWindow(self.dlg.tr(u"Mauvais nom d'utilisateur ou mot de passe"))
            del self.connexionAPI
            self.run()
        except NoResult:
            self.errorWindow(self.dlg.tr(u"Aucun dossier pour ce territoire"))
            del self.connexionAPI
            self.run()
        except IOError:
            self.errorWindow(self.dlg.tr(u"Erreur de connexion réseau à GéoFoncier"))
            del self.connexionAPI
            self.run()
        else:
            Dossier.loadFromCSV(listeDossierCSV)
            
            nombreDossiers = Dossier.getNbrDossiers()
            if nombreDossiers == 1 :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.tr(u" dossier trouvé"))
            else :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.tr(u" dossiers trouvés"))
                
            #Remplissage de la tableView
            self.dlg.ui.tableWidget_dossiers.setColumnCount(6)
            self.dlg.ui.tableWidget_dossiers.setHorizontalHeaderLabels(['Structure', 'Ref', 'Commune', 'Code INSEE', 'Date','Zip'])
            self.dlg.ui.tableWidget_dossiers.setRowCount(nombreDossiers)
            
            self.buttonGroupArchive = QButtonGroup()
            self.buttonGroupArchive.buttonClicked[int].connect(self.getArchive)
            
            for row,dossier in enumerate(Dossier.getListeDossiers()):
                element = dossier.getInformations()
                self.dlg.ui.tableWidget_dossiers.setItem(row, 0, QTableWidgetItem(self.dlg.trUtf8(element["structure"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 1, QTableWidgetItem(self.dlg.trUtf8(element["reference"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 2, QTableWidgetItem(self.dlg.trUtf8(element["nom_commune"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 3, QTableWidgetItem(self.dlg.trUtf8(element["insee_commune"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 4, QTableWidgetItem(self.dlg.trUtf8(element["date"])))
                
                button = QPushButton("Archive")
                self.buttonGroupArchive.addButton(button, row)
                self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 5, button)
            
            self.dlg.ui.tableWidget_dossiers.cellClicked.connect(self.getDetails)
            self.dlg.ui.tableWidget_dossiers.resizeColumnsToContents();
            self.dlg.ui.tableWidget_dossiers.resizeRowsToContents();
            self.dlg.ui.tableWidget_dossiers.show()
            self.dlg.ui.label_listeDossiers.show()
            self.dlg.ui.comboBox_format.show()
            self.dlg.ui.pushButton_enregistrer_dossiers.show()
            self.dlg.ui.pushButton_couche_osm.show()
            
            msgBox.close()
            self.dlg.ui.tabWidget.setTabEnabled(1, True);
            self.dlg.ui.tabWidget.setCurrentIndex(1)
            self.dlg.setCursor(Qt.ArrowCursor)
            
    def layerDeleted(self,idLayer):
        for i in self.layers:
            if idLayer == i:
                if self.layers[i] == "osm":
                    self.dlg.ui.pushButton_couche_osm.setEnabled(True)
                elif self.layers[i] == "googlesat":
                    self.dlg.ui.pushButton_couche_gsat.setEnabled(True)

    def addPointLayerDossier(self):
        self.PointLayerDossier = QgsVectorLayer("Point",self.dlg.tr(u"Dossier GéoFoncier"), "memory")
        table_attributairePoint = [ QgsField("ref",QVariant.String),QgsField("structure",QVariant.String),QgsField("Commune", QVariant.String), QgsField("INSEE", QVariant.String), QgsField("Date", QVariant.String), QgsField("Localisants", QVariant.String), QgsField("ZIP", QVariant.String) ]
        self.dataProviderPointDossier = self.PointLayerDossier.dataProvider()
        self.dataProviderPointDossier.addAttributes(table_attributairePoint)
        self.PointLayerDossier.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId))
        self.PointLayerDossier.loadSldStyle(":/resources/point")
        QgsMapLayerRegistry.instance().addMapLayer(self.PointLayerDossier)
        QObject.connect(self.PointLayerDossier, SIGNAL("layerDeleted()"), self.PointLayerDossierDeleted)
    
    def PointLayerDossierDeleted(self):
        del self.PointLayerDossier
        
    def addPolygonLayerDossier(self):
        self.PolygonLayerDossier = QgsVectorLayer("Polygon",self.dlg.tr(u"Dossier GéoFoncier"), "memory")
        table_attributairePolygons = [ QgsField("ref",QVariant.String),QgsField("structure",QVariant.String),QgsField("Commune", QVariant.String), QgsField("INSEE", QVariant.String), QgsField("Date", QVariant.String), QgsField("ZIP", QVariant.String) ]
        self.dataProviderPolygonDossier = self.PolygonLayerDossier.dataProvider()
        self.dataProviderPolygonDossier.addAttributes(table_attributairePolygons)
        self.PolygonLayerDossier.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId))
        self.PolygonLayerDossier.loadSldStyle(":/resources/polygons")
        QgsMapLayerRegistry.instance().addMapLayer(self.PolygonLayerDossier)
        QObject.connect(self.PolygonLayerDossier, SIGNAL("layerDeleted()"), self.PolygonLayerDossierDeleted)
        
    def PolygonLayerDossierDeleted(self):
        del self.PolygonLayerDossier

    def enregistrerZIP(self):
        fichier = "dossier_"+self.dossier.getReference()+".zip"
        fichier = fichier.decode('utf-8')
        fichier = unicodedata.normalize('NFKD', fichier).encode('ASCII', 'ignore')
        fichier = "-".join(fichier.split())
        self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.dossier.getURLArchiveZIP(),fichier)
        
    def getArchive(self,row):
        self.dossier = Dossier.getDossier(row)
        fichier = "dossier_"+self.dossier.getReference()+".zip"
        fichier = fichier.decode('utf-8')
        fichier = unicodedata.normalize('NFKD', fichier).encode('ASCII', 'ignore')
        fichier = "-".join(fichier.split())
        self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.dossier.getURLArchiveZIP(),fichier)

    def enregistrerDossiers(self):
        formatOutput = self.dlg.ui.comboBox_format.currentText()
        if formatOutput in ('csv', 'kml', 'xml'):
            filename = "mes_dossiers."+formatOutput
            self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.connexionAPI.getURLListeDossiers(formatOutput),filename)
        
    def getDetails(self):
        self.dlg.ui.listWidget_details.clear()
        row = self.dlg.ui.tableWidget_dossiers.currentItem().row()
        self.dossier = Dossier.getDossier(row)
        
        if self.dossier.getGeometries() == None:
            self.dlg.setCursor(Qt.WaitCursor)
            msgBox = QProgressDialog("Chargement","Annuler",0,0)
            msgBox.setValue(-1)
            msgBox.setWindowTitle("Chargement du dossier")
            msgBox.setAutoReset(True)
            msgBox.setAutoClose(False)
            msgBox.open()
            QApplication.processEvents()
    
            self.dossier.loadDetails(self.connexionAPI.get(self.dossier.getURLDossier()))
            
            self.voirCoucheQGIS()
            
            msgBox.close()
        
        tab = self.dossier.getInformations()
        self.dlg.ui.label_reference.setText(self.dlg.trUtf8(tab["reference"]))
        self.dlg.ui.label_structure.setText(self.dlg.trUtf8(tab["structure"]))
        self.dlg.ui.label_commune.setText(self.dlg.trUtf8(tab["nom_commune"]))
        self.dlg.ui.label_date.setText(self.dlg.trUtf8(tab["date"]))
        self.dlg.ui.label_insee.setText(self.dlg.trUtf8(tab["insee_commune"]))
        QApplication.processEvents()
        for i,doc in enumerate(self.dossier.getDocuments()):
            item = QListWidgetItem()
            description = doc.getDescription()
            item.setText(self.dlg.trUtf8(description));
            self.dlg.ui.listWidget_details.addItem(item);
        
        try:    
            self.dlg.ui.listWidget_details.clicked.disconnect(self.getExternalDocument)
        except TypeError:
            pass
        
        self.dlg.ui.listWidget_details.clicked.connect(self.getExternalDocument)
        self.dlg.ui.tabWidget.setTabEnabled(2, True);
        self.dlg.ui.tabWidget.setCurrentIndex(2)
        
        #Zoom sur les géometries
        envelope = self.dossier.getEnvelope()
        self.canvas.setExtent(QgsRectangle(envelope[0],envelope[2],envelope[1],envelope[3]))
        self.canvas.refresh()
        
        self.dlg.setCursor(Qt.ArrowCursor)
        
    def voirCoucheQGIS(self):
        tab = self.dossier.getInformations()
        geometries = self.dossier.getGeometries()
        
        for geom in geometries:
            fet = QgsFeature()
            qgisGeom = QgsGeometry.fromWkt(geom)
            fet.setGeometry(qgisGeom)
            
            qgisGeomType = qgisGeom.wkbType()
            
            if qgisGeomType == QGis.WKBPoint:
                
                #Verification de l'existence de la couche
                try:
                    self.PointLayerDossier
                except AttributeError:
                    self.addPointLayerDossier()
                
                fet.setAttributes( [self.dlg.trUtf8(tab["reference"]),self.dlg.trUtf8(tab["structure"]),self.dlg.trUtf8(tab["nom_commune"]),self.dlg.trUtf8(tab["insee_commune"]),self.dlg.trUtf8(tab["date"]),"1", self.connexionAPI.getURL(self.dossier.getURLArchiveZIP())])
                self.PointLayerDossier.startEditing()
                self.dataProviderPointDossier.addFeatures( [ fet ] )
                self.PointLayerDossier.commitChanges()
            
            elif qgisGeomType == QGis.WKBMultiPoint:
                
                #Verification de l'existence de la couche
                try:
                    self.PointLayerDossier
                except AttributeError:
                    self.addPointLayerDossier()
                
                fet.setAttributes( [self.dlg.trUtf8(tab["reference"]),self.dlg.trUtf8(tab["structure"]),self.dlg.trUtf8(tab["nom_commune"]),self.dlg.trUtf8(tab["insee_commune"]),self.dlg.trUtf8(tab["date"]),str(len(qgisGeom.asMultiPoint())), self.connexionAPI.getURL(self.dossier.getURLArchiveZIP())])
                self.PointLayerDossier.startEditing()
                self.dataProviderPointDossier.addFeatures( [ fet ] )
                self.PointLayerDossier.commitChanges()
            
            elif qgisGeomType == QGis.WKBPolygon or qgisGeomType == QGis.WKBMultiPolygon:
                
                #Verification de l'existence de la couche
                try:
                    self.PolygonLayerDossier
                except AttributeError:
                    self.addPolygonLayerDossier()
                
                fet.setAttributes( [self.dlg.trUtf8(tab["reference"]),self.dlg.trUtf8(tab["structure"]),self.dlg.trUtf8(tab["nom_commune"]),self.dlg.trUtf8(tab["insee_commune"]),self.dlg.trUtf8(tab["date"]), self.connexionAPI.getURL(self.dossier.getURLArchiveZIP())])
                self.PolygonLayerDossier.startEditing()
                self.dataProviderPolygonDossier.addFeatures( [ fet ] )
                self.PolygonLayerDossier.commitChanges()
        
    def telechargerKML(self):
        self.informationWindow(self.dlg.tr(u"Bientôt disponible, en cours de dev"))

    def getExternalDocument(self):
        row = self.dlg.ui.listWidget_details.currentRow()
        doc = self.dossier.getDocument(row)
        self.connexionAPI.getAndSaveExternalDocument(self.dlg,doc.getURL(),doc.getFileName())
        
    def ajouterCoucheOSM(self):
        self.enableUseOfGlobalCrs()
        fileInfo = QFileInfo(os.path.join(self.resources_dir,"osmfr.xml"))
        self.osmLayer = QgsRasterLayer(fileInfo.filePath(), "OpenStreetMap")
        
        if not self.osmLayer.isValid():
            print "Layer failed to load!"
        self.osmLayer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.PostgisCrsId))
        
        QgsMapLayerRegistry.instance().addMapLayer(self.osmLayer)
        self.layers[self.osmLayer.id()] = "osm"
        self.dlg.ui.pushButton_couche_osm.setEnabled(False)
        self.disableUseOfGlobalCrs()
        
    def ajouterCoucheGSAT(self):
        self.enableUseOfGlobalCrs()
        fileInfo = QFileInfo(os.path.join(self.resources_dir,"googlesat.xml"))
        self.googleLayer = QgsRasterLayer(fileInfo.filePath(), u"Photo aérienne Google")
        
        if not self.googleLayer.isValid():
            print "Layer failed to load!"
        self.googleLayer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.PostgisCrsId))
        
        QgsMapLayerRegistry.instance().addMapLayer(self.googleLayer)
        self.layers[self.googleLayer.id()] = "googlesat"
        self.dlg.ui.pushButton_couche_gsat.setEnabled(False)
        self.disableUseOfGlobalCrs()

    def degriseBoutonOSM(self):
        print "signal !"
        
     #set new Layers to use the Project-CRS'  
    def enableUseOfGlobalCrs(self):  
        self.s = QSettings()  
        self.oldValidation = self.s.value("/Projections/defaultBehaviour")
        self.s.setValue( "/Projections/defaultBehaviour", "useProject" )  
    
    #enable old settings again' 
    def disableUseOfGlobalCrs(self):  
        self.s.setValue( "/Projections/defaultBehaviour", self.oldValidation ) 
                
    def run(self):

        try:
            self.connexionAPI
        except AttributeError:
            #Initialisation
            self.window.addDockWidget(Qt.BottomDockWidgetArea, self.dlg)
            self.dlg.setCursor(Qt.ArrowCursor)
            
            #Load zone
            try:
                with open(os.path.join(self.plugin_dir,"zone.txt"), "r") as fichier :
                    ancienneZone = fichier.read()
                    fichier.close()
                    if ancienneZone != "":
                        index = self.dlg.ui.comboBox_zone.findText(ancienneZone)
                        if index in ("metropole", "antilles", "guyane", "reunion", "mayotte"):
                            self.dlg.ui.comboBox_zone.setCurrentIndex(index)
            except IOError:
                pass
            
            self.dlg.ui.tabWidget.setTabEnabled(1, False);
            self.dlg.ui.tabWidget.setTabEnabled(2, False);
            self.dlg.ui.label_login.setDisabled(False)
            self.dlg.ui.label_password.setDisabled(False)
            self.dlg.ui.label_zone.setDisabled(False)
            self.dlg.ui.lineEdit_login.setDisabled(False)
            self.dlg.ui.lineEdit_password.setDisabled(False)
            self.dlg.ui.comboBox_zone.setDisabled(False)
            self.dlg.ui.pushButton_listerDossiers.setDisabled(False)
            self.dlg.ui.label_listeDossiers.hide()
            self.dlg.ui.tableWidget_dossiers.hide()
            self.dlg.ui.tableWidget_dossiers.clearContents()
            self.dlg.ui.comboBox_format.hide()
            self.dlg.ui.pushButton_enregistrer_dossiers.hide()
            self.dlg.ui.pushButton_couche_osm.hide()
            self.dlg.ui.pushButton_telecharger_kml.hide()
            Dossier.truncateDossier()
            self.dlg.show()
            
        else:
            self.dlg.show()

    def saveZone(self, zone):
        with open(os.path.join(self.plugin_dir,"zone.txt"), "w") as fichier :
            fichier.write(zone)
            fichier.close()
            
    def siteGeoFoncier(self):
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl("http://www.geofoncier.fr"))