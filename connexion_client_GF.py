# -*- coding: utf-8 -*- 
'''
Created on 11 nov. 2013

@author: etienne
'''

import urllib2, base64
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Downloader import Downloader
from exception import LoginException, NoResult
from PyQt4 import QtNetwork

class ConnexionClientGF:

    def __init__(self, login, password, zone):
        
        zonesDisponibles = ("metropole", "antilles", "guyane", "reunion", "mayotte")
        if zone not in zonesDisponibles:
            raise Exception, "Zone non disponible" 
        self.login = login
        self.password = password
        self.authentification = self.createLogin(login, password)
        self.qauthentification = QtNetwork.QAuthenticator()
        self.qauthentification.setUser(login)
        self.qauthentification.setPassword(password)
        self.zone = zone
        self.url = self.getURLAPI(login, password)
    
    def getURLAPI(self,login, password):
        if login == "clientge" and password == "clientge":
            return "https://api-geofoncier.brgm-rec.fr/clientsge/"
        else:
            return "https://api.geofoncier.fr/clientsge/"
            
    def createLogin(self,login,password):
        base64string = base64.encodestring('%s:%s' % (login, password))
        return "Basic %s" % base64string

    def getQAuthenticator(self):
        return self.qauthentification
    
    def getAndSaveExternalDocument(self,ui,component,nameFile):
        Downloader(self.login,self.password,self.url+component,nameFile,ui)

    def getExternalLink(self,component):
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl(self.url+component))
    
    def getExternalURL(self,component):
        return self.url+component

    def get(self, composante):
        url = self.url+composante
        req = urllib2.Request(url)
        authheader = self.authentification

        req.add_header("Authorization", authheader)
        req.add_header = ('User-agent', 'QGIS_plugin_consultation')

        try:
            res = urllib2.urlopen(req)
            #headers = res.info().headers
            data = res.read()
            return data
        except urllib2.HTTPError as e:
            if e.code == 401:
                raise LoginException, "Wrong login/password"
            if e.code == 400:
                raise NoResult, "No Result"
            raise e
        except IOError, e:
            raise e
            
    def getURLListeDossiers(self,format):
        if format == "csv":
            return "dossiers?output=csv&zone="+self.zone
        elif format == "kml":
            return "dossiers?output=kml&zone="+self.zone
        else:
            return "dossiers?zone="+self.zone
        
    def getListeDossiers(self,format="csv"):
        return self.get(self.getURLListeDossiers(format))