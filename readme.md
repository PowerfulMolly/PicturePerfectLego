# LegoMosaicMaster (FR)

Projet de groupe en spécialité de NSI en 1ère.
LegoMosaicMaster vous permet d'automatiser le processus de creation de pixel art en lego. Il vous permet de convertir n'importe quelle image en un modèle lego prêt à la construction.

<br>

![]()

## Fonctionnalités:
- pixelisation d'une image et conversion de ses couleurs en celles disponibles à l'achat chez lego
- support du canal alpha, donc des images transparentes avec ajout possible d'une couleur de fond ou d'une image de fond personnalisée
- mode couleur, niveaux de gris ou noir et blanc
- taux de pixelisation reglable afin d'adapter l'outil à différentes exigences de précision et de couts
- instructions détaillées et interactives sous formes d'une page html du montage et des pièces requises

<br>

## Installation (developpement):
- copier le repository
- installer python, se placer dans le répertoire `sources` les dependances `PIL`, `jinja2` (ainsi que `tkinter`, `os`, `math`, normalement installés lors de l'installation de python) sur votre environnement python
- lancer `interface.py` (fichier dans `sources/interface.py`)

<br>

## Installation (production):
- télécharger l'executable portable (nommé `PicturePerfectLego-exe.zip`) de votre système dans les releases ou en copier le repository, dézipper, ouvrir le dossier nouvellement créé et lancer `PicturePerfectLego.exe` (windows)

<br>

## Utilisation/lancement:
- Ajouter une image en appuyant sur téléverser
- Choisir le niveau de pixelisation et le mode de couleur (couleurs/nuances de gris/noir et blanc)
- Choisir une éventuelle couleur ou image de fond si l'image sélectionnée est transparente
- Demander (si souhaité) les instructions

Pour changer d'image ou modifier les options de pixelisation, il suffit d'appuyer sur la croix à droite de l'image en question

<br>

## Ameliorations possibles:
- Utilisation d'autres pièces, plus grosses que 1x1 (pour diminuer les couts): faisable pour des pièces carrées, plus difficile pour des pièces non carrées et augmente le temps de calcul, non souhaitable pour que le programme soit utilisable sur des ordinateurs peu puissants
- Estimation des couts: peu d'intérêt car le tarif d'une pièce lego peut fluctuer suivant l'achat sur la boutique officielle (pour information le tarif officiel en 2023 d'une pièce lego de 1x1 est de 0,06€) ou bien sur une marketplace tierce (bricklink par exemple).
    - Une connection à l'API de bricklink serait alors envisageable pour avoir un estimation de prix voire même commander directement les pièces nécessaires mais étant une marketplace entre professionnels & particuliers, les données seraient complexes à filtrer (il faudrait prendre en compte le nombre de pièces achetées, les frais de livraison, les taxes, ... afin d'avoir une estimation de prix correcte).
    - L'objectif du projet réside également dans la réutilisation de pièces lego vacantes dans les tiroirs, rendant cette fonctionnalité moins importante
- Refonte graphique: avec un peu plus de temps, l'interface réalisée avec tkinter a été faite sans ajout de style particulier et mériterait donc une refonte graphique pour la rendre plus attrayante (palette de couleurs, plus gros boutons, ...)
