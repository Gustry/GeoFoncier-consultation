# -*- coding: utf-8 -*-
'''
Created on 3 déc. 2013

@author: etienne
'''

from osgeo import ogr
import tempfile

class KML:
    
    def __init__(self,kml):
        self.kml = kml
        self.geometries = list()
        
    
    def getGeometries(self):
        
        #Création d'un fichier temporaire
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".kml")
        tf.write(self.kml)
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
        if geom.GetGeometryType() != 1 and geom.GetGeometryType() != 2 and geom.GetGeometryType() != 3 :
            self.explodeMultiGeometry(geom)
        else:
            self.geometries.append(geom.exportToWkt())

        return self.geometries
    
    def explodeMultiGeometry(self,multigeom) :
        #explosion de la multigeom
        for i in range(0, multigeom.GetGeometryCount()):
            geom = multigeom.GetGeometryRef(i)
            if geom.GetGeometryType() == 1 or geom.GetGeometryType() == 2 or geom.GetGeometryType() == 3 :
                #print geom.__class__.__name__
                self.geometries.append(geom.ExportToWkt())
            else:
                self.explodeMultiGeometry(geom)