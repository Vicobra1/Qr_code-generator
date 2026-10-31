# Kobra QR — Générateur de QR codes

Kobra QR est un projet d’apprentissage Python avec une interface de bureau Tkinter. La version 2 reprend le thème sombre et turquoise de Kobra Password et rend la création de QR codes plus guidée.

## Démarrer le programme

1. Ouvre un terminal dans le dossier `Qrcode_generator`.
2. Installe les dépendances :

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Lance l’application :

   ```powershell
   py main.py
   ```

Tkinter est inclus avec la plupart des installations Python pour Windows.

## Utiliser l’interface

1. Choisis le type d’information à encoder.
2. Remplis les champs qui apparaissent.
3. Choisis les couleurs et la taille de l’image.
4. Clique sur **Créer l’aperçu** pour vérifier le QR code.
5. Clique sur **Enregistrer PNG** pour choisir où enregistrer l’image.

Le QR code est généré sur l’ordinateur. Le contenu n’est envoyé à aucun service en ligne.

## Types pris en charge

- **Lien web** : accepte `http://` et `https://`. Si le protocole est omis, `https://` est ajouté.
- **Texte libre** : encode un texte simple.
- **Carte de contact** : produit une carte vCard avec le nom et, si souhaité, le téléphone, l’adresse e-mail et l’organisation.
- **Réseau Wi-Fi** : encode le nom du réseau, la sécurité WPA/WPA2, WEP ou aucune, le mot de passe et l’option réseau masqué.

Les lecteurs de QR codes peuvent présenter différemment les cartes de contact selon leur appareil. Scanne le résultat avant de le distribuer.

## Personnalisation

- Trois couleurs foncées pour les modules et trois fonds clairs pour conserver un contraste lisible.
- Trois tailles d’image : petite, moyenne et grande.
- L’aperçu est réduit pour tenir dans la fenêtre; le fichier PNG conserve la résolution sélectionnée.
- Le niveau de correction d’erreur est réglé sur M et la bordure conserve quatre modules autour du code.

## Historique des modifications

### Version 2

- Refonte de l’interface en français avec une palette sombre, turquoise et des panneaux inspirés de Kobra Password.
- Ajout d’un aperçu avant l’enregistrement et séparation des boutons de génération et de sauvegarde.
- Ajout des formats texte, vCard et Wi-Fi en plus des liens web.
- Ajout de choix de couleurs et de trois tailles PNG.
- Ajout de validations de saisie et de messages d’erreur plus explicites.
- Ajout de ce README et de `requirements.txt`.

### Version 1

- Génération d’un QR code noir et blanc à partir d’un texte ou d’un lien.
- Enregistrement direct au format PNG.

## Limites et précautions

Évite d’encoder des secrets ou des informations privées dans un QR code destiné à être partagé. Les couleurs proposées gardent un contraste clair, mais il est toujours conseillé de tester le code avec un téléphone avant impression ou diffusion.
