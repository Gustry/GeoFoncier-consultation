# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geofoncierconsultation.ui'
#
# Created: Fri Dec 13 00:08:50 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GeoFoncierConsultation(object):
    def setupUi(self, GeoFoncierConsultation):
        GeoFoncierConsultation.setObjectName(_fromUtf8("GeoFoncierConsultation"))
        GeoFoncierConsultation.resize(854, 200)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeoFoncierConsultation.sizePolicy().hasHeightForWidth())
        GeoFoncierConsultation.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.formLayoutWidget = QtGui.QWidget(self.tab_3)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 211, 101))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_login = QtGui.QLabel(self.formLayoutWidget)
        self.label_login.setObjectName(_fromUtf8("label_login"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_login)
        self.lineEdit_login = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_login.setEnabled(True)
        self.lineEdit_login.setText(_fromUtf8("clientge"))
        self.lineEdit_login.setObjectName(_fromUtf8("lineEdit_login"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_login)
        self.label_password = QtGui.QLabel(self.formLayoutWidget)
        self.label_password.setObjectName(_fromUtf8("label_password"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_password.setEnabled(True)
        self.lineEdit_password.setText(_fromUtf8("clientge"))
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_password.setObjectName(_fromUtf8("lineEdit_password"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_password)
        self.label_zone = QtGui.QLabel(self.formLayoutWidget)
        self.label_zone.setObjectName(_fromUtf8("label_zone"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_zone)
        self.comboBox_zone = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_zone.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_zone.setWhatsThis(_fromUtf8(""))
        self.comboBox_zone.setObjectName(_fromUtf8("comboBox_zone"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.setItemText(0, _fromUtf8("metropole"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.setItemText(1, _fromUtf8("antilles"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.setItemText(2, _fromUtf8("guyane"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.setItemText(3, _fromUtf8("reunion"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.setItemText(4, _fromUtf8("mayotte"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_zone)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.tab_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(250, 20, 191, 101))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton_listerDossiers = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_listerDossiers.setDefault(True)
        self.pushButton_listerDossiers.setObjectName(_fromUtf8("pushButton_listerDossiers"))
        self.verticalLayout_3.addWidget(self.pushButton_listerDossiers)
        self.pushButton_site_geofoncier = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_site_geofoncier.setObjectName(_fromUtf8("pushButton_site_geofoncier"))
        self.verticalLayout_3.addWidget(self.pushButton_site_geofoncier)
        self.pushButton_help = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_help.setObjectName(_fromUtf8("pushButton_help"))
        self.verticalLayout_3.addWidget(self.pushButton_help)
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(455, 4, 201, 111))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/resources/banniere")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_listeDossiers = QtGui.QLabel(self.tab)
        self.label_listeDossiers.setObjectName(_fromUtf8("label_listeDossiers"))
        self.horizontalLayout_2.addWidget(self.label_listeDossiers)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_couche_osm = QtGui.QPushButton(self.tab)
        self.pushButton_couche_osm.setObjectName(_fromUtf8("pushButton_couche_osm"))
        self.horizontalLayout_2.addWidget(self.pushButton_couche_osm)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_enregistrer_dossiers = QtGui.QPushButton(self.tab)
        self.pushButton_enregistrer_dossiers.setObjectName(_fromUtf8("pushButton_enregistrer_dossiers"))
        self.horizontalLayout_2.addWidget(self.pushButton_enregistrer_dossiers)
        self.comboBox_format = QtGui.QComboBox(self.tab)
        self.comboBox_format.setWhatsThis(_fromUtf8(""))
        self.comboBox_format.setObjectName(_fromUtf8("comboBox_format"))
        self.comboBox_format.addItem(_fromUtf8(""))
        self.comboBox_format.addItem(_fromUtf8(""))
        self.comboBox_format.setItemText(1, _fromUtf8("xml"))
        self.comboBox_format.addItem(_fromUtf8(""))
        self.comboBox_format.setItemText(2, _fromUtf8("csv"))
        self.horizontalLayout_2.addWidget(self.comboBox_format)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tableWidget_dossiers = QtGui.QTableWidget(self.tab)
        self.tableWidget_dossiers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_dossiers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_dossiers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_dossiers.setGridStyle(QtCore.Qt.DashDotDotLine)
        self.tableWidget_dossiers.setObjectName(_fromUtf8("tableWidget_dossiers"))
        self.tableWidget_dossiers.setColumnCount(0)
        self.tableWidget_dossiers.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget_dossiers, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.listWidget_details = QtGui.QListWidget(self.tab_2)
        self.listWidget_details.setGeometry(QtCore.QRect(420, 30, 351, 101))
        self.listWidget_details.setObjectName(_fromUtf8("listWidget_details"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(420, 10, 201, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_reference = QtGui.QLabel(self.tab_2)
        self.label_reference.setGeometry(QtCore.QRect(10, 10, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_reference.setFont(font)
        self.label_reference.setWhatsThis(_fromUtf8(""))
        self.label_reference.setObjectName(_fromUtf8("label_reference"))
        self.layoutWidget_2 = QtGui.QWidget(self.tab_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 30, 211, 101))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_structure = QtGui.QLabel(self.layoutWidget_2)
        self.label_structure.setWhatsThis(_fromUtf8(""))
        self.label_structure.setObjectName(_fromUtf8("label_structure"))
        self.verticalLayout.addWidget(self.label_structure)
        self.label_commune = QtGui.QLabel(self.layoutWidget_2)
        self.label_commune.setWhatsThis(_fromUtf8(""))
        self.label_commune.setObjectName(_fromUtf8("label_commune"))
        self.verticalLayout.addWidget(self.label_commune)
        self.label_insee = QtGui.QLabel(self.layoutWidget_2)
        self.label_insee.setWhatsThis(_fromUtf8(""))
        self.label_insee.setObjectName(_fromUtf8("label_insee"))
        self.verticalLayout.addWidget(self.label_insee)
        self.label_date = QtGui.QLabel(self.layoutWidget_2)
        self.label_date.setWhatsThis(_fromUtf8(""))
        self.label_date.setObjectName(_fromUtf8("label_date"))
        self.verticalLayout.addWidget(self.label_date)
        self.verticalLayoutWidget = QtGui.QWidget(self.tab_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(250, 40, 160, 82))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButton_telecharger_kml = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_telecharger_kml.setObjectName(_fromUtf8("pushButton_telecharger_kml"))
        self.verticalLayout_2.addWidget(self.pushButton_telecharger_kml)
        self.pushButton_ZIP = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_ZIP.setObjectName(_fromUtf8("pushButton_ZIP"))
        self.verticalLayout_2.addWidget(self.pushButton_ZIP)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        GeoFoncierConsultation.setWidget(self.dockWidgetContents)

        self.retranslateUi(GeoFoncierConsultation)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GeoFoncierConsultation)

    def retranslateUi(self, GeoFoncierConsultation):
        GeoFoncierConsultation.setWindowTitle(_translate("GeoFoncierConsultation", "Mes dossiers GéoFoncier", None))
        self.label_login.setText(_translate("GeoFoncierConsultation", "Client", None))
        self.label_password.setText(_translate("GeoFoncierConsultation", "Mot de passe", None))
        self.label_zone.setText(_translate("GeoFoncierConsultation", "Territoire", None))
        self.pushButton_listerDossiers.setText(_translate("GeoFoncierConsultation", "Lister les dossiers", None))
        self.pushButton_site_geofoncier.setText(_translate("GeoFoncierConsultation", "Accéder au site GéoFoncier", None))
        self.pushButton_help.setText(_translate("GeoFoncierConsultation", "Aide", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("GeoFoncierConsultation", "Connexion", None))
        self.label_listeDossiers.setText(_translate("GeoFoncierConsultation", "Dossiers", None))
        self.pushButton_couche_osm.setText(_translate("GeoFoncierConsultation", "Couche cartographique", None))
        self.pushButton_enregistrer_dossiers.setText(_translate("GeoFoncierConsultation", "Enregistrer les dossiers en", None))
        self.comboBox_format.setItemText(0, _translate("GeoFoncierConsultation", "kml", None))
        self.tableWidget_dossiers.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("GeoFoncierConsultation", "Dossiers", None))
        self.label.setText(_translate("GeoFoncierConsultation", "Liste des documents à télécharger :", None))
        self.label_reference.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_structure.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_commune.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_insee.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_date.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.pushButton_telecharger_kml.setText(_translate("GeoFoncierConsultation", "Télécharger KML", None))
        self.pushButton_ZIP.setText(_translate("GeoFoncierConsultation", "Archive ZIP", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("GeoFoncierConsultation", "Détails", None))

import resources_rc
