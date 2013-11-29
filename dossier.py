# -*- coding: utf-8 -*-
'''
Created on 11 nov. 2013

@author: etienne
'''
import StringIO, csv, re
import xml.etree.ElementTree as ET
from exception import ErreurDossier, ErreurAPI
from document import Document

class Dossier:
    
    listeDossiers = []
    
    def loadFromCSV(cls,csvString) :
        data = StringIO.StringIO(csvString)
        csvReader = csv.reader(data)

        for i,row in enumerate(csvReader):
            if i>=1:
                Dossier.listeDossiers.append(Dossier(row[5], row[0], row[1], row[2], row[3], row[4]))
    loadFromCSV = classmethod(loadFromCSV)
    
    def getNbrDossiers(cls) :
        return len(Dossier.listeDossiers)
    getNbrDossiers = classmethod(getNbrDossiers)
    
    def getDossier(cls,row) :
        return Dossier.listeDossiers[row]
    getDossier = classmethod(getDossier)
    
    def __init__(self,url,structure_ge,reference,nom_commune,insee_commune,date,geometrie_kml = None):
        self.id = self.getID(url)
        self.structure_ge = structure_ge
        self.reference = reference
        self.nom_commune = nom_commune
        self.insee_commune = insee_commune
        self.date = date
        self.geometrie_kml = geometrie_kml
        self.document = list()
        
    def getID(self,url):
        element = url.split("/")
        zipFile = element[5].split(".")
        return zipFile[0]
    
    def getReference(self):
        return self.reference.replace("/","_")
    
    def getInformations(self):
        return [self.structure_ge, self.reference, self.nom_commune, self.insee_commune, self.date, self.id]
    
    def getURLArchiveZIP(self):
        return "dossiers/"+self.id+".zip"
    
    def getURLDossier(self):
        return "dossiers/"+self.id

    def getDocument(self,numDocument):
        return self.document[numDocument]
    
    def getDocuments(self):
        return self.document
    
    def getGeometrie(self):
        return self.geometrie_kml
    
    def loadDetails(self,data):
        tree = ET.parse(StringIO.StringIO(data))
        root = tree.getroot()
        for child in root[0]:
            
            if child.tag == "id" and child.text != self.id:
                raise ErreurDossier, "Erreur dossier"
            
            if child.tag == "geometrie_kml":
                self.geometrie_kml = "dossier en memoire"
                
            if child.tag == "document":
                if child[0].tag == "description" and child[1].tag == "fichier":
                    tab = child[1].text.split(".")
                    extension = tab[1]
                    tab = child[2].attrib["href"].split("/")
                    id = tab[5]
                    self.document.append(Document(id,child[0].text,extension))
                else:
                    raise ErreurAPI, "Changement de l'API"