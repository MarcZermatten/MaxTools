#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des problèmes d'imports résiduels
Auteur: GeoMind
Date: 2025-12-19
"""

import os
import re

def fix_profile_dock_widget():
    """Fix profile_dock_widget.py specifically"""
    filepath = 'ui/profile_dock_widget.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix malformed QtCore import
    content = re.sub(
        r'from qgis\.PyQt\.QtCore import \(QSize,\s+QRectF,\s+QCoreApplication,\s+Qt,\s+pyqtSignal\)',
        'from qgis.PyQt.QtCore import (QSize, QRectF, QCoreApplication, Qt, pyqtSignal)',
        content
    )

    # Fix broken Qwt5 try/except block
    pattern = r'try:\n# Qwt5 not available.*?\n.*?QwtPlotCurve\)\n    Qwt5_loaded = False.*?\nexcept ImportError:\n    Qwt5_loaded = False'
    replacement = '''# Qwt5 not available in QGIS 3.x - using matplotlib instead
Qwt5_loaded = False'''
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Add urllib import if missing
    if 'from urllib.error import HTTPError, URLError' not in content:
        # Find the right place to add it (after qgis imports, before other imports)
        content = content.replace(
            'from ..core.signal import Signal',
            'from urllib.error import HTTPError, URLError\nfrom ..core.signal import Signal'
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {filepath}")

def fix_show_settings_dialog():
    """Fix show_settings_dialog.py specifically"""
    filepath = 'ui/show_settings_dialog.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix malformed core import
    pattern = r'from qgis\.core import Qgis, \(QgsMapLayer,\s+QgsWKBTypes,\s+QgsMapLayerRegistry,\s+QGis\)'
    replacement = 'from qgis.core import (Qgis, QgsMapLayer, QgsWKBTypes, QgsProject)'
    content = re.sub(pattern, replacement, content)

    # Remove QGis import if still present
    content = content.replace('QGis)', '')

    # Ensure QgsProject import
    if 'QgsProject' not in content.split('from qgis.core import')[1].split('\n')[0]:
        content = re.sub(
            r'from qgis\.core import \(([^)]+)\)',
            lambda m: f"from qgis.core import ({m.group(1)}, QgsProject)" if 'QgsProject' not in m.group(1) else m.group(0),
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {filepath}")

def general_cleanup():
    """Clean up common issues in all UI files"""
    ui_dir = 'ui'
    for filename in os.listdir(ui_dir):
        if not filename.endswith('.py') or filename == '__init__.py':
            continue

        filepath = os.path.join(ui_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Remove orphan QGis) or URLError) lines
        content = re.sub(r'^\s*(QGis\)|URLError\))\s*$', '', content, flags=re.MULTILINE)

        # Fix double empty lines
        content = re.sub(r'\n\n\n+', '\n\n', content)

        # Fix QtCore imports with too much whitespace
        content = re.sub(
            r'from qgis\.PyQt\.QtCore import \(([^)]+)\)',
            lambda m: f"from qgis.PyQt.QtCore import ({', '.join([x.strip() for x in re.split(r'[,\s]+', m.group(1)) if x.strip()])})",
            content
        )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned: {filename}")

if __name__ == '__main__':
    print("Fixing specific files with known issues...")

    try:
        fix_profile_dock_widget()
    except Exception as e:
        print(f"Error fixing profile_dock_widget.py: {e}")

    try:
        fix_show_settings_dialog()
    except Exception as e:
        print(f"Error fixing show_settings_dialog.py: {e}")

    print("\nGeneral cleanup...")
    general_cleanup()

    print("\nDone!")
