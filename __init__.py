# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoFoncierConsultation
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
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load GeoFoncierConsultation class from file GeoFoncierConsultation
    from geofoncierconsultation import GeoFoncierConsultation
    return GeoFoncierConsultation(iface)
