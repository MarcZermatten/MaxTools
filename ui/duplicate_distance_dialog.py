# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2016-04-05
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

from qgis.PyQt.QtWidgets import (QDialog, QGridLayout, QPushButton, QCheckBox, QLabel, QLineEdit, QRadioButton, QButtonGroup, QVBoxLayout, QSpacerItem, QSizePolicy)
from qgis.PyQt.QtGui import QDoubleValidator
from qgis.PyQt.QtCore import QCoreApplication

from .theme import apply_theme, add_geomind_footer, style_accent_button


class DuplicateDistanceDialog(QDialog):
    """
    Dialog class to choose the duplicate distance
    """

    def __init__(self, isComplexPolygon):
        """
        Constructor
        :param isComplexPolygon: for a polygon, if it has interior ring(s)
        """
        QDialog.__init__(self)
        self.setWindowTitle(QCoreApplication.translate("MaxTools", "Duplicate"))
        self.resize(320, 140)

        # Apply dark neon theme
        apply_theme(self)
        self.__distanceLabel = QLabel(QCoreApplication.translate("MaxTools", "distance :"))
        self.__distanceLabel.setMinimumHeight(20)
        self.__distanceLabel.setMinimumWidth(50)

        self.__distanceEdit = QLineEdit("inputMask")
        self.__distanceEdit.setMinimumHeight(20)
        self.__distanceEdit.setMinimumWidth(120)
        self.__distanceEdit.setValidator(QDoubleValidator(-1000, 1000, 4, self))

        self.__distanceDirection = QCheckBox(QCoreApplication.translate("MaxTools", "invert direction"))

        self.__previewButton = QPushButton(QCoreApplication.translate("MaxTools", "Preview"))
        self.__previewButton.setMinimumHeight(20)
        self.__previewButton.setMinimumWidth(100)

        self.__okButton = QPushButton(QCoreApplication.translate("MaxTools", "OK"))
        self.__okButton.setMinimumHeight(20)
        self.__okButton.setMinimumWidth(100)

        self.__cancelButton = QPushButton(QCoreApplication.translate("MaxTools", "Cancel"))
        self.__cancelButton.setMinimumHeight(20)
        self.__cancelButton.setMinimumWidth(100)

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__distanceLabel, 0, 0)
        self.__layout.addWidget(self.__distanceEdit, 0, 1)
        self.__layout.addWidget(self.__distanceDirection, 0, 2)

        if isComplexPolygon:
            self.__polygonLabel = QLabel(
                QCoreApplication.translate("MaxTools", "In which direction the internal part has to be duplicated ?"))
            self.__polygonLabel.setMinimumHeight(20)
            self.__polygonLabel.setMinimumWidth(50)
            self.__layout.addWidget(self.__polygonLabel, 1, 0, 1, 3)

            self.__directions = [QRadioButton(QCoreApplication.translate("MaxTools", "same")),
                                 QRadioButton(QCoreApplication.translate("MaxTools", "opposite"))]
            self.__directions[0].setChecked(True)
            self.__direction_button_group = QButtonGroup()
            for i in range(len(self.__directions)):
                self.__layout.addWidget(self.__directions[i], 2, i+1)
                self.__direction_button_group.addButton(self.__directions[i], i)

        self.__layout.addWidget(self.__previewButton, 3, 0)
        self.__layout.addWidget(self.__okButton, 3, 1)
        self.__layout.addWidget(self.__cancelButton, 3, 2)

        # Style OK button as primary
        style_accent_button(self.__okButton)

        self.setLayout(self.__layout)

        # Add GeoMind footer
        add_geomind_footer(self)

    def previewButton(self):
        """
        To get the preview button instance
        :return: preview button instance
        """
        return self.__previewButton

    def okButton(self):
        """
        To get the ok button instance
        :return: ok button instance
        """
        return self.__okButton

    def cancelButton(self):
        """
        To get the cancel button instance
        :return: cancel button instance
        """
        return self.__cancelButton

    def distanceEdit(self):
        """
        To get the distance edit widget
        :return: distance edit widget
        """
        return self.__distanceEdit

    def directionCheck(self):
        """
        To get the direction check button
        :return: direction check button
        """
        return self.__distanceDirection

    def isInverted(self):
        """
        To get if the user want a complex polygon duplication inverted or not
        :return: true if inverted, false otherwise
        """
        return self.__direction_button_group.checkedId() == 1
