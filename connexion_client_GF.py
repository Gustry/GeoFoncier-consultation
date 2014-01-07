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
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import urllib2, base64
from Saver import Saver
from exception import LoginException, NoResultException

class ConnexionClientGF:
    """Classe client GéoFoncier"""

    def __init__(self, login, password, zone):
        """
        Constructeur d'une connexion client
        
        @type login: str
        @param login: Compte utilisateur
        @type password:str
        @param password: Mot de passe
        @type zone: str
        @param zone: Zone de l'utilisateur
        """
        if zone not in ("metropole", "antilles", "guyane", "reunion", "mayotte"):
            raise Exception, "Zone non disponible"
        
        self.__login = login
        self.__password = password
        self.__authentification = self.__createLogin(login, password)
        self.__zone = zone
        self.__url = self.__getURLAPI(login, password)
    
    def __getURLAPI(self,login, password):
        """
        Fonction privée pour obtenir l'URL de l'API entre la recette et production
        
        @type login: str
        @param login: Compte utilisateur
        @type password:str
        @param password: Mot de passe
        @rtype: str
        @return: URL
        """
        if login == "clientge" and password == "clientge":
            return "https://api-geofoncier.brgm-rec.fr/clientsge/"
        else:
            return "https://api.geofoncier.fr/clientsge/"
            
    def __createLogin(self,login,password):
        """
        Fonction privée pour obtenir le header d'authentification HTTP
        
        @type login: str
        @param login: Compte utilisateur
        @type password:str
        @param password: Mot de passe
        @rtype: str
        @return: Authentification header
        """
        base64string = base64.encodestring('%s:%s' % (login, password))
        return "Basic %s" % base64string
    
    def getAndSaveExternalDocument(self,ui,component,nameFile):
        """
        Fonction de téléchargement et d'enregistrement d'un fichier qui se trouve sur internet
        
        @type ui:UI
        @param ui: Interface graphique
        @type component:str
        @param component: URL de la composante
        @param nameFile: str
        @param nameFile: Nom du fichier
        """
        Saver(self.__login,self.__password,self.__url+component,nameFile,ui)

    def get(self, composante):
        """
        Fonction de téléchargement de données
        
        @type composante:str
        @param composante: URL de la ressource à télécharger
        @rtype: str
        @return: Les données
        """
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
                raise NoResultException, "No Result"
            raise e
        except IOError, e:
            raise e
            
    def getURLListeDossiers(self,formatOutput):
        """
        URL de la liste des dossiers du client
        
        @type formatOutput:str
        @param formatOutput: "Format de sortie"
        @rtype: str
        @return: URL
        """
        if formatOutput == "csv":
            return "dossiers?output=csv&zone="+self.__zone
        elif formatOutput == "kml":
            return "dossiers?output=kml&zone="+self.__zone
        else:
            return "dossiers?zone="+self.__zone
        
    def getListeDossiers(self,formatOutput="csv"):
        """
        Liste des dossiers du client
        
        @type formatOutput:str
        @param formatOutput: "Format de sortie"
        @rtype: str
        @return: Les données
        """
        return self.get(self.getURLListeDossiers(formatOutput))
    
    def getURL(self,url):
        return self.__url+url