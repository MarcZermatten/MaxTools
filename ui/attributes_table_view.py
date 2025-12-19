# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2017-11-30
        git sha              : $Format:%H$
        copyright            : (C) 2016 Max Francken
        author               : Max Francken
        email                : max.francken@lausanne.ch
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

from qgis.gui import QgsDualView, QgsAttributeEditorContext
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QMenu)


class AttributesTableView(QDialog):
    """
    AttributeTableView class to display filtered attributes table
    """

    def __init__(self, layer, canvas, request):
        """
        Constructor
        """
        QDialog.__init__(self)
        self.setWindowTitle(layer.name())
        self.__layout = QVBoxLayout()
        self.__menu = QMenu()
        for a in layer.actions().listActions():
            self.__menu.addAction(a)
        self.__layout.addWidget(self.__menu)
        self.__dual = QgsDualView()
        self.__context = QgsAttributeEditorContext()
        self.__dual.init(layer, canvas,request, self.__context)
        self.__dual.setView(QgsDualView.AttributeTable)
        self.__layout.addWidget(self.__dual)
        self.setLayout(self.__layout)
