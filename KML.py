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
        self.__geometries = list()

    def getFullKML(self):
        kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark>'
        kml = kml + self.__kml
        kml = kml + '</Placemark></Document></kml>'
        return kml       
    
    def getGeometries(self):
        
        #Création d'un fichier temporaire
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".kml")
        tf.write(self.getFullKML())
        namefile = tf.name
        tf.flush()
        tf.close()
        
        #Ouverture du fichier avec OGR
        driver = ogr.GetDriverByName("kml")
        datasource = driver.Open(str(namefile))
        
        #print datasource.GetLayerCount()
        
        #Récuperation du layer
        layer = datasource.GetLayer()
        
        #print layer.GetFeatureCount()
        
        row = layer.GetNextFeature()
        geom = row.GetGeometryRef()
        
        #Test d'une multigeom
        if geom.GetGeometryType() != ogr.wkbPoint and geom.GetGeometryType() != ogr.wkbPolygon and geom.GetGeometryType() != ogr.wkbMultiPoint and geom.GetGeometryType() != ogr.wkbMultiPolygon:
            self.__explodeMultiGeometry(geom)
        else:
            self.__geometries.append(geom.ExportToWkt())

        return self.__geometries
    
    def __explodeMultiGeometry(self,multigeom) :
        #explosion de la multigeom
        for i in range(0, multigeom.GetGeometryCount()):
            geom = multigeom.GetGeometryRef(i)
            if geom.GetGeometryType() == ogr.wkbPoint or geom.GetGeometryType() == ogr.wkbMultiPoint or geom.GetGeometryType() == ogr.wkbPolygon or geom.GetGeometryType() == ogr.wkbMultiPolygon:
                self.__geometries.append(geom.ExportToWkt())
            else:
                self.__explodeMultiGeometry(geom)
