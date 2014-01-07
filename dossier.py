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
import StringIO, csv
import xml.etree.ElementTree as ET
from exception import ErreurDossierException, ErreurAPIException
from document import Document
from KML import KML

class Dossier:
    """ Classe dossier"""
    
    """Variable de classe comportant la liste des dossiers"""
    __listeDossiers = []
    
    """Méthode statique pour charger les dossiers à partir du CSV"""
    def loadFromCSV(cls,csvString) :
        data = StringIO.StringIO(csvString)
        csvReader = csv.reader(data)

        for i,row in enumerate(csvReader):
            if i>=1:
                Dossier.__listeDossiers.append(Dossier(row[5], row[0], row[1], row[2], row[3], row[4]))
    loadFromCSV = classmethod(loadFromCSV)
    
    """Méthode statique pour obtenir le nombre de dossiers"""
    def getNbrDossiers(cls) :
        return len(Dossier.__listeDossiers)
    getNbrDossiers = classmethod(getNbrDossiers)
    
    """Méthode statique pour retourne un dossier"""
    def getDossier(cls,row) :
        return Dossier.__listeDossiers[row]
    getDossier = classmethod(getDossier)
    
    """Méthode statique qui retourne les dossiers"""
    def getListeDossiers(cls) :
        return Dossier.__listeDossiers
    getListeDossiers = classmethod(getListeDossiers)
    
    """Méthode statique qui vide la liste des dossiers"""
    def truncateDossier(cls) :
        del Dossier.__listeDossiers[:]
    truncateDossier = classmethod(truncateDossier)
    
    def __init__(self,url,structure_ge,reference,nom_commune,insee_commune,date,geometrie_kml = None):
        """Constructeur de dossier"""
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
        """Méthode qui permet de rajouter des informations à un dossier à partir du XML"""
        tree = ET.parse(StringIO.StringIO(data))
        root = tree.getroot()
        for child in root[0]:
            
            if child.tag == "id" and child.text != self.__id:
                raise ErreurDossierException, "Erreur dossier"
            
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
                    raise ErreurAPIException, "Changement de l'API"