# -*- coding: utf-8 -*- 
from PyQt4.QtCore import QUrl, QFileInfo, QFile, QIODevice
from PyQt4.QtGui import QFileDialog, QDialog, QProgressBar, QLabel, QPushButton, QDialogButtonBox, QVBoxLayout, QMessageBox, QDesktopServices
from PyQt4.QtNetwork import QHttp
from urlparse import urlparse, parse_qs

class Saver(QDialog):
    '''Classe qui permet d'enregistrer un fichier sur le disque'''
    
    def __init__(self, login, password, url, nameFile, parent = None):
        '''
        Constructeur
        @type login: String
        @param login: Compte utilisateur
        @type password: String
        @param password: Mot de passe utilisateur
        @type url:String
        @param url: URL de la ressource
        @type nameFile: String
        @param nameFile: Nom du fichier
        '''
        
        super(Saver, self).__init__(parent)
        
        self.url_to_download = url
        self.login = login
        self.password = password
        self.nameFile = nameFile
        
        #Création des parametres
        self.parameters = parse_qs(urlparse(url).query)
        
        self.httpGetId = 0
        self.requeteHTTPannule = False
        self.statusLabel = QLabel(u'Enregistrement %s' % self.url_to_download)
        self.closeButton = QPushButton("Fermer")
        self.closeButton.setAutoDefault(False)
        self.openFileButton = QPushButton("Ouvrir le fichier")
        self.openFileButton.setAutoDefault(False)
        self.openDirectoryButton = QPushButton(u"Ouvrir le répertoire")
        self.openDirectoryButton.setAutoDefault(False)
        self.progressBar = QProgressBar()

        #Gestion des boutons inférieurs
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.openFileButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.openDirectoryButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.closeButton, QDialogButtonBox.RejectRole)

        #Construction de l'objet QHTTP et mise en place des signaux/slots
        self.http = QHttp(self)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.closeButton.clicked.connect(self.cancelDownload)
        self.openDirectoryButton.clicked.connect(self.openDirectory)
        self.openFileButton.clicked.connect(self.openFile)

        #Construction de l'interface
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        #Création de la fenêtre et affichage
        self.setWindowTitle(u'Enregistrement')
        self.openFileButton.hide()
        self.openDirectoryButton.hide()
        self.show()
        
        #Lancement du téléchargement
        self.downloadFile()


    def downloadFile(self):
        url = QUrl(self.url_to_download)

        fileName = QFileDialog.getSaveFileName(self, "Enregistrer la liste des dossiers", self.nameFile, "conf")

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Erreur','Impossible d\'enregistrer le fichier %s: %s.' % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        #Création que la connexion HTTPS
        mode = QHttp.ConnectionModeHttps
        port = 0
        self.http.setHost(url.host(), mode, port)
        
        self.requeteHTTPannule = False
        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '/'

        #Concaténation des paramètres à l'URL
        path = path+("?")
        for item in url.queryItems():
            path = path + item[0] + "=" + item[1] + "&" 
        
        self.http.setUser(self.login, self.password)
        self.httpGetId = self.http.get(path, self.outFile)

    def cancelDownload(self):
        self.statusLabel.setText(u"Enregistrement annulé")
        self.requeteHTTPannule = True
        self.http.abort()
        self.close()

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.requeteHTTPannule:
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
            QMessageBox.information(self, 'Erreur','Le téléchargement a échoué : %s.' % self.http.errorString())

        self.statusLabel.setText('Enregistrement ok')
        self.openDirectoryButton.show()
        self.openFileButton.show()

    def readResponseHeader(self, responseHeader):
        '''Slot pour analyser les headers HTTP'''
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QMessageBox.information(self, 'Erreur','Le téléchargement a échoué : %s.' % responseHeader.reasonPhrase())
            self.requeteHTTPannule = True
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        '''Slot pour mettre à jour la barre de progression'''
        if self.requeteHTTPannule:
            return
        self.progressBar.setMaximum(totalBytes)
        self.progressBar.setValue(bytesRead)
        
    def openFile(self):
        '''Fonction permettant d'ouvrir le fichier'''
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl(self.outFile.fileName()))
        
    def openDirectory(self):
        '''Fonction permettant d'ouvrir le répertoire'''
        desktopService = QDesktopServices()
        fileInfo = QFileInfo(QFile(self.outFile.fileName()))
        directory = fileInfo.dir()
        desktopService.openUrl(QUrl(directory.path()))