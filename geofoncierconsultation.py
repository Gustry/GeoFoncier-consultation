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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
#import resources_rc
# Import the code for the dialog
from geofoncierconsultationdialog import GeoFoncierConsultationDialog

from connexion_client_GF import ConnexionClientGF
from dossier import Dossier
from exception import LoginException, NoResult

import os.path
from fileinput import close


class GeoFoncierConsultationDetails:
    
    dossier = None
    connexionAPI = None

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
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

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/geofoncierconsultation/icon.png"),
            u"GéoFoncier", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Mes dossiers GéoFoncier", self.action)
        
        #Ajout du connecteur bouton d'aide
        QObject.connect(self.dlg.ui.pushButton_help, SIGNAL("clicked()"), self.aboutWindow)
        QObject.connect(self.dlg.ui.pushButton_listerDossiers, SIGNAL("clicked()"), self.listerDossiers)
        QObject.connect(self.dlg.ui.lineEdit_login, SIGNAL("textChanged(QString)"), self.checkLineEdits)
        QObject.connect(self.dlg.ui.lineEdit_password, SIGNAL("textChanged(QString)"), self.checkLineEdits)
        #QObject.connect(self.dlg.ui.pushButton_quitter, SIGNAL("clicked()"), self.quitter())

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Mes dossiers GéoFoncier", self.action)
        self.iface.removeToolBarIcon(self.action)
          
    def aboutWindow(self):
        infoString = QCoreApplication.translate('GéoFoncier', self.dlg.trUtf8("Plugin QGIS pour la consultation des dossiers GéoFoncier<br /><br />Auteur: Etienne Trimaille<br />Mail: <a href=\"mailto:etienne@trimaille.eu\">etienne@trimaille.eu</a>\n<br /><strong>Ce plugin est expérimental !</strong>"))
        QMessageBox.information(self.dlg,self.dlg.trUtf8("GéoFoncier"), infoString)
        
    def errorWindow(self,message):
        QMessageBox.critical(self.dlg, self.dlg.trUtf8("GéoFoncier"), message)
        
    def informationWindow(self,message):
        QMessageBox.information(self.dlg, self.dlg.trUtf8("GéoFoncier"), message)

    def checkLineEdits(self):
        if self.dlg.ui.lineEdit_login.text() != "" and self.dlg.ui.lineEdit_password.text() != "":
            self.dlg.ui.pushButton_listerDossiers.setEnabled(True)
        else:
            self.dlg.ui.pushButton_listerDossiers.setEnabled(False)
            
    def listerDossiers(self):
        msgBox = QProgressDialog("Chargement","Annuler",0,0)
        msgBox.setValue(-1)
        msgBox.setWindowTitle("Chargement des dossiers")
        msgBox.setAutoReset(True)
        msgBox.setAutoClose(False)
        msgBox.open()
        QApplication.processEvents()
        
        global connexionAPI
        
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
        
        connexionAPI = ConnexionClientGF(login, password, zone)
        listeDossierCSV = ''
        try:
            listeDossierCSV = connexionAPI.getListeDossiers()
        except LoginException, e:
            self.errorWindow("Mauvais nom d'utilisateur ou mot de passe")
            self.run()
        except NoResult, e:
            self.errorWindow("Aucun dossier pour ce territoire")
            self.run()
        else:
            Dossier.loadFromCSV(listeDossierCSV)
            
            nombreDossiers = Dossier.getNbrDossiers()
            if nombreDossiers == 1 :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.trUtf8(" dossier trouvé"))
            else :
                self.dlg.ui.label_listeDossiers.setText(str(Dossier.getNbrDossiers())+ self.dlg.trUtf8(" dossiers trouvés"))
                
            #Remplissage de la tableView
            self.dlg.ui.tableWidget_dossiers.setColumnCount(7)
            self.dlg.ui.tableWidget_dossiers.setHorizontalHeaderLabels(['Structure', 'Ref', 'Commune', 'Code INSEE', 'Date','Zip','Afficher'])
            self.dlg.ui.tableWidget_dossiers.setRowCount(nombreDossiers)
            
            self.buttonGroupArchive = QButtonGroup()
            self.buttonGroupArchive.buttonClicked[int].connect(self.getArchive)
            self.buttonGroupDetails = QButtonGroup()
            self.buttonGroupDetails.buttonClicked[int].connect(self.getDetails)
            
            for row,dossier in enumerate(Dossier.listeDossiers):
                element = dossier.getInformations()
                self.dlg.ui.tableWidget_dossiers.setItem(row, 0, QTableWidgetItem(self.dlg.trUtf8(element[0])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 1, QTableWidgetItem(self.dlg.trUtf8(element[1])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 2, QTableWidgetItem(self.dlg.trUtf8(element[2])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 3, QTableWidgetItem(self.dlg.trUtf8(element[3])))
                self.dlg.ui.tableWidget_dossiers.setItem(row, 4, QTableWidgetItem(self.dlg.trUtf8(element[4])))
                
                button = QPushButton("Archive")
                self.buttonGroupArchive.addButton(button, row)
                self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 5, button)
                
                button = QPushButton("Voir")
                self.buttonGroupDetails.addButton(button, row)
                self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 6, button)
            
            self.dlg.ui.tableWidget_dossiers.resizeColumnsToContents();
            self.dlg.ui.tableWidget_dossiers.resizeRowsToContents();
            self.dlg.ui.tableWidget_dossiers.show()
            self.dlg.ui.label_listeDossiers.show()
            
            msgBox.close()

    def getArchive(self,row):
        global connexionAPI
        dossier = Dossier.getDossier(row)
        connexionAPI.getExternalLink(dossier.getURLArchiveZIP())
        
    def getDetails(self,row):
        msgBox = QProgressDialog("Chargement","Annuler",0,0)
        msgBox.setValue(-1)
        msgBox.setWindowTitle("Chargement du dossier")
        msgBox.setAutoReset(True)
        msgBox.setAutoClose(False)
        msgBox.open()
        QApplication.processEvents()

        global connexionAPI
        global dossier
        self.dlg.ui.listWidget_details.clear()
        dossier = Dossier.getDossier(row)

        if dossier.getGeometrie() == None:
            dossier.loadDetails(connexionAPI.get(dossier.getURLDossier()))
            
        self.dlg.ui.label_reference.setText(dossier.reference)
        self.dlg.ui.label_structure.setText(dossier.structure_ge)
        self.dlg.ui.label_commune.setText(dossier.nom_commune)
        self.dlg.ui.label_date.setText(dossier.date)
        self.dlg.ui.label_insee.setText(dossier.insee_commune)
        QApplication.processEvents()
        for i,doc in enumerate(dossier.getDocuments()):
            item = QListWidgetItem()
            tab = dossier.getTypeOfDocument(i)
            item.setText(self.dlg.trUtf8(tab[0]));
            self.dlg.ui.listWidget_details.addItem(item);
        self.dlg.ui.listWidget_details.clicked.connect(self.getExternalDocument)
        self.dlg.ui.tabWidget.setTabEnabled(1, True);
        self.dlg.ui.tabWidget.setCurrentIndex(1)
        msgBox.close()

    def getExternalDocument(self):
        global connexionAPI
        row = self.dlg.ui.listWidget_details.currentRow()
        connexionAPI.getExternalLink(dossier.getURLDocument(row))
                
    def run(self):
        #Initialisation
        self.dlg.setFixedSize(self.dlg.size());
        
        #Load zone
        try:
            with open(os.path.join(self.plugin_dir,"zone.txt"), "r") as fichier :
                ancienneZone = fichier.read()
                fichier.close()
                if ancienneZone != "":
                    index = self.dlg.ui.comboBox_zone.findText(ancienneZone)
                    self.dlg.ui.comboBox_zone.setCurrentIndex(index)
        except IOError:
            pass
        
        self.dlg.ui.tabWidget.setTabEnabled(1, False);
        self.dlg.ui.tabWidget.setTabText(0,"Dossiers")
        self.dlg.ui.tabWidget.setTabText(1,self.dlg.trUtf8("Détails"))
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
        del Dossier.listeDossiers[:]
        self.dlg.show()

    def saveZone(self, zone):
        with open(os.path.join(self.plugin_dir,"zone.txt"), "w") as fichier :
            fichier.write(zone)
            fichier.close()