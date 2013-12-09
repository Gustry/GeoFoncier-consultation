# -*- coding: utf-8 -*-
'''
Created on 3 déc. 2013

@author: etienne
'''

from osgeo import ogr
import tempfile

class KML:
    
    def __init__(self,kml):
        self.__kml = kml
        self.__pointGeometries = list()
        self.__polygonGeometries = list()
        self.__geometries = list()
        self.__envelope = list()
        self.__getGeometriesWKT()

    def getFullKML(self):
        kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>'
        kml = kml + self.__kml
        kml = kml + '</Placemark></Document></kml>'
        return kml
    
    def getEnvelope(self):
        return self.__envelope
    
    def getGeometries(self):
        return self.__geometries
    
    def __getGeometriesWKT(self):
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
        #explosion de la multigeom
        for i in range(0, multigeom.GetGeometryCount()):
            geom = multigeom.GetGeometryRef(i)
            if geom.GetGeometryType() == ogr.wkbPoint:
                self.__pointGeometries.append(geom)
            elif geom.GetGeometryType() == ogr.wkbPolygon or geom.GetGeometryType() == ogr.wkbMultiPolygon:
                self.__geometries.append(geom.ExportToWkt())
            else:
                self.__explodeMultiGeometry(geom)
