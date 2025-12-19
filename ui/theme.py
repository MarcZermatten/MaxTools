# -*- coding: utf-8 -*-
"""
MaxTools Theme Module - Dark Neon Theme
Powered by GeoMind

Applies a modern dark theme with neon green accents to all MaxTools dialogs.
"""

import os
from qgis.PyQt.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget
from qgis.PyQt.QtGui import QPixmap, QFont
from qgis.PyQt.QtCore import Qt

# Theme colors
COLORS = {
    'background': '#1a1a1a',
    'background_alt': '#252525',
    'accent': '#00ff88',
    'accent_dark': '#00cc6a',
    'text': '#e0e0e0',
    'text_dim': '#888888',
    'border': '#404040'
}

def get_stylesheet():
    """Load and return the dark neon stylesheet."""
    style_path = os.path.join(os.path.dirname(__file__), 'styles', 'dark_neon.qss')
    try:
        with open(style_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def apply_theme(widget):
    """
    Apply the dark neon theme to a widget (usually a dialog).

    Usage in dialog __init__:
        from ..ui.theme import apply_theme
        apply_theme(self)
    """
    stylesheet = get_stylesheet()
    if stylesheet:
        widget.setStyleSheet(stylesheet)

def create_powered_by_label():
    """
    Create a discrete 'Powered by GeoMind' label.
    Returns a QLabel widget.
    """
    label = QLabel()
    label.setText('<span style="color: #555555; font-size: 8pt;">Powered by </span>'
                  '<span style="color: #00ff88; font-size: 8pt; font-weight: bold;">GeoMind</span>')
    label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
    label.setStyleSheet("background: transparent; padding: 2px;")
    return label

def create_header_with_logo(title, subtitle=None):
    """
    Create a header widget with GeoMind branding.

    Args:
        title: Main title text
        subtitle: Optional subtitle

    Returns:
        QWidget containing the styled header
    """
    header = QWidget()
    header.setStyleSheet(f"background-color: {COLORS['background_alt']}; border-radius: 6px; padding: 8px;")

    layout = QVBoxLayout(header)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(4)

    # Title
    title_label = QLabel(title)
    title_font = QFont()
    title_font.setPointSize(14)
    title_font.setBold(True)
    title_label.setFont(title_font)
    title_label.setStyleSheet(f"color: {COLORS['accent']}; background: transparent;")
    layout.addWidget(title_label)

    # Subtitle
    if subtitle:
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 9pt; background: transparent;")
        layout.addWidget(subtitle_label)

    return header

def add_geomind_footer(dialog):
    """
    Add a GeoMind footer to a dialog's layout.
    Call this at the end of dialog setup.

    Usage:
        from ..ui.theme import apply_theme, add_geomind_footer
        apply_theme(self)
        add_geomind_footer(self)
    """
    if dialog.layout():
        footer = create_powered_by_label()
        dialog.layout().addWidget(footer)

def style_accent_button(button):
    """
    Style a button as the primary/accent button.
    """
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: {COLORS['background']};
            border: none;
            border-radius: 4px;
            padding: 8px 20px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent_dark']};
        }}
        QPushButton:pressed {{
            background-color: #009955;
        }}
    """)

def style_danger_button(button):
    """
    Style a button as a danger/cancel button.
    """
    button.setStyleSheet("""
        QPushButton {
            background-color: #2a2a2a;
            color: #ff6b6b;
            border: 1px solid #ff6b6b;
            border-radius: 4px;
            padding: 8px 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ff6b6b;
            color: #1a1a1a;
        }
    """)
