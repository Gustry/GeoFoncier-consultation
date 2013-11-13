# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoFoncierConsultation
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


class GeoFoncierConsultation:

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
        self.iface.addPluginToMenu(u"&GéoFoncier : diffusion aux clients", self.action)
        
        #Ajout du connecteur bouton d'aide
        QObject.connect(self.dlg.ui.pushButton_help, SIGNAL("clicked()"), self.aboutWindow)
        QObject.connect(self.dlg.ui.pushButton_listerDossiers, SIGNAL("clicked()"), self.listerDossiers)
        #QObject.connect(self.dlg.ui.pushButton_quitter, SIGNAL("clicked()"), self.quitter())

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&GéoFoncier : diffusion aux clients", self.action)
        self.iface.removeToolBarIcon(self.action)
          
    def aboutWindow(self):
        infoString = QCoreApplication.translate('GéoFoncier', self.dlg.trUtf8("Plugin QGIS pour la consultation des dossiers GéoFoncier<br /><br />Auteur: Etienne Trimaille<br />Mail: <a href=\"mailto:etienne@trimaille.eu\">etienne@trimaille.eu</a>\n<br /><strong>Ce plugin est expérimental !</strong>"))
        QMessageBox.information(self.dlg,self.dlg.trUtf8("GéoFoncier"), infoString)
        
    def errorWindow(self,message):
        QMessageBox.critical(self.dlg, self.dlg.trUtf8("GéoFoncier"), message)
        
    def informationWindow(self,message):
        QMessageBox.information(self.dlg, self.dlg.trUtf8("GéoFoncier"), message)

    def listerDossiers(self):
        self.dlg.ui.label_listeDossiers.setText("Recherche en cours")
        self.dlg.ui.label_listeDossiers.show()
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
            self.dlg.ui.tableWidget_dossiers.setColumnCount(6)
            self.dlg.ui.tableWidget_dossiers.setHorizontalHeaderLabels(['Structure', 'Ref', 'Commune', 'Code INSEE', 'Date','Zip','Doc','Afficher'])
            self.dlg.ui.tableWidget_dossiers.setRowCount(nombreDossiers)
            
            self.buttonGroupArchive = QButtonGroup()
            self.buttonGroupArchive.buttonClicked[int].connect(self.getArchive)
            self.buttonGroupDocument = QButtonGroup()
            self.buttonGroupDocument.buttonClicked[int].connect(self.getDocument)
            
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
                button = QPushButton("Document")
                self.buttonGroupDocument.addButton(button, row)
                #self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 6, button)
                #self.dlg.ui.tableWidget_dossiers.setCellWidget(row, 7, QPushButton("Afficher"))
            
            self.dlg.ui.tableWidget_dossiers.resizeColumnsToContents();
            self.dlg.ui.tableWidget_dossiers.resizeRowsToContents();
            self.dlg.ui.tableWidget_dossiers.show()

    def getArchive(self,row):
        dossier = Dossier.getDossier(row)
        login = self.dlg.ui.lineEdit_login.text()
        password = self.dlg.ui.lineEdit_password.text()
        zone = str(self.dlg.ui.comboBox_zone.currentText())
        connexionAPI = ConnexionClientGF(login, password, zone)
        connexionAPI.getExternalLink(dossier.getURLArchiveZIP())
        
    def getDocument(self,row):
        dossier = Dossier.getDossier(row)
        login = self.dlg.ui.lineEdit_login.text()
        password = self.dlg.ui.lineEdit_password.text()
        zone = str(self.dlg.ui.comboBox_zone.currentText())
        connexionAPI = ConnexionClientGF(login, password, zone)
        connexionAPI.getExternalLink(dossier.getURLDocument())
         
                
    def run(self):
        #Initialisation
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
