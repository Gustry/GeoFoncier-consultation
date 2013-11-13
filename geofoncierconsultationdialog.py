# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoFoncierConsultationDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_geofoncierconsultation import Ui_GeoFoncierConsultation
# create the dialog for zoom to point


class GeoFoncierConsultationDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_GeoFoncierConsultation()
        self.ui.setupUi(self)
