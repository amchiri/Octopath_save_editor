# 🎮 Guide de Démarrage Rapide - Octopath Traveler 2 Save Editor

## Installation

1. **Pré-requis**: Python 3.7 ou supérieur
   ```bash
   python --version
   ```

2. **Aucune dépendance externe requise** - Utilise uniquement les bibliothèques standard Python

## Utilisation en 3 Étapes

### 1️⃣ Placer vos Sauvegardes

Copiez vos fichiers `.sav` dans le dossier `SaveData/`:

```
Octopath_save/
└── SaveData/
    ├── SaveData0.sav
    ├── SaveData1.sav
    └── ...
```

**Emplacement Windows typique des sauvegardes**:
```
C:\Users\[VotreNom]\AppData\Local\Octopath_Traveler2\Saved\SaveGames\
```

### 2️⃣ Analyser vos Sauvegardes (Optionnel)

```bash
# Analyse basique
python gvas_parser.py

# Analyse approfondie des patterns
python pattern_analyzer.py

# Analyse des propriétés
python octopath_parser.py
```

### 3️⃣ Modifier une Sauvegarde

```bash
python save_editor.py
```

**Menu interactif**:
```
Fichiers de sauvegarde disponibles:
  0: SaveData0.sav
  1: SaveData1.sav
  ...
  
Choisissez un fichier (numéro): 0
✓ Fichier chargé: SaveData0.sav
✓ Backup créé: SaveData0.sav.backup

Options:
  1. Afficher le résumé des stats
  2. Scanner les patterns de données
  3. Modifier HP/MP
  4. Modifier EXP
  5. Rechercher et remplacer une valeur
  6. Sauvegarder les modifications
  0. Quitter
```

## Exemples Pratiques

### Exemple 1: Augmenter les HP de tous les personnages

```
Votre choix: 3
Nouvelle valeur HP: 9999
Nouvelle valeur MP (laisser vide pour ignorer): 

Modification des HP à 9999:
  0x000878B6: 3072 -> 9999
  0x00089411: 3072 -> 9999
  ... (40 modifications)

Votre choix: 6
✓ Sauvegardé: SaveData0.sav
```

### Exemple 2: Donner beaucoup d'expérience

```
Votre choix: 4
Nouvelle valeur EXP: 999999

Modification de l'EXP à 999999:
  0x00080E6C [BackupExp]: 58368 -> 999999
  0x00080EBC [Org_Exp]: 10748025 -> 999999

Votre choix: 6
✓ Sauvegardé: SaveData0.sav
```

### Exemple 3: Afficher les stats actuelles

```
Votre choix: 1

======================================================================
Résumé des statistiques du personnage
======================================================================

HP trouvés: 40
  Personnage 1: 3072 HP (0x000878B6)
  Personnage 2: 3072 HP (0x00089411)
  Personnage 3: 3072 HP (0x0008AF6C)
  ...

EXP trouvés: 2
  BackupExp: 58368 (0x00080E6C)
  Org_Exp: 10748025 (0x00080EBC)
```

## ⚠️ Sécurité

### Avant de Modifier

1. ✅ **TOUJOURS créer un backup** de vos sauvegardes originales
   - L'éditeur crée automatiquement un `.sav.backup`
   - Mais faites aussi une copie manuelle dans un dossier séparé

2. ✅ **Tester sur une sauvegarde de test** d'abord
   - Copiez une sauvegarde et renommez-la
   - Testez vos modifications dessus

3. ✅ **Valeurs raisonnables recommandées**:
   - HP: 1 - 9,999 (max sûr: 9,999)
   - MP: 1 - 999 (max sûr: 999)
   - EXP: 0 - 999,999 (max sûr: 999,999)

### En Cas de Problème

Si le jeu ne charge pas votre sauvegarde modifiée:

1. Fermez le jeu
2. Supprimez le fichier `.sav` modifié
3. Restaurez le backup `.sav.backup`
4. Réessayez avec des valeurs plus modérées

## 🧪 Tests

Pour vérifier que l'éditeur fonctionne correctement:

```bash
python test_editor.py
```

Résultat attendu:
```
RÉSUMÉ DES TESTS
======================================================================

✓ PASS: Intégrité des fichiers
✓ PASS: Modification HP/MP
✓ PASS: Modification EXP

3/3 tests réussis (100%)
```

## 📊 Fonctionnalités Actuelles

### ✅ Fonctionnel

- ✅ Modification des HP (40 emplacements détectés)
- ✅ Modification de l'EXP (2 emplacements)
- ✅ Sauvegarde automatique de backup
- ✅ Interface interactive
- ✅ Recherche et remplacement de valeurs

### 🚧 En Cours

- 🚧 Modification des MP (détection à améliorer)
- 🚧 Modification de l'inventaire
- 🚧 Modification des jobs/classes
- 🚧 Modification de l'équipement

### 🔮 Prévu

- 🔮 Interface graphique (GUI)
- 🔮 Export/Import de personnages
- 🔮 Modification de la progression

## 🆘 Aide

### Problèmes Courants

**Q: "Aucun fichier de sauvegarde trouvé"**
- Vérifiez que vos `.sav` sont dans le dossier `SaveData/`
- Le chemin doit être: `Octopath_save/SaveData/SaveData0.sav`

**Q: "Le jeu ne charge pas ma sauvegarde"**
- Restaurez le backup `.sav.backup`
- Utilisez des valeurs plus raisonnables
- Assurez-vous que le jeu est fermé pendant la modification

**Q: "Les modifications ne sont pas visibles dans le jeu"**
- Rechargez complètement la sauvegarde (quittez et relancez le jeu)
- Vérifiez que vous avez bien sauvegardé (option 6 du menu)
- Assurez-vous de modifier le bon fichier de sauvegarde

**Q: "Erreur lors de l'exécution des scripts"**
- Vérifiez votre version de Python: `python --version`
- Doit être Python 3.7 ou supérieur

## 📚 Documentation Complète

Pour plus de détails:

- **README.md** - Documentation générale du projet
- **DATA_STRUCTURES.md** - Structures de données détaillées
- **gvas_parser.py** - Code source du parser GVAS
- **save_editor.py** - Code source de l'éditeur

## 🎯 Conseils

### Modification Progressive

Au lieu de modifier toutes les stats d'un coup:

1. Commencez par les HP uniquement
2. Testez dans le jeu
3. Si ça fonctionne, modifiez l'EXP
4. Testez à nouveau
5. Continuez progressivement

### Valeurs Réalistes

Pour une expérience équilibrée:

- **HP Niveau 50**: ~5,000
- **HP Niveau 99**: ~9,999
- **MP Niveau 50**: ~500
- **MP Niveau 99**: ~999
- **EXP pour niveau 50**: ~200,000
- **EXP pour niveau 99**: ~900,000

## 🤝 Contribution

Des questions? Des bugs? Des améliorations?

1. Consultez `DATA_STRUCTURES.md` pour les données identifiées
2. Utilisez `pattern_analyzer.py` pour découvrir de nouveaux patterns
3. Partagez vos découvertes!

---

**Bon jeu avec Octopath Traveler 2! 🎮✨**
