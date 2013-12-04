# -*- coding: utf-8 -*- 
'''
Created on 11 nov. 2013

@author: etienne
'''

import urllib2, base64
from Saver import Saver
from exception import LoginException, NoResult

class ConnexionClientGF:
    """Classe client GéoFoncier"""

    def __init__(self, login, password, zone):
        
        if zone not in ("metropole", "antilles", "guyane", "reunion", "mayotte"):
            raise Exception, "Zone non disponible"
        
        self.__login = login
        self.__password = password
        self.__authentification = self.__createLogin(login, password)
        self.__zone = zone
        self.__url = self.__getURLAPI(login, password)
    
    '''
    Private
    '''
    
    def __getURLAPI(self,login, password):
        """A private function to get baz.

        This really should have a full function definition, but I am too lazy.

        """
        if login == "clientge" and password == "clientge":
            return "https://api-geofoncier.brgm-rec.fr/clientsge/"
        else:
            return "https://api.geofoncier.fr/clientsge/"
            
    def __createLogin(self,login,password):
        base64string = base64.encodestring('%s:%s' % (login, password))
        return "Basic %s" % base64string
    
    '''
    Public
    '''
    def getAndSaveExternalDocument(self,ui,component,nameFile):
        Saver(self.__login,self.__password,self.__url+component,nameFile,ui)

    def get(self, composante):
        url = self.__url+composante
        req = urllib2.Request(url)
        authheader = self.__authentification

        req.add_header("Authorization", authheader)
        req.add_header = ('User-agent', 'QGIS_plugin_consultation')

        try:
            res = urllib2.urlopen(req)
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
            
    def getURLListeDossiers(self,formatOutput):
        if formatOutput == "csv":
            return "dossiers?output=csv&zone="+self.__zone
        elif formatOutput == "kml":
            return "dossiers?output=kml&zone="+self.__zone
        else:
            return "dossiers?zone="+self.__zone
        
    def getListeDossiers(self,formatOutput="csv"):
        return self.get(self.getURLListeDossiers(formatOutput))