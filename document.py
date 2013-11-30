# -*- coding: utf-8 -*-
'''
Created on 28 nov. 2013

@author: etienne
'''


class Document:
    
    def __init__(self,identifiant, description, extension):
        self.identifiant = identifiant
        self.description = description
        self.extension = extension
        
    def getDescription(self):
        return self.description
    
    def getFileName(self):
        return self.identifiant+"."+self.extension
    
    def getURL(self):
        return("documents/fichier/"+self.identifiant)