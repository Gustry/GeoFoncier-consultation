# -*- coding: utf-8 -*-
'''
Created on 11 nov. 2013

@author: etienne
'''
import StringIO, csv
import xml.etree.ElementTree as ET
from exception import ErreurDossier, ErreurAPI
from document import Document
from KML import KML

class Dossier:
    
    __listeDossiers = []
    
    def loadFromCSV(cls,csvString) :
        data = StringIO.StringIO(csvString)
        csvReader = csv.reader(data)

        for i,row in enumerate(csvReader):
            if i>=1:
                Dossier.__listeDossiers.append(Dossier(row[5], row[0], row[1], row[2], row[3], row[4]))
    loadFromCSV = classmethod(loadFromCSV)
    
    def getNbrDossiers(cls) :
        return len(Dossier.__listeDossiers)
    getNbrDossiers = classmethod(getNbrDossiers)
    
    def getDossier(cls,row) :
        return Dossier.__listeDossiers[row]
    getDossier = classmethod(getDossier)
    
    def getListeDossiers(cls) :
        return Dossier.__listeDossiers
    getListeDossiers = classmethod(getListeDossiers)
    
    def truncateDossier(cls) :
        del Dossier.__listeDossiers[:]
    truncateDossier = classmethod(truncateDossier)
    
    def __init__(self,url,structure_ge,reference,nom_commune,insee_commune,date,geometrie_kml = None):
        self.__id = self.__getID(url)
        self.__structure_ge = structure_ge
        self.__reference = reference
        self.__nom_commune = nom_commune
        self.__insee_commune = insee_commune
        self.__date = date
        self.__document = list()
        if geometrie_kml != None:
            self.__geometrie_kml = KML(geometrie_kml)
        else:
            self.__geometrie_kml = None
        self.__envelope = None
        
        
    def __getID(self,url):
        element = url.split("/")
        zipFile = element[5].split(".")
        return zipFile[0]
    
    def getReference(self):
        return self.__reference.replace("/","_")
    
    def getInformations(self):
        return {"structure":self.__structure_ge, "reference":self.__reference, "nom_commune":self.__nom_commune, "insee_commune":self.__insee_commune,"date": self.__date, "id":self.__id}
    
    def getURLArchiveZIP(self):
        return "dossiers/"+self.__id+".zip"
    
    def getURLDossier(self):
        return "dossiers/"+self.__id
    
    def getGeometries(self):
        if self.__geometrie_kml == None:
            return None
        else:
            return self.__geometrie_kml.getGeometries()

    def getEnvelope(self):
        if self.__geometrie_kml == None:
            return None
        elif self.__envelope == None:
            self.__envelope = self.__geometrie_kml.getEnvelope()
            return self.__envelope
        else:
            return self.__envelope
    
    def getDocument(self,numDocument):
        return self.__document[numDocument]
    
    def getDocuments(self):
        return self.__document
    
    def loadDetails(self,data):
        tree = ET.parse(StringIO.StringIO(data))
        root = tree.getroot()
        for child in root[0]:
            
            if child.tag == "id" and child.text != self.__id:
                raise ErreurDossier, "Erreur dossier"
            
            if child.tag == "geometrie_kml":
                geometrie = ET.tostring(child)
                geometrie = geometrie.replace("<geometrie_kml>", '')
                geometrie = geometrie.replace("</geometrie_kml>", '')
                self.__geometrie_kml = KML(geometrie)
                
            if child.tag == "document":
                if child[0].tag == "description" and child[1].tag == "fichier":
                    tab = child[1].text.split(".")
                    extension = tab[1]
                    tab = child[2].attrib["href"].split("/")
                    id = tab[5]
                    self.__document.append(Document(id,child[0].text,extension))
                else:
                    raise ErreurAPI, "Changement de l'API"