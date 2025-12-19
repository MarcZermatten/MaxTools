# -*- coding: utf-8 -*-
"""
Icon path utilities for MaxTools plugin.
Uses direct file paths instead of Qt resources for better compatibility.
"""

import os

# Plugin root directory
PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(PLUGIN_DIR, 'icons')


def get_icon_path(icon_name):
    """
    Get the absolute path to an icon file.

    Args:
        icon_name: Name of the icon file (e.g., 'duplicate_icon.png')

    Returns:
        Absolute path to the icon file
    """
    return os.path.join(ICONS_DIR, icon_name)
