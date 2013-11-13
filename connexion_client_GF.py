# -*- coding: utf-8 -*- 
'''
Created on 11 nov. 2013

@author: etienne
'''

import urllib2, base64
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from exception import LoginException, NoResult

class ConnexionClientGF:

    def __init__(self, login, password, zone, url = "https://api-geofoncier.brgm-rec.fr/"):
        
        zonesDisponibles = ("metropole", "antilles", "guyane", "reunion", "mayotte")
        if zone not in zonesDisponibles:
            raise Exception, "Zone non disponible" 
        
        self.authentification = self.createLogin(login, password)
        self.zone = zone
        self.url = url
    
    def createLogin(self,login,password):
        base64string = base64.encodestring('%s:%s' % (login, password))
        return "Basic %s" % base64string

    def getExternalLink(self,url):
        desktopService = QDesktopServices()
        desktopService.openUrl(QUrl(self.url+url))

    def get(self, composante):
        url = self.url+composante
        req = urllib2.Request(url)
        authheader = self.authentification

        req.add_header("Authorization", authheader)

        try:
            print u"Requête HTTPS en cours"
            print url
            res = urllib2.urlopen(req)
            #headers = res.info().headers
            data = res.read()
            print u"Fin requête HTTPS"
            return data
        except urllib2.HTTPError as e:
            if e.code == 401:
                raise LoginException, "Wrong login/password"
            if e.code == 400:
                raise NoResult, "No Result"
            raise e
        except IOError, e:
            raise e
            
    def getListeDossiers(self):
        return self.get("clientsge/dossiers?output=csv&zone="+self.zone)