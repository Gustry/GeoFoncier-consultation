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
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
#from PyQt4.QtCore import *
from PyQt4.QtCore import SIGNAL, Qt, QSettings, QTranslator, qVersion, QCoreApplication, QObject, QVariant, QFileInfo, QUrl
from PyQt4.QtGui import QAction, QIcon, QMessageBox, QDesktopServices, QApplication, QProgressDialog, QPushButton, QTableWidgetItem, QButtonGroup, QListWidgetItem
from qgis.core import QgsGeometry, QgsMapLayerRegistry, QgsRectangle, QgsFeature, QGis, QgsVectorLayer, QgsRasterLayer, QgsField, QgsCoordinateReferenceSystem
from qgis.gui import QgsMessageBar

# Import the code for the dialog
from geofoncierconsultationdialog import GeoFoncierConsultationDialog
from connexion_client_GF import ConnexionClientGF
from dossier import Dossier
from exception import LoginException, NoResultException
import unicodedata
import os.path


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
        
        #Duration QgsMessageDialog
        self.duration = 5

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
        QObject.connect(self.dlg.ui.pushButton_rechargerDossiers, SIGNAL("clicked()"), self.rechargerDossiers)
        QObject.connect(self.dlg.ui.pushButton_ZIP, SIGNAL("clicked()"), self.enregistrerZIP)
        QObject.connect(self.dlg.ui.pushButton_rechargerDossier, SIGNAL("clicked()"), self.rechargerDossier)
        QObject.connect(self.dlg.ui.pushButton_couche_osm, SIGNAL("clicked()"), self.ajouterCoucheOSM)
        QObject.connect(self.dlg.ui.pushButton_couche_gsat, SIGNAL("clicked()"), self.ajouterCoucheGSAT)
        QObject.connect(self.dlg.ui.pushButton_site_geofoncier, SIGNAL("clicked()"), self.siteGeoFoncier)
        
        QObject.connect(self.dlg.ui.checkBox_memoriser, SIGNAL("clicked()"), self.memoriserLoginInformation)
        
        QObject.connect(self.dlg.ui.lineEdit_login, SIGNAL("textChanged(QString)"), self.checkLineEdits)
        QObject.connect(self.dlg.ui.lineEdit_password, SIGNAL("textChanged(QString)"), self.checkLineEdits)

        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerRemoved(QString)"), self.layerDeleted)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Mes dossiers GéoFoncier", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        if self.iface:
            self.iface.removeDockWidget(self.dlg)
                
    def run(self):
        """Initialisation du plugin"""
        try:
            self.connexionAPI
        except AttributeError:
            #Si la connexion API n'existe pas
            self.window.addDockWidget(Qt.TopDockWidgetArea, self.dlg)
            self.dlg.setCursor(Qt.ArrowCursor)
            
            #Lecture des logins
            self.s = QSettings()
            if self.s.value("/GeoFoncierConsultation/saveLogin") == "true":
                self.dlg.ui.pushButton_listerDossiers.setEnabled(True)
                self.dlg.ui.lineEdit_login.setText(self.s.value("/GeoFoncierConsultation/login"))
                self.dlg.ui.lineEdit_password.setText(self.s.value("/GeoFoncierConsultation/password"))
                
                index = self.dlg.ui.comboBox_zone.findText(self.s.value("/GeoFoncierConsultation/territoire"))
                if index in ("metropole", "antilles", "guyane", "reunion", "mayotte"):
                    self.dlg.ui.comboBox_zone.setCurrentIndex(index)

                self.dlg.ui.checkBox_memoriser.setChecked(True)
                self.saveLogin = True
            else:
                self.dlg.ui.pushButton_listerDossiers.setEnabled(False)
                self.dlg.ui.lineEdit_login.setText("")
                self.dlg.ui.lineEdit_password.setText("")
                self.dlg.ui.checkBox_memoriser.setChecked(False)
                self.saveLogin = False
            
            self.dlg.ui.tabWidget.setTabEnabled(1, False);
            self.dlg.ui.tabWidget.setTabEnabled(2, False);
            self.dlg.ui.label_login.setDisabled(False)
            self.dlg.ui.label_password.setDisabled(False)
            self.dlg.ui.label_zone.setDisabled(False)
            self.dlg.ui.lineEdit_login.setDisabled(False)
            self.dlg.ui.lineEdit_password.setDisabled(False)
            self.dlg.ui.comboBox_zone.setDisabled(False)
            self.dlg.ui.checkBox_memoriser.setDisabled(False)
            self.dlg.ui.label_memoriser.setDisabled(False)
            self.dlg.ui.label_listeDossiers.hide()
            self.dlg.ui.tableWidget_dossiers.hide()
            self.dlg.ui.tableWidget_dossiers.clearContents()
            self.dlg.ui.comboBox_format.hide()
            self.dlg.ui.pushButton_enregistrer_dossiers.hide()
            self.dlg.ui.pushButton_couche_osm.hide()
            Dossier.truncateDossier()
            
        self.dlg.show()
        
    """ Fenêtre d'aide """      
    def aboutWindow(self):
        msg = self.dlg.tr(u"Plugin QGIS pour la consultation des dossiers GéoFoncier<br /><br />Mail: <a href=\"mailto:admin@geofoncier.fr\">admin@geofoncier.fr</a><br />Auteur: Etienne Trimaille\n<br /><strong>Ce plugin est expérimental !</strong><br /><br />Source cartographique : les contributeurs d'<a href='http://www.openstreetmap.org'>OpenStreetMap</a><br/>Fonctionne avec l'API GéoFoncier version 1.2c<br />Licence : <a href='http://www.gnu.org/licenses/quick-guide-gplv3.fr.html'>GNU GPL v3</a>")
        infoString = QCoreApplication.translate('GéoFoncier', msg)
        QMessageBox.information(self.dlg,u"GéoFoncier", infoString)

 
    """ ONGLET CONNEXION """
    def memoriserLoginInformation(self):
        if self.dlg.ui.checkBox_memoriser.isChecked():
            res = QMessageBox.question(self.dlg, u"Sauvegarder les identifiants", u"<b>ATTENTION : </b> Vous avez choisi de sauvegarder votre mot de passe. Il sera stocké en clair dans le fichier de votre projet et dans votre dossier utilisateur. Voulez-vous réellement sauvegarder vos identifiants ?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.saveLogin = True
            else:
                self.saveLogin = False
                self.dlg.ui.checkBox_memoriser.setChecked(False)
        else:
            self.saveLogin = False
            self.dlg.ui.checkBox_memoriser.setChecked(False)

    def checkLineEdits(self):
        """Grise le bouton de connexion si les champs sont vides"""
        if self.dlg.ui.lineEdit_login.text() != "" and self.dlg.ui.lineEdit_password.text() != "":
            self.dlg.ui.pushButton_listerDossiers.setEnabled(True)
        else:
            self.dlg.ui.pushButton_listerDossiers.setEnabled(False)

    def siteGeoFoncier(self):
        """Bouton d'accès au site GéoFoncier"""
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl("http://www.geofoncier.fr"))




    """ ONGLET Dossiers """            
    def listerDossiers(self):
        """Gere l'affichage de l'onglet Dossiers"""
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
        self.dlg.ui.checkBox_memoriser.setDisabled(True)
        self.dlg.ui.label_memoriser.setDisabled(True)
        self.dlg.ui.pushButton_listerDossiers.setDisabled(True)
        QApplication.processEvents()
        
        login = self.dlg.ui.lineEdit_login.text()
        password = self.dlg.ui.lineEdit_password.text()
        zone = str(self.dlg.ui.comboBox_zone.currentText())
        
        self.connexionAPI = ConnexionClientGF(login, password, zone)
        listeDossierCSV = ''
        try:
            listeDossierCSV = self.connexionAPI.getListeDossiers()
        except LoginException:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Mauvais nom d'utilisateur ou mot de passe"), level=QgsMessageBar.CRITICAL, duration=self.duration)
            del self.connexionAPI
            self.run()
        except NoResultException:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Aucun dossier pour ce territoire"), level=QgsMessageBar.CRITICAL, duration=self.duration)
            del self.connexionAPI
            self.run()
        except IOError:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Erreur de connexion réseau à GéoFoncier"), level=QgsMessageBar.CRITICAL, duration=self.duration)
            del self.connexionAPI
            self.run()
        else:
            
            #La connexion est OK, alors on enregistre les parametres de connexion
            self.s = QSettings()
            if self.saveLogin == True:
                self.s.setValue("/GeoFoncierConsultation/saveLogin",True)
                self.s.setValue("/GeoFoncierConsultation/login",login)
                self.s.setValue("/GeoFoncierConsultation/password",password)
                self.s.setValue("/GeoFoncierConsultation/territoire",zone)
            else:
                self.s.setValue("/GeoFoncierConsultation/saveLogin",False)
                self.s.remove("/GeoFoncierConsultation/password")
                self.s.remove("/GeoFoncierConsultation/login")
                self.s.remove("/GeoFoncierConsultation/territoire")
            
            Dossier.loadFromCSV(listeDossierCSV)
            
            nombreDossiers = Dossier.getNbrDossiers()
            if nombreDossiers == 1 :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.tr(u" dossier trouvé"))
            else :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.tr(u" dossiers trouvés"))
                
            #Remplissage de la tableView
            self.dlg.ui.tableWidget_dossiers.setColumnCount(7)
            self.dlg.ui.tableWidget_dossiers.setHorizontalHeaderLabels(['ID','Structure', u'Référence', 'Commune', 'Code INSEE', 'Date','Zip'])
            self.dlg.ui.tableWidget_dossiers.setRowCount(nombreDossiers)
            
            self.buttonGroupArchive = QButtonGroup()
            self.buttonGroupArchive.buttonClicked[int].connect(self.getArchive)
            
            for row,dossier in enumerate(Dossier.getListeDossiers()):
                element = dossier.getInformations()
                self.dlg.ui.tableWidget_dossiers.setItem(row, 0, QTableWidgetItem(str(row)))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 1, QTableWidgetItem(self.dlg.trUtf8(element["structure"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 2, QTableWidgetItem(self.dlg.trUtf8(element["reference"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 3, QTableWidgetItem(self.dlg.trUtf8(element["nom_commune"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 4, QTableWidgetItem(self.dlg.trUtf8(element["insee_commune"])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 5, QTableWidgetItem(self.dlg.trUtf8(element["date"])))
                
                button = QPushButton("Archive")
                self.buttonGroupArchive.addButton(button, row)
                self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 6, button)
            
            self.dlg.ui.tableWidget_dossiers.cellClicked.connect(self.getDetails)
            self.dlg.ui.tableWidget_dossiers.resizeColumnsToContents();
            self.dlg.ui.tableWidget_dossiers.setColumnWidth(0, 0);
            self.dlg.ui.tableWidget_dossiers.sortByColumn(5, Qt.DescendingOrder);
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
    
    def rechargerDossiers(self):
        """Recharge la totalité des dossiers"""
        try:
            self.PointLayerDossier
        except AttributeError:
            pass
        else:
            QgsMapLayerRegistry.instance().removeMapLayer(self.PointLayerDossier.id())
        
        try:
            self.PolygonLayerDossier
        except AttributeError:
            pass
        else:
            QgsMapLayerRegistry.instance().removeMapLayer(self.PolygonLayerDossier.id())
        self.canvas.refresh()
        
        Dossier.truncateDossier()
        
        while self.dlg.ui.tableWidget_dossiers.rowCount() > 0:
            self.dlg.ui.tableWidget_dossiers.removeRow(0)
            
        while self.dlg.ui.tableWidget_dossiers.columnCount() > 0:
            self.dlg.ui.tableWidget_dossiers.removeColumn(0)
        
        self.dlg.ui.tabWidget.setTabEnabled(2, False);
        self.listerDossiers()
        
    def getArchive(self,row):
        """Recupere le numero de la ligne et telecharge le fichier ZIP du dossier"""
        result = self.dlg.ui.tableWidget_dossiers.findItems(str(row), Qt.MatchExactly)
        if len(result) != 1:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Erreur de récupération de l'archive"), level=QgsMessageBar.CRITICAL, duration=self.duration)
        else:
            self.dossier = Dossier.getDossier(int(result[0].data(0)))
            fichier = "dossier_"+self.dossier.getReference()+".zip"
            fichier = fichier.decode('utf-8')
            fichier = unicodedata.normalize('NFKD', fichier).encode('ASCII', 'ignore')
            fichier = "-".join(fichier.split())
            self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.dossier.getURLArchiveZIP(),fichier)

    def enregistrerDossiers(self):
        """Enregistre les dossiers"""
        formatOutput = self.dlg.ui.comboBox_format.currentText()
        if formatOutput in ('csv', 'kml', 'xml'):
            filename = "mes_dossiers."+formatOutput
            self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.connexionAPI.getURLListeDossiers(formatOutput),filename)



   
    """ ONGLET DETAILS """    
    def getDetails(self):
        """Gere l'affichage de l'onglet details"""
        index = self.dlg.ui.tableWidget_dossiers.currentIndex();
        rownumber = index.row();
        index = index.sibling(rownumber, 0)
        idDossier = index.data()
        
        self.dlg.ui.listWidget_details.clear()
        self.dossier = Dossier.getDossier(int(idDossier))
        
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
        for doc in self.dossier.getDocuments():
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
        rect = QgsRectangle(envelope[0],envelope[2],envelope[1],envelope[3])
        self.canvas.setExtent(rect)
        
        if self.canvas.scale() < 1600:
            self.canvas.zoomScale(1600)
        
        self.canvas.refresh()
        
        self.dlg.setCursor(Qt.ArrowCursor)
    
    def rechargerDossier(self):
        """Recharger un dossier"""
        dossierZip = self.connexionAPI.getURL(self.dossier.getURLArchiveZIP())
        
        """Suppression des géométries ponctuelles"""
        zipField = self.PointLayerDossier.fieldNameIndex('ZIP')
        features = self.PointLayerDossier.getFeatures()
        for feature in features:
            featureZip = feature.attributes()[zipField]
            if str(featureZip) == str(dossierZip):
                self.PointLayerDossier.startEditing()
                self.PointLayerDossier.deleteFeature(feature.id())
                self.PointLayerDossier.commitChanges()
        
        """Suppression des géométries surfaciques"""
        zipField = self.PolygonLayerDossier.fieldNameIndex('ZIP')
        features = self.PolygonLayerDossier.getFeatures()
        for feature in features:
            featureZip = feature.attributes()[zipField]
            if str(featureZip) == str(dossierZip):
                self.PolygonLayerDossier.startEditing()
                self.PolygonLayerDossier.deleteFeature(feature.id())
                self.PolygonLayerDossier.commitChanges()    
            
        self.canvas.refresh()
        
        """Suppression des documents"""
        self.dossier.deleteDetails()
        
        """Rechargement du dossier"""
        self.getDetails()
        
    def voirCoucheQGIS(self):
        """Filtre les geometries et les affiche dans les couches correspondantes"""
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

    def enregistrerZIP(self):
        """Fonction qui enregistre le fichier ZIP sur le disque"""
        fichier = "dossier_"+self.dossier.getReference()+".zip"
        fichier = fichier.decode('utf-8')
        fichier = unicodedata.normalize('NFKD', fichier).encode('ASCII', 'ignore')
        fichier = "-".join(fichier.split())
        self.connexionAPI.getAndSaveExternalDocument(self.dlg,self.dossier.getURLArchiveZIP(),fichier)

    def getExternalDocument(self):
        """Fonction qui enregistre un document sur le disque"""
        row = self.dlg.ui.listWidget_details.currentRow()
        doc = self.dossier.getDocument(row)
        fichier = doc.getFileName()
        
        if isinstance(fichier, str):
            fichier = fichier.decode('utf-8')
            
        fichier = fichier + "." + doc.getExtension()
        fichier = unicodedata.normalize('NFKD', fichier).encode('ASCII', 'ignore')
        fichier = "-".join(fichier.split())
        self.connexionAPI.getAndSaveExternalDocument(self.dlg,doc.getURL(),fichier)




    """ Gestion des couches raster et vecteurs """
    def layerDeleted(self,idLayer):
        """Slot qui ecoute les couches supprimees"""
        for i in self.layers:
            if idLayer == i:
                if self.layers[i] == "osm":
                    self.dlg.ui.pushButton_couche_osm.setEnabled(True)
                elif self.layers[i] == "googlesat":
                    self.dlg.ui.pushButton_couche_gsat.setEnabled(True) 

    def addPointLayerDossier(self):
        """Permet d'ajouter la couche des localisants"""
        #self.enableUseOfGlobalCrs()
        self.PointLayerDossier = QgsVectorLayer("Point",self.dlg.tr(u"Dossier GéoFoncier"), "memory")
        table_attributairePoint = [ QgsField(u"Référence",QVariant.String),QgsField("Structure",QVariant.String),QgsField("Commune", QVariant.String), QgsField("INSEE", QVariant.String), QgsField("Date", QVariant.String), QgsField("Localisants", QVariant.String), QgsField("ZIP", QVariant.String) ]
        self.dataProviderPointDossier = self.PointLayerDossier.dataProvider()
        self.dataProviderPointDossier.addAttributes(table_attributairePoint)
        self.PointLayerDossier.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))
        self.PointLayerDossier.loadSldStyle(":/resources/point")
        QgsMapLayerRegistry.instance().addMapLayer(self.PointLayerDossier)
        QObject.connect(self.PointLayerDossier, SIGNAL("layerDeleted()"), self.PointLayerDossierDeleted)
        #self.disableUseOfGlobalCrs()
    
    def PointLayerDossierDeleted(self):
        """Supprime la variable des localisants si la couche est supprimé"""
        del self.PointLayerDossier
        
    def addPolygonLayerDossier(self):
        """Permet d'ajouter la couche des polygones"""
        #self.enableUseOfGlobalCrs()
        self.PolygonLayerDossier = QgsVectorLayer("Polygon",self.dlg.tr(u"Dossier GéoFoncier"), "memory")
        table_attributairePolygons = [ QgsField(u"Référence",QVariant.String),QgsField("Structure",QVariant.String),QgsField("Commune", QVariant.String), QgsField("INSEE", QVariant.String), QgsField("Date", QVariant.String), QgsField("ZIP", QVariant.String) ]
        self.dataProviderPolygonDossier = self.PolygonLayerDossier.dataProvider()
        self.dataProviderPolygonDossier.addAttributes(table_attributairePolygons)
        self.PolygonLayerDossier.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))
        self.PolygonLayerDossier.loadSldStyle(":/resources/polygons")
        QgsMapLayerRegistry.instance().addMapLayer(self.PolygonLayerDossier)
        QObject.connect(self.PolygonLayerDossier, SIGNAL("layerDeleted()"), self.PolygonLayerDossierDeleted)
        #self.disableUseOfGlobalCrs()
        
    def PolygonLayerDossierDeleted(self):
        """Supprime la variable des polygones si la couche est supprimé"""
        del self.PolygonLayerDossier
    
    def informationWindowOrdreCouches(self):
        try:
            self.informationFenetreOrdreCoucheDejaVu
        except AttributeError:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Vous pouvez modifier l'ordre des couches en effectuant un glisser/déposer des couches OpenStreetMap et Google en les déplacant vers le bas dans la fenêtre de gauche."), level=QgsMessageBar.INFO , duration=self.duration)
            self.informationFenetreOrdreCoucheDejaVu = True
            
    def ajouterCoucheOSM(self):
        """Ajoute la couche OSM"""
        self.informationWindowOrdreCouches()
        self.enableUseOfGlobalCrs()
        fileInfo = QFileInfo(os.path.join(self.resources_dir,"osmfr.xml"))
        self.osmLayer = QgsRasterLayer(fileInfo.filePath(), "OpenStreetMap")
        
        if not self.osmLayer.isValid():
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Erreur d'ajout de la couche OpenStreetMap"), level=QgsMessageBar.CRITICAL, duration=self.duration)
        
        self.osmLayer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId))
        QgsMapLayerRegistry.instance().addMapLayer(self.osmLayer)
        self.layers[self.osmLayer.id()] = "osm"
        self.dlg.ui.pushButton_couche_osm.setEnabled(False)
        self.disableUseOfGlobalCrs()
        
    def ajouterCoucheGSAT(self):
        """Ajoute la couche google satellite"""
        self.informationWindowOrdreCouches()
        self.enableUseOfGlobalCrs()
        fileInfo = QFileInfo(os.path.join(self.resources_dir,"googlesat.xml"))
        self.googleLayer = QgsRasterLayer(fileInfo.filePath(), u"Photo aérienne Google")
        
        if not self.googleLayer.isValid():
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Erreur d'ajout de la couche Google"), level=QgsMessageBar.CRITICAL, duration=self.duration)
            
        self.googleLayer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId))
        QgsMapLayerRegistry.instance().addMapLayer(self.googleLayer)
        self.layers[self.googleLayer.id()] = "googlesat"
        self.dlg.ui.pushButton_couche_gsat.setEnabled(False)
        self.disableUseOfGlobalCrs()

    def enableUseOfGlobalCrs(self):
        self.s = QSettings()
        self.oldDefaultProjection = self.s.value("/Projections/defaultBehaviour")
        self.s.setValue( "/Projections/defaultBehaviour", "useProject")
        #self.s.setValue("/Projections/otfTransformAutoEnable", "true")
    
    def disableUseOfGlobalCrs(self):  
        self.s.setValue( "/Projections/defaultBehaviour", self.oldDefaultProjection) 

    """ Fin de la gestion des couches """