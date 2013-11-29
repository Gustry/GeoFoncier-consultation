# -*- coding: utf-8 -*-
'''
Created on 28 nov. 2013

@author: etienne
'''


class Document:
    
    def __init__(self,description, fichier, type, territoire):
        self.description = description
        self.fichier = fichier
        self.type = type
        self.territoire = territoire
        
    def getDescription(self):
        return self.description
    
    def getURL(self):
        return("documents/fichier/"+self.territoire+self.fichier)