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

from osgeo import ogr
import tempfile

class KML:
    """Classe KML"""
    
    def __init__(self,kml):
        """Constructeur de d'objet KML"""
        self.__kml = kml
        self.__pointGeometries = list()
        self.__polygonGeometries = list()
        self.__geometries = list()
        self.__envelope = list()
        self.__getGeometriesWKT()

    def getFullKML(self):
        """Fonction pour obtenir le KML complet"""
        kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>'
        kml = kml + self.__kml
        kml = kml + '</Placemark></Document></kml>'
        return kml
    
    def getEnvelope(self):
        """Retourne un tableau comportant les coordonnées de la BBOX"""
        return self.__envelope
    
    def getGeometries(self):
        """Retourne un tableau comportant toutes les géoméries polygones et multipoints"""
        return self.__geometries
    
    def __getGeometriesWKT(self):
        """Fonction privé pour la lecture du KML via OGR et obtenir les géométries"""
        #Création d'un fichier temporaire
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".kml")
        tf.write(self.getFullKML())
        namefile = tf.name
        tf.flush()
        tf.close()
        
        #Ouverture du fichier avec OGR
        ogr.UseExceptions()
        driver = ogr.GetDriverByName("kml")
        datasource = driver.Open(namefile)
        #datasource = driver.Open("/home/etienne/Bureau/test_poly.kml")
        
        #Récuperation du layer
        layer = datasource.GetLayer()
        
        row = layer.GetNextFeature()
        geom = row.GetGeometryRef()
        
        self.__envelope = geom.GetEnvelope()
        
        #Test d'une multigeom
        if geom.GetGeometryType() != ogr.wkbPoint and geom.GetGeometryType() != ogr.wkbPolygon and geom.GetGeometryType() != ogr.wkbMultiPolygon:
            self.__explodeMultiGeometry(geom)
        elif geom.GetGeometryType() == ogr.wkbPoint:
            self.__pointGeometries.append(geom)
        elif geom.GetGeometryType() == ogr.wkbPolygon or geom.GetGeometryType() == ogr.wkbMultiPolygon:
            self.__geometries.append(geom.ExportToWkt())
        else:
            return "error"
        
        if len(self.__pointGeometries)>1:
            multipoint = ogr.Geometry(ogr.wkbMultiPoint)
            for i in range(0,len(self.__pointGeometries)):
                point = self.__pointGeometries[i]
                multipoint.AddGeometry(point)
            self.__geometries.append(multipoint.ExportToWkt())
        elif len(self.__pointGeometries)==1:
            self.__geometries.append(self.__pointGeometries[0].ExportToWkt())
    
    def __explodeMultiGeometry(self,multigeom) :
        """Fonction récursive privé pour exploser les multigéometries"""
        for i in range(0, multigeom.GetGeometryCount()):
            geom = multigeom.GetGeometryRef(i)
            if geom.GetGeometryType() == ogr.wkbPoint:
                self.__pointGeometries.append(geom)
            elif geom.GetGeometryType() == ogr.wkbPolygon or geom.GetGeometryType() == ogr.wkbMultiPolygon:
                self.__geometries.append(geom.ExportToWkt())
            else:
                self.__explodeMultiGeometry(geom)
