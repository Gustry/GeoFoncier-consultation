# -*- coding: utf-8 -*- 
from PyQt4.QtCore import QUrl, QFileInfo, QFile, QIODevice
from PyQt4.QtGui import QApplication, QFileDialog, QDialog, QProgressBar, QLabel, QPushButton, QDialogButtonBox, \
                    QVBoxLayout, QMessageBox, QDesktopServices
from PyQt4.QtNetwork import QHttp
from urlparse import urlparse, parse_qs


class Saver(QDialog):
    def __init__(self, login, password, url, nameFile, parent = None):
        super(Saver, self).__init__(parent)
        
        self.url_to_download = url
        self.login = login
        self.password = password
        self.nameFile = nameFile
        
        urlparse(self.url_to_download).query
        self.parameters = parse_qs(urlparse(url).query)
        
        self.httpGetId = 0
        self.httpRequestAborted = False
        self.statusLabel = QLabel(u'Enregistrement %s' % self.url_to_download)
        self.closeButton = QPushButton("Fermer")
        self.closeButton.setAutoDefault(False)
        self.openFileButton = QPushButton("Ouvrir le fichier")
        self.openFileButton.setAutoDefault(False)
        self.openDirectoryButton = QPushButton("Ouvrir le repertoire")
        self.openDirectoryButton.setAutoDefault(False)
        self.progressBar = QProgressBar()

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.openFileButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.openDirectoryButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.closeButton, QDialogButtonBox.RejectRole)

        self.http = QHttp(self)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.closeButton.clicked.connect(self.cancelDownload)
        self.openDirectoryButton.clicked.connect(self.openDirectory)
        self.openFileButton.clicked.connect(self.openFile)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(u'Enregistrement')
        self.openFileButton.hide()
        self.openDirectoryButton.hide()
        self.show()
        self.downloadFile()


    def downloadFile(self):
        url = QUrl(self.url_to_download)

        fileName = QFileDialog.getSaveFileName(self, "Enregistrer la liste des dossiers", self.nameFile, "conf")

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Error',
                    'Unable to save the file %s: %s.' % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        mode = QHttp.ConnectionModeHttps
        port = url.port()
        if port == -1:
            port = 0
        self.http.setHost(url.host(), mode, port)
        self.httpRequestAborted = False
        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '/'

        #Hack parameters
        path = path+("?")
        for item in url.queryItems():
            path = path + item[0] + "=" + item[1] + "&" 
        
        self.http.setUser(self.login, self.password)
        self.httpGetId = self.http.get(path, self.outFile)

    def cancelDownload(self):
        self.statusLabel.setText(u"Enregistrement annule")
        self.httpRequestAborted = True
        self.http.abort()
        self.close()

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None
            return

        self.outFile.close()
        
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)

        if error:
            self.outFile.remove()
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % self.http.errorString())

        self.statusLabel.setText('Enregistrement ok')
        self.openDirectoryButton.show()
        self.openFileButton.show()
        #self.close()      

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            print responseHeader.statusCode()
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return
        self.progressBar.setMaximum(totalBytes)
        self.progressBar.setValue(bytesRead)
        
    def openFile(self):
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl(self.outFile.fileName()))
        
    def openDirectory(self):
        desktopService = QDesktopServices()
        fileInfo = QFileInfo(QFile(self.outFile.fileName()))
        directory = fileInfo.dir()
        desktopService.openUrl(QUrl(directory.path()))