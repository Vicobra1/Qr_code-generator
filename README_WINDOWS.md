# Kobra QR — version Windows

## Lancer l’application

Pour créer l’exécutable, suis les étapes ci-dessous, puis ouvre le dossier `dist` et double-clique sur `Kobra QR.exe`. La fenêtre du programme s’ouvre directement, sans fenêtre noire de terminal. Pour l’utiliser sur un autre ordinateur, copie ce fichier sur un PC Windows 64 bits. Python et les bibliothèques du projet ne sont pas nécessaires sur cet autre ordinateur.

Windows peut afficher un avertissement SmartScreen, car l’application n’est pas signée. Le fichier est compilé pour Windows 64 bits; il ne fonctionnera pas sur une version 32 bits de Windows.

## Recréer l’exécutable

Depuis ce dossier, double-clique sur `build_windows.bat`. La construction nécessite Python 3 et une connexion Internet lors du premier lancement pour télécharger les outils. Cette étape de fabrication peut afficher un terminal; l’application compilée, elle, ne l’affiche pas.

Le script utilise `requirements.txt` et `build-requirements.txt`, crée une icône depuis `create_icon.py`, puis place l’application dans `dist/Kobra QR.exe`. Le code source `main.py` et les images du projet restent à leur place.
