# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geofoncierconsultation.ui'
#
# Created: Tue Nov 12 20:00:26 2013
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
        GeoFoncierConsultation.resize(854, 363)
        self.pushButton_help = QtGui.QPushButton(GeoFoncierConsultation)
        self.pushButton_help.setGeometry(QtCore.QRect(800, 340, 51, 24))
        self.pushButton_help.setObjectName(_fromUtf8("pushButton_help"))
        self.layoutWidget = QtGui.QWidget(GeoFoncierConsultation)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 851, 26))
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
        self.pushButton_listerDossiers.setObjectName(_fromUtf8("pushButton_listerDossiers"))
        self.horizontalLayout.addWidget(self.pushButton_listerDossiers)
        self.label_listeDossiers = QtGui.QLabel(GeoFoncierConsultation)
        self.label_listeDossiers.setGeometry(QtCore.QRect(0, 40, 141, 20))
        self.label_listeDossiers.setObjectName(_fromUtf8("label_listeDossiers"))
        self.tableWidget_dossiers = QtGui.QTableWidget(GeoFoncierConsultation)
        self.tableWidget_dossiers.setGeometry(QtCore.QRect(0, 60, 851, 279))
        self.tableWidget_dossiers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_dossiers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_dossiers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_dossiers.setGridStyle(QtCore.Qt.DashDotDotLine)
        self.tableWidget_dossiers.setObjectName(_fromUtf8("tableWidget_dossiers"))
        self.tableWidget_dossiers.setColumnCount(0)
        self.tableWidget_dossiers.setRowCount(0)

        self.retranslateUi(GeoFoncierConsultation)
        QtCore.QMetaObject.connectSlotsByName(GeoFoncierConsultation)

    def retranslateUi(self, GeoFoncierConsultation):
        GeoFoncierConsultation.setWindowTitle(_translate("GeoFoncierConsultation", "GéoFoncier : consultation de dossiers", None))
        self.pushButton_help.setText(_translate("GeoFoncierConsultation", "Aide", None))
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
        self.label_listeDossiers.setText(_translate("GeoFoncierConsultation", "Dossiers", None))
        self.tableWidget_dossiers.setSortingEnabled(True)

