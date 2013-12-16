# -*- coding: utf-8 -*-
'''
Created on 28 nov. 2013

@author: etienne
'''

class Document:
    """Classe Document"""
    
    def __init__(self,identifiant, description, extension):
        """
        Constructeur de document
        @type identifiant: string
        @param identifiant: identifiant du fichier
        @type description: string
        @param description: description du fichier
        @type extension: string
        @param extension: extension du fichier
        """
        self.__identifiant = identifiant
        self.__description = description
        self.__extension = extension
        
    def getDescription(self):
        """
        Accesseur description
        @rtype: string
        @return: description
        """
        return self.__description
    
    def getFileName(self):
        """
        Accesseur nom du fichier
        @rtype: string
        @return: nom de fichier
        """
        return self.__identifiant
    
    def getExtension(self):
        """
        Accesseur de l'extension
        @rtype: string
        @return: extension
        """
        return self.__extension
    
    def getURL(self):
        """
        URL composante du document
        @rtype: string
        @return: URL composante
        """
        return("documents/fichier/"+self.__identifiant)