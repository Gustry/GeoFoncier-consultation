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

class Document:
    """Classe Document"""
    
    def __init__(self,identifiant, description, extension):
        """
        Constructeur de document
        @type identifiant: string
        @param identifiant: identifiant du fichier
        @type description: string
        @param description: description du fichier
        @type extension: string
        @param extension: extension du fichier
        """
        self.__identifiant = identifiant
        self.__description = description
        self.__extension = extension
        
    def getDescription(self):
        """
        Accesseur description
        @rtype: string
        @return: description
        """
        return self.__description
    
    def getFileName(self):
        """
        Accesseur nom du fichier
        @rtype: string
        @return: nom de fichier
        """
        return self.__identifiant
    
    def getExtension(self):
        """
        Accesseur de l'extension
        @rtype: string
        @return: extension
        """
        return self.__extension
    
    def getURL(self):
        """
        URL composante du document
        @rtype: string
        @return: URL composante
        """
        return("documents/fichier/"+self.__identifiant)