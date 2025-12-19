# -*- coding: utf-8 -*-
"""
MaxTools - Manuel d'utilisation
Généré avec le thème GeoMind
"""
import sys
sys.path.insert(0, r'C:\Users\zema\GeoBrain\scripts\python')

from geomind_pdf import (
    GeoMindDocTemplate, get_styles, create_table, create_metadata_table,
    create_separator, create_tip_box, create_warning_box, create_section_header,
    VERT_GEOMIND, CONTENT_WIDTH, format_date
)
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import cm
from reportlab.lib import colors
import os

OUTPUT_PATH = r"C:\Users\zema\GeoBrain\MaxTools\docs\MaxTools_Manuel_Utilisateur.pdf"

# Liste des outils avec descriptions détaillées
TOOLS = [
    {
        "name": "Duplicate",
        "icon": "duplicate_icon.png",
        "short": "Dupliquer une entité",
        "description": "Permet de dupliquer une entité (ligne ou polygone) à une distance définie. "
                      "L'outil crée une copie parallèle de la géométrie sélectionnée.",
        "usage": [
            "Sélectionner une couche ligne ou polygone en mode édition",
            "Cliquer sur l'entité à dupliquer",
            "Entrer la distance de décalage (positive ou négative)",
            "Valider pour créer la copie"
        ],
        "requires": "Couche ligne/polygone en mode édition"
    },
    {
        "name": "Move/Copy",
        "icon": "move_icon.png",
        "short": "Déplacer ou copier une entité",
        "description": "Permet de déplacer ou copier une entité vers un nouvel emplacement. "
                      "Supporte le sketching avancé (CAD) pour un positionnement précis.",
        "usage": [
            "Sélectionner une couche en mode édition",
            "Cliquer sur l'entité à déplacer",
            "Pour les lignes/polygones: sélectionner le vertex de référence",
            "Cliquer sur la nouvelle position (avec sketching si besoin)",
            "Choisir entre Déplacer ou Copier"
        ],
        "requires": "Couche vecteur en mode édition"
    },
    {
        "name": "Profile",
        "icon": "profile_icon.png",
        "short": "Profil d'une ligne",
        "description": "Affiche le profil en long d'une ligne sélectionnée. "
                      "Utilise les altitudes Z des vertices ou interroge un MNT configuré. "
                      "Permet de visualiser et modifier les points du profil.",
        "usage": [
            "Sélectionner une couche ligne",
            "Cliquer sur la ligne pour afficher son profil",
            "Utiliser le dock pour visualiser/éditer les points",
            "Double-clic sur un point pour le modifier"
        ],
        "requires": "Couche ligne (avec Z ou MNT configuré)"
    },
    {
        "name": "Sub-Profile (MNT)",
        "icon": "profile_2_icon.png",
        "short": "Ligne pour profil MNT",
        "description": "Permet de dessiner une ligne temporaire pour extraire un profil depuis le MNT. "
                      "Utile pour analyser le terrain sans créer d'entité permanente.",
        "usage": [
            "Configurer l'URL du MNT dans les paramètres",
            "Dessiner une ligne sur la carte",
            "Le profil s'affiche automatiquement"
        ],
        "requires": "MNT configuré dans les paramètres"
    },
    {
        "name": "Interpolate",
        "icon": "interpolate_icon.png",
        "short": "Interpoler l'altitude d'un vertex",
        "description": "Interpole l'altitude Z d'un point en fonction des points voisins sur une ligne. "
                      "Permet de corriger des altitudes manquantes ou erronées.",
        "usage": [
            "Sélectionner une couche point en mode édition",
            "Cliquer sur le point à interpoler",
            "Sélectionner les deux points de référence sur la ligne",
            "Valider l'interpolation"
        ],
        "requires": "Couche point en mode édition"
    },
    {
        "name": "Extrapolate",
        "icon": "extrapolate_icon.png",
        "short": "Extrapoler l'altitude",
        "description": "Extrapole l'altitude Z d'un point situé au-delà des points de référence. "
                      "Calcule la pente et projette l'altitude.",
        "usage": [
            "Sélectionner une couche ligne en mode édition",
            "Cliquer sur l'extrémité à extrapoler",
            "L'altitude est calculée automatiquement"
        ],
        "requires": "Couche ligne en mode édition"
    },
    {
        "name": "Elevation Pointer",
        "icon": "pointer_icon.png",
        "short": "Pointeur d'altitude",
        "description": "Affiche l'altitude Z des entités sous le curseur. "
                      "Utile pour vérifier rapidement les valeurs d'altitude.",
        "usage": [
            "Activer l'outil",
            "Survoler les entités pour voir leur altitude",
            "L'altitude s'affiche dans la barre de message"
        ],
        "requires": "Couches avec géométrie Z"
    },
    {
        "name": "Intersect",
        "icon": "intersect_icon.png",
        "short": "Cercle depuis intersection",
        "description": "Crée un cercle ou un arc à partir d'une intersection. "
                      "Permet de générer des géométries circulaires précises.",
        "usage": [
            "Cliquer sur un point d'intersection",
            "Définir le rayon du cercle",
            "Choisir le type (cercle complet ou arc)",
            "Valider la création"
        ],
        "requires": "Sketching/snap activé"
    },
    {
        "name": "Multi-Attributes",
        "icon": "select_icon.png",
        "short": "Sélection multi-couches",
        "description": "Permet de sélectionner des entités sur plusieurs couches simultanément. "
                      "Dessine un rectangle de sélection et sélectionne toutes les entités intersectées.",
        "usage": [
            "Activer l'outil",
            "Dessiner un rectangle de sélection",
            "Toutes les entités visibles sont sélectionnées"
        ],
        "requires": "Couches visibles"
    },
    {
        "name": "Drawdown",
        "icon": "drawdown_icon.png",
        "short": "Profil en long (rabattement)",
        "description": "Outil spécialisé pour les profils en long de canalisations. "
                      "Permet de visualiser et ajuster les pentes et les niveaux.",
        "usage": [
            "Configurer les couches de référence dans les paramètres",
            "Sélectionner le tronçon à analyser",
            "Visualiser et ajuster le profil"
        ],
        "requires": "Configuration spécifique dans les paramètres"
    },
    {
        "name": "Control",
        "icon": "control_icon.png",
        "short": "Requêtes de contrôle",
        "description": "Exécute des requêtes de contrôle qualité sur une zone sélectionnée. "
                      "Permet de vérifier la cohérence des données.",
        "usage": [
            "Configurer les requêtes dans les paramètres",
            "Dessiner une zone de contrôle",
            "Sélectionner la requête à exécuter",
            "Analyser les résultats"
        ],
        "requires": "Requêtes configurées dans les paramètres"
    },
    {
        "name": "Rebuild Index",
        "icon": "rebuild_icon.png",
        "short": "Reconstruire les index",
        "description": "Reconstruit les index spatiaux des couches. "
                      "Utile après des modifications importantes pour améliorer les performances.",
        "usage": [
            "Cliquer sur l'outil",
            "Les index sont reconstruits automatiquement"
        ],
        "requires": "Aucun"
    },
    {
        "name": "Settings",
        "icon": "settings_icon.png",
        "short": "Paramètres MaxTools",
        "description": "Configure les paramètres du plugin: URL du MNT, couches mémoire, "
                      "couches de référence, requêtes de contrôle, etc.",
        "usage": [
            "Ouvrir les paramètres via le menu",
            "Configurer les différentes options",
            "Sauvegarder"
        ],
        "requires": "Aucun"
    }
]


def generate():
    doc = GeoMindDocTemplate(
        OUTPUT_PATH,
        doc_description="Manuel utilisateur v1.0"
    )
    styles = get_styles()
    elements = []

    # === PAGE DE TITRE ===
    elements.append(Spacer(1, 2 * cm))
    elements.append(Paragraph("MAXTOOLS", styles['GTitle']))
    elements.append(Paragraph("Plugin QGIS pour la gestion des géodonnées", styles['GSubtitle']))
    elements.append(Spacer(1, 1 * cm))

    # Logo si disponible (conserver les proportions)
    logo_path = r"C:\Users\zema\GeoBrain\docs\Logos\GeoMind_Logo_tsp.png"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=5*cm, height=5*cm, kind='proportional')
            img.hAlign = 'CENTER'
            elements.append(img)
        except:
            pass

    elements.append(Spacer(1, 1.5 * cm))
    elements.append(Paragraph("Manuel d'utilisation", styles['GH1']))
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(create_metadata_table({
        "Version :": "1.0 (QGIS 3.x)",
        "Date :": format_date(),
        "Auteur original :": "Max Francken (Ville de Lausanne)",
        "Migration QGIS 3 :": "GeoMind / Marc Zermatten",
        "Licence :": "GNU GPL v2"
    }))

    elements.append(PageBreak())

    # === TABLE DES MATIÈRES ===
    elements.append(Paragraph("Table des matières", styles['GH1']))
    elements.append(Spacer(1, 0.3 * cm))

    toc_data = [["#", "Outil", "Description"]]
    for i, tool in enumerate(TOOLS, 1):
        toc_data.append([str(i), tool['name'], tool['short']])

    toc_table = create_table(toc_data, [1*cm, 4*cm, 10*cm], zebra=True)
    elements.append(toc_table)

    elements.append(PageBreak())

    # === INTRODUCTION ===
    elements.append(Paragraph("Introduction", styles['GH1']))
    elements.append(Paragraph(
        "MaxTools est un plugin QGIS développé initialement par Max Francken pour la Ville de Lausanne. "
        "Il fournit un ensemble d'outils spécialisés pour la gestion des géodonnées, notamment pour "
        "les réseaux d'infrastructure (canalisations, routes, etc.).",
        styles['GBody']
    ))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(
        "Cette version a été migrée vers QGIS 3.x et adaptée par GeoMind.",
        styles['GBody']
    ))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(create_tip_box(
        "La plupart des outils nécessitent que la couche soit en <b>mode édition</b>. "
        "Activez le mode édition avant d'utiliser les outils."
    ))

    elements.append(Spacer(1, 0.5 * cm))

    # === DOCUMENTATION DES OUTILS ===
    elements.append(Paragraph("Outils disponibles", styles['GH1']))
    elements.append(create_separator())
    elements.append(Spacer(1, 0.5 * cm))

    for i, tool in enumerate(TOOLS, 1):
        # Titre de l'outil
        elements.append(Paragraph(f"{i}. {tool['name']}", styles['GH2']))
        elements.append(Paragraph(f"<i>{tool['short']}</i>", styles['GBody']))
        elements.append(Spacer(1, 0.2 * cm))

        # Description
        elements.append(Paragraph(tool['description'], styles['GBody']))
        elements.append(Spacer(1, 0.2 * cm))

        # Prérequis
        elements.append(Paragraph(f"<b>Prérequis :</b> {tool['requires']}", styles['GBody']))
        elements.append(Spacer(1, 0.2 * cm))

        # Utilisation
        elements.append(Paragraph("<b>Utilisation :</b>", styles['GBody']))
        for step in tool['usage']:
            elements.append(Paragraph(f"• {step}", styles['GBullet']))

        elements.append(Spacer(1, 0.5 * cm))
        elements.append(create_separator())
        elements.append(Spacer(1, 0.3 * cm))

    # === CONFIGURATION ===
    elements.append(PageBreak())
    elements.append(Paragraph("Configuration", styles['GH1']))
    elements.append(Paragraph(
        "Les paramètres du plugin sont accessibles via le menu MaxTools > Settings. "
        "Les principales options sont :",
        styles['GBody']
    ))
    elements.append(Spacer(1, 0.3 * cm))

    config_data = [
        ["Paramètre", "Description"],
        ["URL MNT", "URL du service WCS pour les profils de terrain"],
        ["Couche points mémoire", "Couche pour stocker les points temporaires"],
        ["Couche lignes mémoire", "Couche pour stocker les lignes temporaires"],
        ["Couches de référence", "Couches utilisées pour les profils"],
        ["Couche de rabattement", "Couche pour l'outil Drawdown"],
        ["Requêtes de contrôle", "Configuration des requêtes de validation"]
    ]
    elements.append(create_table(config_data, [5*cm, 10*cm]))

    elements.append(Spacer(1, 0.5 * cm))
    elements.append(create_warning_box(
        "Les paramètres sont sauvegardés dans le projet QGIS. "
        "Pensez à sauvegarder votre projet après configuration."
    ))

    # === DÉPANNAGE ===
    elements.append(PageBreak())
    elements.append(Paragraph("Dépannage", styles['GH1']))

    troubleshoot = [
        ("Bouton grisé", "Vérifiez que la couche appropriée est sélectionnée et en mode édition"),
        ("Profil vide", "Vérifiez que les entités ont des coordonnées Z ou que le MNT est configuré"),
        ("Sketching inactif", "Activez le sketching avancé dans les options de sketching QGIS"),
        ("Erreur de connexion MNT", "Vérifiez l'URL et la connectivité réseau")
    ]

    for problem, solution in troubleshoot:
        elements.append(Paragraph(f"<b>{problem}</b>", styles['GH3']))
        elements.append(Paragraph(solution, styles['GBody']))
        elements.append(Spacer(1, 0.2 * cm))

    # Générer le PDF
    doc.build(elements)
    print(f"Manuel généré : {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
