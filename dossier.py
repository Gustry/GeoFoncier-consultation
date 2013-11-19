'''
Created on 11 nov. 2013

@author: etienne
'''
import StringIO, csv
import xml.etree.ElementTree as ET
from exception import ErreurDossier

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
    
    def __init__(self,url,structure_ge,reference,nom_commune,insee_commune,date,document = [],geometrie_kml = None):
        self.id = self.getID(url)
        self.structure_ge = structure_ge
        self.reference = reference
        self.nom_commune = nom_commune
        self.insee_commune = insee_commune
        self.date = date
        self.geometrie_kml = geometrie_kml
        self.document = document
        
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
    
    def getDocuments(self):
        return self.document
    
    def loadDetails(self,data):
        tree = ET.parse(StringIO.StringIO(data))
        root = tree.getroot()
        for child in root[0]:
            
            if child.tag == "id" and child.text != self.id:
                raise ErreurDossier, "Erreur dossier"
            
            if child.tag == "geometrie_kml":
                print child[0]
                
            if child.tag == "document":
                self.document.append(child[0].attrib["href"])
