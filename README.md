# MaxTools
Outils QGIS pour Max Francken
-------------------------------------

> **Version 1.0.0** - Migré vers QGIS 3.x par Marc Zermatten via GeoMind (2025)

## 📖 Documentation

**[📥 Télécharger le Manuel Utilisateur (PDF)](docs/MaxTools_Manuel_Utilisateur.pdf)**

Le manuel complet contient la documentation de tous les outils avec exemples d'utilisation.

## Compatibilité

| Version | QGIS | Python | Qt |
|---------|------|--------|-----|
| 0.9 (originale) | 2.18+ | 2.7 | 4 |
| **1.0.0** | **3.0 - 3.44+** | **3.6+** | **5/6** |

## Installation

1. Télécharger ou cloner ce dépôt
2. Copier le dossier `MaxTools` dans :
   - **Windows** : `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux** : `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS** : `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Redémarrer QGIS
4. Activer le plugin : `Extensions` → `Gérer les extensions` → Cocher "Max Tools"

## Outils disponibles

### Duplicate

L'outil "Duplicate" permet de copier un objet dans une direction à une distance donnée. La distance est fixe pour chaque noeud de l'objet, donc la géométrie n'est pas conservée.

- sélectionner une couche éditable
- sélectionner l'outil
- sélectionner un élément sur la carte
- choisir à quelle distance et dans quelle direction dupliquer l'élément
- compléter les attributs du formulaire s'il est affiché

![Duplicate Gif](./gifs/duplicate.gif)

---

### Move

L'outil "Move" permet de déplacer ou copier un objet.

- sélectionner une couche éditable
- sélectionner l'outil
- sélectionner un élément sur la carte
- sélectionner un vertex de l'élément (si ce n'est pas un point)
- choisir où déplacer/copier l'élément et cliquer (utilisation possible des options d'accrochage)
- choisir entre déplacer et copier
- pour une copie, compléter les attributs du formulaire s'il est affiché

![Move Gif](./gifs/copy.gif)

---

### Intersect

L'outil "Intersect" permet de créer un cercle de construction d'un rayon donné.

- sélectionner une couche
- sélectionner l'outil
- sélectionner une position (utilisation possible des options d'accrochage)
- choisir le diamètre
- en cliquant sur OK le point central est enregistré dans une couche mémoire de points et le cercle dans une couche mémoire de lignes

Ces couches peuvent être choisies dans les paramètres (`Extension` → `MaxTools`).

![Intersect Gif](./gifs/intersect.gif)

---

### Profile

L'outil "Profile" permet d'afficher le profil d'une ligne 3D en parallèle de couches de points 3D.

> **Note QGIS 3.x** : Seul Matplotlib est disponible (Qwt5 n'est plus supporté)

- sélectionner une couche lignes
- sélectionner l'outil
- sélectionner une première ligne (détermine le sens du profil) avec le bouton gauche
- sélectionner autant de lignes contiguës que nécessaire
- cliquer sur le bouton droit pour lancer le profil
- choisir les couches de points à afficher

Options avancées :
- Correction des altitudes entre vertices et points
- Interpolation/extrapolation des altitudes nulles
- Affichage du profil MNT via service MapFish

![Profile Gif](./gifs/profile.gif)

---

### Subprofile

L'outil "Subprofile" permet d'afficher le profil MNT le long d'une polyline construite (nécessite un service MapFish).

---

### Interpolate

L'outil "Interpolate" permet d'interpoler une altitude au milieu d'un segment de ligne.

- sélectionner une couche points éditable
- sélectionner l'outil
- sélectionner la ligne sur laquelle se positionner
- choisir de créer un point, un vertex, ou les deux
- compléter les attributs du formulaire

![Interpolate Gif](./gifs/interpolate.gif)

---

### Extrapolate

L'outil "Extrapolate" permet d'extrapoler une altitude en bout de ligne.

- sélectionner une couche lignes éditable
- sélectionner l'outil
- sélectionner une extrémité de ligne à extrapoler

> Le dernier segment ne doit pas faire plus d'un quart du segment précédent.

![Extrapolate Gif](./gifs/extrapolate.gif)

---

### Pointer

L'outil "Pointer" permet d'obtenir l'altitude de différents éléments en un point donné.

---

### Control

Outil de contrôle pour vérifier la cohérence des données.

![Modèle représentation "Contrôle"](gifs/control_model_use.gif)

![Utilisation outils de contrôle](gifs/control.gif)

---

## Migration QGIS 2.x → 3.x

Cette version a été migrée de QGIS 2.18 vers QGIS 3.x. Principales modifications :

| Composant | Avant | Après |
|-----------|-------|-------|
| PyQt | PyQt4 | qgis.PyQt (Qt5/6) |
| Graphiques profil | Qwt5 | Matplotlib |
| Classes géométrie | QgsPointV2, etc. | QgsPoint, etc. |
| Registre couches | QgsMapLayerRegistry | QgsProject |

## Crédits

- **Auteur original** : Christophe Gusthiot (Ville de Lausanne)
- **Migration QGIS 3.x** : Marc Zermatten via GeoMind (2025)
- **Pour** : Max Francken
- **Licence** : GPL v2

## Changelog

### v1.0.0 (2025-12)
- Migration complète vers QGIS 3.x
- Remplacement Qwt5 par Matplotlib
- Compatibilité Python 3.6+
- Compatibilité Qt5/Qt6

### v0.9 (2016)
- Version originale pour QGIS 2.18
