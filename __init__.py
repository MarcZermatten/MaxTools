# -*- coding: utf-8 -*-
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MaxTools class from file MaxTools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .max_tools import MaxTools
    return MaxTools(iface)
