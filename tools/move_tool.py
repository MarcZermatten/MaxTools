# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2016-07-12
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
from qgis.PyQt.QtCore import (Qt,
                          QCoreApplication)
from qgis.PyQt.QtGui import QColor, QMoveEvent
from qgis.core import (QgsPoint,
                       QgsPointXY,
                       QgsEditFormConfig,
                       QgsSnappingUtils,
                       QgsTolerance,
                       QgsPointLocator,
                       QgsLineString,
                       QgsCircularString,
                       QgsCompoundCurve,
                       QgsDataSourceUri,
                       QgsFeature,
                       QgsCurvePolygon,
                       Qgis,
                       QgsGeometry,
                       QgsMapLayer)
from qgis.gui import (QgsMapToolAdvancedDigitizing,
                      QgsRubberBand,
                      QgsMessageBar)
from ..ui.move_confirm_dialog import MoveConfirmDialog
from ..core.finder import Finder
from ..core.geometry_v2 import GeometryV2
from ..core.signal import Signal


class MoveTool(QgsMapToolAdvancedDigitizing):
    """
    Map tool class to move or copy an object
    """

    def __init__(self, iface):
        """
        Constructor
        :param iface: interface
        """
        QgsMapToolAdvancedDigitizing.__init__(self,  iface.mapCanvas(), iface.cadDockWidget())
        self.__iface = iface
        from ..core.icons import get_icon_path
        self.icon_path = get_icon_path('move_icon.png')
        self.text = QCoreApplication.translate("MaxTools", "Move/Copy a feature")
        self.setCursor(Qt.ArrowCursor)
        self.__isEditing = False
        self.__findVertex = False
        self.__onMove = False
        self.__layer = None
        self.__confDlg = None
        self.__lastFeatureId = None
        self.__selectedFeature = None
        self.__rubberBand = None
        self.__rubberSnap = None
        self.__newFeature = None
        self.__selectedVertex = None

    def activate(self):
        """
        When the action is selected
        """
        QgsMapToolAdvancedDigitizing.activate(self)
        if self.__layer.geometryType() == Qgis.GeometryType.Point:
            self.setMode(self.CaptureLine)
        else:
            self.setMode(self.CaptureNone)

    def deactivate(self):
        """
        When the action is deselected
        """
        self.__cancel()
        QgsMapToolAdvancedDigitizing.deactivate(self)

    def toolName(self):
        """
        To get the tool name
        :return: tool name
        """
        return QCoreApplication.translate("MaxTools", "Move/Copy")

    def startEditing(self):
        """
        To set the action as enable, as the layer is editable
        """
        self.action().setEnabled(True)
        Signal.safelyDisconnect(self.__layer.editingStarted, self.startEditing)
        self.__layer.editingStopped.connect(self.stopEditing)

    def stopEditing(self):
        """
        To set the action as disable, as the layer is not editable
        """
        self.action().setEnabled(False)
        Signal.safelyDisconnect(self.__layer.editingStopped, self.stopEditing)
        self.__layer.editingStarted.connect(self.startEditing)
        if self.canvas().mapTool() == self:
            self.__iface.actionPan().trigger()

    def setTool(self):
        """
        To set the current tool as this one
        """
        self.canvas().setMapTool(self)

    def __cancel(self):
        """
        To cancel used variables
        """
        if self.__rubberBand is not None:
            self.canvas().scene().removeItem(self.__rubberBand)
            self.__rubberBand.reset()
            self.__rubberBand = None
        if self.__rubberSnap is not None:
            self.canvas().scene().removeItem(self.__rubberSnap)
            self.__rubberSnap.reset()
            self.__rubberSnap = None
        self.__isEditing = False
        self.__findVertex = False
        self.__onMove = False
        self.__lastFeatureId = None
        self.__selectedFeature = None
        self.__confDlg = None
        self.__newFeature = None
        self.__selectedVertex = None
        # Only access layer if it exists
        if self.__layer is not None:
            self.__layer.removeSelection()
            # setMode only works when tool is active as map tool
            if self.canvas().mapTool() == self:
                if self.__layer.geometryType() == Qgis.GeometryType.Point:
                    self.setMode(self.CaptureLine)
                else:
                    self.setMode(self.CaptureNone)

    def __removeLayer(self):
        """
        To remove the current working layer
        """
        if self.__layer is not None:
            if self.__layer.isEditable():
                Signal.safelyDisconnect(self.__layer.editingStopped, self.stopEditing)
            else:
                Signal.safelyDisconnect(self.__layer.editingStarted, self.startEditing)
            self.__layer = None

    def setEnable(self, layer):
        """
        To check if we can enable the action for the selected layer
        :param layer: selected layer
        """
        if layer is not None and layer.type() == QgsMapLayer.VectorLayer:
            if layer == self.__layer:
                return

            if self.__layer is not None:
                if self.__layer.isEditable():
                    Signal.safelyDisconnect(self.__layer.editingStopped, self.stopEditing)
                else:
                    Signal.safelyDisconnect(self.__layer.editingStarted, self.startEditing)
            self.__layer = layer
            # Note: setMode is called in activate() when the tool becomes active
            # Calling it here before activation causes AttributeError

            if self.__layer.isEditable():
                self.action().setEnabled(True)
                self.__layer.editingStopped.connect(self.stopEditing)
            else:
                self.action().setEnabled(False)
                self.__layer.editingStarted.connect(self.startEditing)
                if self.canvas().mapTool() == self:
                    self.__iface.actionPan().trigger()
            return
        self.action().setEnabled(False)
        if self.canvas().mapTool() == self:
            self.__iface.actionPan().trigger()
        self.__removeLayer()

    def __pointPreview(self, point):
        """
        To create a point geometry preview (rubberBand)
        :param point: new position as mapPoint
        """
        point_v2 = GeometryV2.asPointV2(self.__selectedFeature.geometry(), self.__iface)
        self.__newFeature = QgsPoint(point.x(), point.y())
        self.__newFeature.addZValue(point_v2.z())
        self.__rubberBand = QgsRubberBand(self.canvas(), Qgis.GeometryType.Point)
        self.__rubberBand.setToGeometry(QgsGeometry(self.__newFeature.clone()), None)

    def __linePreview(self, point):
        """
        To create a line geometry preview (rubberBand)
        :param point: new position as mapPoint
        """
        line_v2, curved = GeometryV2.asLineV2(self.__selectedFeature.geometry(), self.__iface)
        vertex = QgsPoint()
        line_v2.pointAt(self.__selectedVertex, vertex)
        self.__rubberBand = QgsRubberBand(self.canvas(), Qgis.GeometryType.Line)
        dx = vertex.x() - point.x()
        dy = vertex.y() - point.y()
        if isinstance(curved, (list, tuple)):
            self.__newFeature = QgsCompoundCurve()
            for pos in range(line_v2.nCurves()):
                curve_v2 = self.__newCurve(curved[pos], line_v2.curveAt(pos), dx, dy)
                self.__newFeature.addCurve(curve_v2)
                if pos == 0:
                    self.__rubberBand.setToGeometry(QgsGeometry(curve_v2.curveToLine()), None)
                else:
                    self.__rubberBand.addGeometry(QgsGeometry(curve_v2.curveToLine()), None)
        else:
            self.__newFeature = self.__newCurve(curved, line_v2, dx, dy)
            self.__rubberBand.setToGeometry(QgsGeometry(self.__newFeature.curveToLine()), None)

    @staticmethod
    def __newCurve(curved, line_v2, dx, dy):
        """
        To create a new moved line
        :param curved: if the line is curved
        :param line_v2: the original line
        :param dx: x translation
        :param dy: y translation
        :return: the new line
        """
        if curved:
            newCurve = QgsCircularString()
        else:
            newCurve = QgsLineString()
        points = []
        for pos in range(line_v2.numPoints()):
            x = line_v2.pointN(pos).x() - dx
            y = line_v2.pointN(pos).y() - dy
            pt = QgsPoint(x, y)
            pt.addZValue(line_v2.pointN(pos).z())
            points.append(pt)
        newCurve.setPoints(points)
        return newCurve

    def __polygonPreview(self, point):
        """
        To create a polygon geometry preview (rubberBand)
        :param point: new position as mapPoint
        """
        polygon_v2, curved = GeometryV2.asPolygonV2(self.__selectedFeature.geometry(), self.__iface)
        vertex = polygon_v2.vertexAt(GeometryV2.polygonVertexId(polygon_v2, self.__selectedVertex))
        dx = vertex.x() - point.x()
        dy = vertex.y() - point.y()
        self.__newFeature = QgsCurvePolygon()
        self.__rubberBand = QgsRubberBand(self.canvas(), Qgis.GeometryType.Line)
        line_v2 = self.__newCurve(curved[0], polygon_v2.exteriorRing(), dx, dy)
        self.__newFeature.setExteriorRing(line_v2)
        self.__rubberBand.setToGeometry(QgsGeometry(line_v2.curveToLine()), None)
        for num in range(polygon_v2.numInteriorRings()):
            line_v2 = self.__newCurve(curved[num+1], polygon_v2.interiorRing(num), dx, dy)
            self.__newFeature.addInteriorRing(line_v2)
            self.__rubberBand.addGeometry(QgsGeometry(line_v2.curveToLine()), None)

    def __onConfirmCancel(self):
        """
        When the Cancel button in Move Confirm Dialog is pushed
        """
        self.__confDlg.reject()

    def __onConfirmMove(self):
        """
        When the Move button in Move Confirm Dialog is pushed
        """
        geometry = QgsGeometry(self.__newFeature)
        if not geometry.isGeosValid():
            self.__iface.messageBar().pushMessage(
                QCoreApplication.translate("MaxTools", "Geos geometry problem"), level=Qgis.Critical, duration=0)
        self.__layer.changeGeometry(self.__selectedFeature.id(), geometry)
        self.__confDlg.accept()
        self.__cancel()

    def __onConfirmCopy(self):
        """
        When the Copy button in Move Confirm Dialog is pushed
        """
        geometry = QgsGeometry(self.__newFeature)
        if not geometry.isGeosValid():
            self.__iface.messageBar().pushMessage(
                QCoreApplication.translate("MaxTools", "Geos geometry problem"), level=Qgis.Critical, duration=0)
        feature = QgsFeature(self.__layer.fields())
        feature.setGeometry(geometry)
        primaryKey = QgsDataSourceUri(self.__layer.source()).keyColumn()
        for field in self.__selectedFeature.fields():
            if field.name() != primaryKey:
                feature.setAttribute(field.name(), self.__selectedFeature.attribute(field.name()))
        if len(self.__selectedFeature.fields()) > 0 and self.__layer.editFormConfig().suppress() != \
                Qgis.AttributeFormSuppression.On:
            self.__iface.openFeatureForm(self.__layer, feature)
        else:
            ok, outs = self.__layer.dataProvider().addFeatures([feature])
            self.__layer.updateExtents()
            self.__layer  # setCacheImage obsolete in QGIS 3
            self.__layer.triggerRepaint()
            self.__layer.featureAdded.emit(outs[0].id())  # emit signal so feature is added to snapping index

        self.__confDlg.accept()
        self.__cancel()

    def keyReleaseEvent(self, event):
        """
        When keyboard is pressed
        :param event: keyboard event
        """
        if event.key() == Qt.Key_Escape:
            self.__cancel()

    def cadCanvasMoveEvent(self, event):
        """
        When the mouse is moved
        :param event: mouse event
        """

        if type(event) == QMoveEvent:
            map_point = self.toMapCoordinates(event.pos())
        else:
            map_point = event.mapPoint()

        if not self.__isEditing and not self.__findVertex and not self.__onMove:
            laySettings = QgsSnappingUtils.LayerConfig(self.__layer, QgsPointLocator.All, 10,
                                                       QgsTolerance.Pixels)
            feat = Finder.findClosestFeatureAt(map_point, laySettings, self)
            if feat is not None and self.__lastFeatureId != feat.id():
                self.__lastFeatureId = feat.id()
                self.__layer.setSelectedFeatures([feat.id()])
            if feat is None:
                self.__layer.removeSelection()
                self.__lastFeatureId = None
        elif self.__findVertex:
            if self.__rubberBand is not None:
                self.__rubberBand.reset()
            closest = self.__selectedFeature.geometry().closestVertex(map_point)
            color = QColor("red")
            color.setAlphaF(0.78)
            self.__rubberBand.setColor(color)
            self.__rubberBand.setIcon(4)
            self.__rubberBand.setIconSize(20)
            self.__rubberBand.setToGeometry(QgsGeometry.fromPointXY(QgsPointXY(closest[0])), None)
        elif self.__onMove:
            if self.__rubberBand is not None:
                self.__rubberBand.reset()
            if self.__layer.geometryType() == Qgis.GeometryType.Polygon:
                self.__polygonPreview(map_point)
            elif self.__layer.geometryType() == Qgis.GeometryType.Line:
                self.__linePreview(map_point)
            else:
                self.__pointPreview(map_point)
            color = QColor("red")
            color.setAlphaF(0.78)
            self.__rubberBand.setColor(color)
            self.__rubberBand.setWidth(2)
            if self.__layer.geometryType() != Qgis.GeometryType.Point:
                self.__rubberBand.setLineStyle(Qt.DotLine)
            else:
                self.__rubberBand.setIcon(4)
                self.__rubberBand.setIconSize(8)
            if self.__rubberSnap is not None:
                self.__rubberSnap.reset()
            else:
                self.__rubberSnap = QgsRubberBand(self.canvas(), Qgis.GeometryType.Point)
            self.__rubberSnap.setColor(color)
            self.__rubberSnap.setWidth(2)
            self.__rubberSnap.setIconSize(20)
            match = Finder.snap(map_point, self.canvas())
            if match.hasVertex() or match.hasEdge():
                point = match.point()
                if match.hasVertex():
                    if match.layer():
                        self.__rubberSnap.setIcon(4)
                    else:
                        self.__rubberSnap.setIcon(1)
                if match.hasEdge():
                    intersection = Finder.snapCurvedIntersections(point, self.canvas(), self)
                    if intersection is not None:
                        self.__rubberSnap.setIcon(1)
                        point = intersection
                    else:
                        self.__rubberSnap.setIcon(3)
                self.__rubberSnap.setToGeometry(QgsGeometry.fromPointXY(QgsPointXY(point)), None)

    def cadCanvasReleaseEvent(self, event):
        """
        When the mouse is clicked
        :param event: mouse event
        """
        if not self.__isEditing and not self.__findVertex and not self.__onMove:
            found_features = self.__layer.selectedFeatures()
            if len(found_features) > 0:
                if len(found_features) > 1:
                    self.__iface.messageBar().pushMessage(
                        QCoreApplication.translate("MaxTools", "One feature at a time"), level=Qgis.Info)
                    return
                self.__selectedFeature = found_features[0]
                if self.__layer.geometryType() != Qgis.GeometryType.Point:
                    self.__iface.messageBar().pushMessage(
                        QCoreApplication.translate("MaxTools",
                                                   "Select vertex for moving (ESC to undo)"),
                        level=Qgis.Info, duration=3)
                    self.__findVertex = True
                    self.setMode(self.CaptureLine)
                    self.__rubberBand = QgsRubberBand(self.canvas(), Qgis.GeometryType.Point)
                else:
                    self.setMode(self.CaptureNone)
                    self.__onMove = True
        elif self.__findVertex:
            self.__findVertex = False
            self.setMode(self.CaptureNone)
            closest = self.__selectedFeature.geometry().closestVertex(event.mapPoint())
            self.__selectedVertex = closest[1]
            self.__onMove = True
        elif self.__onMove:
            self.__onMove = False
            mapPoint = event.mapPoint()
            match = Finder.snap(event.mapPoint(), self.canvas())
            if match.hasVertex() or match.hasEdge():
                mapPoint = match.point()
                if match.hasEdge():
                    intersection = Finder.snapCurvedIntersections(mapPoint, self.canvas(), self)
                    if intersection is not None:
                        mapPoint = intersection
            self.__isEditing = True
            if self.__rubberBand is not None:
                self.__rubberBand.reset()
            if self.__layer.geometryType() == Qgis.GeometryType.Polygon:
                self.__polygonPreview(mapPoint)
            elif self.__layer.geometryType() == Qgis.GeometryType.Line:
                self.__linePreview(mapPoint)
            else:
                self.__pointPreview(mapPoint)
            color = QColor("red")
            color.setAlphaF(0.78)
            self.__rubberBand.setColor(color)
            if self.__layer.geometryType() != Qgis.GeometryType.Point:
                self.__rubberBand.setWidth(2)
                self.__rubberBand.setLineStyle(Qt.DotLine)
            else:
                self.__rubberBand.setIcon(4)
                self.__rubberBand.setIconSize(20)
            self.__confDlg = MoveConfirmDialog()
            self.__confDlg.rejected.connect(self.__cancel)
            self.__confDlg.moveButton().clicked.connect(self.__onConfirmMove)
            self.__confDlg.copyButton().clicked.connect(self.__onConfirmCopy)
            self.__confDlg.cancelButton().clicked.connect(self.__onConfirmCancel)
            self.__confDlg.show()
