# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geofoncierconsultation.ui'
#
# Created: Fri Nov 22 21:21:34 2013
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
        GeoFoncierConsultation.resize(785, 340)
        self.layoutWidget = QtGui.QWidget(GeoFoncierConsultation)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 781, 26))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_login = QtGui.QLabel(self.layoutWidget)
        self.label_login.setObjectName(_fromUtf8("label_login"))
        self.horizontalLayout.addWidget(self.label_login)
        self.lineEdit_login = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_login.setEnabled(True)
        self.lineEdit_login.setObjectName(_fromUtf8("lineEdit_login"))
        self.horizontalLayout.addWidget(self.lineEdit_login)
        self.label_password = QtGui.QLabel(self.layoutWidget)
        self.label_password.setObjectName(_fromUtf8("label_password"))
        self.horizontalLayout.addWidget(self.label_password)
        self.lineEdit_password = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_password.setEnabled(True)
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_password.setObjectName(_fromUtf8("lineEdit_password"))
        self.horizontalLayout.addWidget(self.lineEdit_password)
        self.label_zone = QtGui.QLabel(self.layoutWidget)
        self.label_zone.setObjectName(_fromUtf8("label_zone"))
        self.horizontalLayout.addWidget(self.label_zone)
        self.comboBox_zone = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_zone.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_zone.setObjectName(_fromUtf8("comboBox_zone"))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.comboBox_zone.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_zone)
        self.pushButton_listerDossiers = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_listerDossiers.setDefault(True)
        self.pushButton_listerDossiers.setObjectName(_fromUtf8("pushButton_listerDossiers"))
        self.horizontalLayout.addWidget(self.pushButton_listerDossiers)
        self.pushButton_help = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_help.setObjectName(_fromUtf8("pushButton_help"))
        self.horizontalLayout.addWidget(self.pushButton_help)
        self.tabWidget = QtGui.QTabWidget(GeoFoncierConsultation)
        self.tabWidget.setGeometry(QtCore.QRect(0, 40, 781, 301))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tableWidget_dossiers = QtGui.QTableWidget(self.tab)
        self.tableWidget_dossiers.setGeometry(QtCore.QRect(0, 30, 771, 241))
        self.tableWidget_dossiers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_dossiers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_dossiers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_dossiers.setGridStyle(QtCore.Qt.DashDotDotLine)
        self.tableWidget_dossiers.setObjectName(_fromUtf8("tableWidget_dossiers"))
        self.tableWidget_dossiers.setColumnCount(0)
        self.tableWidget_dossiers.setRowCount(0)
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 761, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_listeDossiers = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_listeDossiers.setObjectName(_fromUtf8("label_listeDossiers"))
        self.horizontalLayout_2.addWidget(self.label_listeDossiers)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_enregistrer_dossiers = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_enregistrer_dossiers.setObjectName(_fromUtf8("pushButton_enregistrer_dossiers"))
        self.horizontalLayout_2.addWidget(self.pushButton_enregistrer_dossiers)
        self.comboBox_format = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_format.setObjectName(_fromUtf8("comboBox_format"))
        self.comboBox_format.addItem(_fromUtf8(""))
        self.comboBox_format.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_format)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.listWidget_details = QtGui.QListWidget(self.tab_2)
        self.listWidget_details.setGeometry(QtCore.QRect(420, 30, 351, 231))
        self.listWidget_details.setObjectName(_fromUtf8("listWidget_details"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(420, 10, 201, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_reference = QtGui.QLabel(self.tab_2)
        self.label_reference.setGeometry(QtCore.QRect(20, 40, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_reference.setFont(font)
        self.label_reference.setObjectName(_fromUtf8("label_reference"))
        self.layoutWidget1 = QtGui.QWidget(self.tab_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 80, 261, 137))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setSpacing(25)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_structure = QtGui.QLabel(self.layoutWidget1)
        self.label_structure.setObjectName(_fromUtf8("label_structure"))
        self.verticalLayout.addWidget(self.label_structure)
        self.label_commune = QtGui.QLabel(self.layoutWidget1)
        self.label_commune.setObjectName(_fromUtf8("label_commune"))
        self.verticalLayout.addWidget(self.label_commune)
        self.label_insee = QtGui.QLabel(self.layoutWidget1)
        self.label_insee.setObjectName(_fromUtf8("label_insee"))
        self.verticalLayout.addWidget(self.label_insee)
        self.label_date = QtGui.QLabel(self.layoutWidget1)
        self.label_date.setObjectName(_fromUtf8("label_date"))
        self.verticalLayout.addWidget(self.label_date)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(GeoFoncierConsultation)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GeoFoncierConsultation)

    def retranslateUi(self, GeoFoncierConsultation):
        GeoFoncierConsultation.setWindowTitle(_translate("GeoFoncierConsultation", "GéoFoncier : consultation de dossiers", None))
        self.label_login.setText(_translate("GeoFoncierConsultation", "Client", None))
        self.lineEdit_login.setText(_translate("GeoFoncierConsultation", "clientge", None))
        self.label_password.setText(_translate("GeoFoncierConsultation", "Mot de passe", None))
        self.lineEdit_password.setText(_translate("GeoFoncierConsultation", "clientge", None))
        self.label_zone.setText(_translate("GeoFoncierConsultation", "Territoire", None))
        self.comboBox_zone.setItemText(0, _translate("GeoFoncierConsultation", "metropole", None))
        self.comboBox_zone.setItemText(1, _translate("GeoFoncierConsultation", "antilles", None))
        self.comboBox_zone.setItemText(2, _translate("GeoFoncierConsultation", "guyane", None))
        self.comboBox_zone.setItemText(3, _translate("GeoFoncierConsultation", "reunion", None))
        self.comboBox_zone.setItemText(4, _translate("GeoFoncierConsultation", "mayotte", None))
        self.pushButton_listerDossiers.setText(_translate("GeoFoncierConsultation", "Lister les dossiers", None))
        self.pushButton_help.setText(_translate("GeoFoncierConsultation", "Aide", None))
        self.tableWidget_dossiers.setSortingEnabled(True)
        self.label_listeDossiers.setText(_translate("GeoFoncierConsultation", "Dossiers", None))
        self.pushButton_enregistrer_dossiers.setText(_translate("GeoFoncierConsultation", "Enregistrer les dossiers en", None))
        self.comboBox_format.setItemText(0, _translate("GeoFoncierConsultation", "kml", None))
        self.comboBox_format.setItemText(1, _translate("GeoFoncierConsultation", "csv", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("GeoFoncierConsultation", "Tab 1", None))
        self.label.setText(_translate("GeoFoncierConsultation", "Liste des documents à télécharger :", None))
        self.label_reference.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_structure.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_commune.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_insee.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.label_date.setText(_translate("GeoFoncierConsultation", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("GeoFoncierConsultation", "Tab 2", None))

