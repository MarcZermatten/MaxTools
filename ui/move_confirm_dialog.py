# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2016-07-13
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

from qgis.PyQt.QtWidgets import (QDialog, QGridLayout, QPushButton, QLabel)
from qgis.PyQt.QtCore import QCoreApplication

from .theme import apply_theme, add_geomind_footer, style_accent_button


class MoveConfirmDialog(QDialog):
    """
    Dialog class ton confirm the move or copy
    """

    def __init__(self):
        """
        Constructor
        """
        QDialog.__init__(self)
        apply_theme(self)
        self.setWindowTitle(QCoreApplication.translate("MaxTools", "Move/Copy Confirmation"))
        self.resize(300, 100)
        self.__layout = QGridLayout()

        self.__confirmLabel = QLabel(
            QCoreApplication.translate("MaxTools", "Would you like to move or to copy this feature ?"))

        self.__layout.addWidget(self.__confirmLabel, 0, 0, 1, 3)

        self.__moveButton = QPushButton(QCoreApplication.translate("MaxTools", "Move"))
        self.__moveButton.setMinimumHeight(20)
        self.__moveButton.setMinimumWidth(100)

        self.__copyButton = QPushButton(QCoreApplication.translate("MaxTools", "Copy"))
        self.__copyButton.setMinimumHeight(20)
        self.__copyButton.setMinimumWidth(100)

        self.__cancelButton = QPushButton(QCoreApplication.translate("MaxTools", "Cancel"))
        self.__cancelButton.setMinimumHeight(20)
        self.__cancelButton.setMinimumWidth(100)

        self.__layout.addWidget(self.__moveButton, 1, 0)
        self.__layout.addWidget(self.__copyButton, 1, 1)
        self.__layout.addWidget(self.__cancelButton, 1, 2)

        self.setLayout(self.__layout)

    def moveButton(self):
        """
        To get the move button instance
        :return: move button instance
        """
        return self.__moveButton

    def copyButton(self):
        """
        To get the cpoy button instance
        :return: cpoy button instance
        """
        return self.__copyButton

    def cancelButton(self):
        """
        To get the cancel button instance
        :return: cancel button instance
        """
        return self.__cancelButton
