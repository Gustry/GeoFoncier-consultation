# -*- coding: utf-8 -*-
'''
Created on 28 nov. 2013

@author: etienne
'''


class Document:
    
    def __init__(self,identifiant, description, extension):
        self.__identifiant = identifiant
        self.__description = description
        self.__extension = extension
        
    def getDescription(self):
        return self.__description
    
    def getFileName(self):
        return self.__identifiant+"."+self.__extension
    
    def getURL(self):
        return("documents/fichier/"+self.__identifiant)