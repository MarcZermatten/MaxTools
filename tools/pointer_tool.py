# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2017-01-23
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
from qgis.core import (QgsWkbTypes,
                       QgsMapLayer,
                       QgsSnappingUtils,
                       QgsTolerance,
                       QgsPointLocator,
                       Qgis)
from qgis.gui import (QgsMapTool,
                      QgsMessageBar)
from qgis.PyQt.QtCore import (Qt,
                          QCoreApplication)
from qgis.PyQt.QtWidgets import QMessageBox
from ..core.finder import Finder


class PointerTool(QgsMapTool):
    """
    Tool class for making a line elevation profile
    """

    def __init__(self, iface):
        """
        Constructor
        :param iface: interface
        """
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.__iface = iface
        from ..core.icons import get_icon_path
        self.icon_path = get_icon_path('pointer_icon.png')
        self.text = QCoreApplication.translate("MaxTools", "Elevation pointer")
        self.setCursor(Qt.ArrowCursor)

    def setTool(self):
        """
        To set the current tool as this one
        """
        self.canvas().setMapTool(self)

    def canvasReleaseEvent(self, event):
        """
        When the mouse is clicked
        :param event: mouse event
        """
        types = [QgsWkbTypes.PointZ, QgsWkbTypes.LineStringZ, QgsWkbTypes.CircularStringZ, QgsWkbTypes.CompoundCurveZ,
                 QgsWkbTypes.CurvePolygonZ, QgsWkbTypes.PolygonZ]
        display = ""
        for layer in self.canvas().layers():
            if layer.type() == QgsMapLayer.VectorLayer and QgsWkbTypes.geometryType(layer.wkbType()) in types:
                layerConfig = QgsSnappingUtils.LayerConfig(layer, QgsPointLocator.Vertex, 10, QgsTolerance.Pixels)
                features = Finder.findFeaturesAt(event.mapPoint(), layerConfig, self)
                if len(features) > 0:
                    display += layer.name() + " : \n"
                    for f in features:
                        if f.geometry().type() == Qgis.GeometryType.Point:
                            alt = f.geometry().constGet().z()
                        elif f.geometry().type() == Qgis.GeometryType.Line:
                            closest = f.geometry().closestVertex(event.mapPoint())
                            alt = f.geometry().constGet().zAt(closest[1])
                        elif f.geometry().type() == Qgis.GeometryType.Polygon:
                            self.__iface.messageBar().pushMessage(
                                QCoreApplication.translate("MaxTools", "Polygon not yet implemented"),
                                level=Qgis.Warning)
                            continue
                        else:
                            continue
                        display += "    " + str(f.id()) + " | " + str(alt) + " m.\n"
        if display != "":
            QMessageBox.information(None, QCoreApplication.translate("MaxTools", "Id | Elevation"), display)
