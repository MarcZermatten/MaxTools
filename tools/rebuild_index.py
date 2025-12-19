# -*- coding: utf-8 -*-
# Migrated to QGIS 3.x by GeoMind (2025)
"""
/***************************************************************************
 MaxTools
                                 A QGIS plugin for the Max Francken
                              -------------------
        begin                : 2019-11-05
        git sha              : $Format:%H$
        copyright            : (C) 2019 Max Francken
        author               : Ingénierie Informatique Gusthiot, Max Francken
        email                : i2g@gusthiot.ch
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QProgressBar, QPushButton, QProgressDialog


class RebuildIndex(object):
    """
    Tool class to rebuild the indexation
    """

    def __init__(self, iface):
        """
        Constructor
        :param iface: interface
        """
        self.__iface = iface
        self.icon_path = ':/plugins/MaxTools/icons/rebuild_icon.png'
        self.text = QCoreApplication.translate("MaxTools", "Rebuild Index")
        self.killed = False

    def start(self):
        """
        To start the rebuild
        """
        snap_util = self.__iface.mapCanvas().snappingUtils()
        extent = self.__iface.mapCanvas().extent()
        self.__progressDialog = QProgressDialog()
        self.__progressDialog.setWindowTitle(QCoreApplication.translate("MaxTools", "Rebuild Index..."))
        self.__progressDialog.setLabelText(QCoreApplication.translate("MaxTools", "Percentage of indexed layers"))
        progressBar = QProgressBar(self.__progressDialog)
        progressBar.setTextVisible(True)
        cancelButton = QPushButton()
        cancelButton.setText(QCoreApplication.translate("MaxTools", "Cancel"))
        cancelButton.clicked.connect(self.kill)
        self.__progressDialog.setBar(progressBar)
        self.__progressDialog.setCancelButton(cancelButton)
        self.__progressDialog.setMinimumWidth(300)
        self.__progressDialog.show()

        lcs_list = snap_util.layers()
        step = 0
        self.killed = False
        for lc in lcs_list:
            if self.killed:
                break
            locator = snap_util.locatorForLayer(lc.layer)
            if locator.extent() is not None:
                txt = locator.extent().toString()
            else:
                txt = "None"
            print("old extent : " + txt)
            print("new extent : " + extent.toString())
            locator.setExtent(extent)
            if not locator.hasIndex():
                locator.init()
            else:
                locator.rebuildIndex()
            locator.setExtent(None)
            progressBar.setValue(100 * step / len(lcs_list))
            step += 1
        self.__progressDialog.close()

    def kill(self):
        """
        To stop the rebuild at the end of the current working layer
        """
        self.killed = True
