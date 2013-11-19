# -*- coding: utf-8 -*-
'''
Created on 11 nov. 2013

@author: etienne
'''
import StringIO, csv
import xml.etree.ElementTree as ET
from exception import ErreurDossier
from array import *

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
    
    def printDossiers(cls) :
        for i,dossier in enumerate(Dossier.listeDossiers):
            print str(i) + " " + str(dossier.id)
    printDossiers = classmethod(printDossiers)
    
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
    
    def getInformations(self):
        return [self.structure_ge, self.reference, self.nom_commune, self.insee_commune, self.date, self.id]
    
    def getURLArchiveZIP(self):
        return "clientsge/dossiers/"+self.id+".zip"
    
    def getURLDossier(self):
        return "clientsge/dossiers/"+self.id

    def getURLDocument(self,numDocument):
        return self.document[numDocument]
    
    def getDocuments(self):
        return self.document
    
    def getGeometrie(self):
        return self.geometrie_kml
    
    def getTypeOfDocument(self,idDocument):
        import re
        result = []
        resultat = re.search("^https://(api-geofoncier.brgm-rec.fr|api.geofoncier.fr)/[a-z]*/documents/mFR_[a-zA-Z0-9]{11}_[a-zA-Z0-9 ]*_(\d[A-Z][A-Z][a-z])_(\d)$",self.document[idDocument])
        if resultat:
            type = resultat.group(2)
            if type == "1PVa":
                    result.append("Procès-verbal avec plan foncier ou croquis")
            elif type == "1PVb":
                    result.append("Procès-verbal seul")
            elif type == "1PVc":
                    result.append("Procès-verbal de carence avec plan foncier ou croquis")
            elif type == "1PVd":
                    result.append("Procès-verbal de carence seul")
            elif type == "2PLa":
                    result.append("Plan foncier")
            elif type == "2PLb":
                    result.append("Croquis foncier")
            elif type == "2PLc":
                    result.append("Plan autre que foncier")
            elif type == "2PLd":
                    result.append("Croquis autre que foncier")
            elif type == "2PLe":
                    result.append("Esquisse")
            elif type == "3AMa":
                    result.append("Croquis de conservation Alsace-Moselle")
            elif type == "5COa":
                    result.append("Règlement de copropriété")
            elif type == "5COb":
                    result.append("Etat descriptif de division")
            elif type == "6CAa":
                    result.append("Extrait cadastral")
            elif type == "6CAb":
                    result.append("DMPC / DA")
            elif type == "7POa":
                    result.append("Pouvoir")
            elif type ==  "7POb":
                    result.append("Courrier")
            elif type == "8PHa":
                    result.append("Photographie")
            elif type == "9DIa":
                    result.append("Plan de situation")
            elif type ==  "9DIz":
                    result.append("Autre document")
            else:
                    print "erreur de doc"
                    
            result.append(resultat.group(3))            
        return result
    
    def loadDetails(self,data):
        tree = ET.parse(StringIO.StringIO(data))
        root = tree.getroot()
        for child in root[0]:
            
            if child.tag == "id" and child.text != self.id:
                raise ErreurDossier, "Erreur dossier"
            
            if child.tag == "geometrie_kml":
                self.geometrie_kml = "dossier en memoire"
                
            if child.tag == "document":
                self.document.append(child[0].attrib["href"])
