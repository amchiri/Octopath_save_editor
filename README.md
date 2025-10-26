# 🎮 Éditeur de Sauvegarde Octopath Traveler 2

Outil complet pour analyser et modifier les fichiers de sauvegarde d'Octopath Traveler 2.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Status](https://img.shields.io/badge/status-beta-yellow)

## ⚠️ Avertissement Important

**FAITES TOUJOURS UNE SAUVEGARDE DE VOS FICHIERS ORIGINAUX AVANT DE LES MODIFIER!**

Les éditeurs créent automatiquement un backup (.sav.backup), mais il est recommandé de faire une copie manuelle également.

## 📁 Structure du Projet

```
Octopath_save/
├── SaveData/                          # Dossier contenant vos fichiers .sav
│
├── 📝 Documentation
│   ├── README.md                      # Ce fichier
│   ├── QUICKSTART.md                  # Guide de démarrage rapide
│   ├── DATA_STRUCTURES.md             # Structures de données détaillées
│   └── CHARACTERS_FOUND.md            # Positions des 8 personnages
│
├── ⚙️ Éditeurs Principaux (Stats des Personnages)
│   ├── hp_bonus_editor_correct.py     # Modifier HP/MP/Stats bonus
│   └── fixed_editor.py                # Éditeur général de stats
│
├── 📖 Éditeurs d'Histoire (NOUVEAU!)
│   ├── chapter_editor_mainstory.py    # Modifier la progression des chapitres
│   ├── story_editor.py                # Éditeur général d'histoire
│   └── analyze_chapter_pattern.py     # Analyser le format des IDs de chapitres
│
├── 🔍 Outils d'Analyse
│   ├── find_mainstorydata.py          # Localiser les données d'histoire
│   ├── find_completed_chapters.py     # Trouver les chapitres complétés
│   ├── analyze_clearedms.py           # Analyser Endroll_ClearedMS
│   └── search_chapter_strings.py      # Rechercher les chaînes de chapitres
│
└── 🧪 Scripts de Test
    ├── test_add_chapter.py            # Tester l'ajout de chapitres
    ├── test_100_hp_bonus.py           # Tester les modifications HP
    └── verify_temenos_position.py     # Vérifier les positions
```

## 🔧 Installation

Aucune dépendance externe requise! Utilise uniquement les bibliothèques standard Python.

```bash
# Requis: Python 3.7 ou supérieur
python --version
```

## 📖 Format des Fichiers

Les sauvegardes d'Octopath Traveler 2 utilisent le format **GVAS** d'Unreal Engine 4.27.

### Structure GVAS

```
[En-tête GVAS]
  ├── Signature: "GVAS" (4 octets)
  ├── Version de sauvegarde: 2
  ├── Version de package: 522
  ├── Unreal Engine: 4.27.2
  └── Type: KSSaveGameBP_C
  
[Données de propriétés]
  ├── BitFlag (Array)
  ├── Statistiques des personnages
  │   ├── RawHP, RawMP
  │   ├── BackupExp, Org_Exp
  │   ├── FirstJobID, SecondJobID
  │   └── EquipSupportSkill
  ├── Inventaire
  │   ├── ItemList
  │   ├── ItemId
  │   └── SaveBackPackItem
  └── Équipement
      ├── PlayerWeapon
      └── Sword, Dagger, Bow, Axe, etc.
```

## 🚀 Utilisation

### 1. Analyser une sauvegarde

```bash
# Analyse basique
python gvas_parser.py

# Analyse approfondie
python octopath_parser.py

# Analyse de patterns et recherche
python pattern_analyzer.py
```

### 2. Éditeur Interactif

```bash
python save_editor.py
```

**Menu principal:**
- `1` - Afficher le résumé des statistiques (HP/MP/EXP)
- `2` - Scanner les patterns de données
- `3` - Modifier HP/MP de tous les personnages
- `4` - Modifier l'EXP de tous les personnages
- `5` - Rechercher et remplacer une valeur spécifique
- `6` - Sauvegarder les modifications
- `0` - Quitter

### 3. Exemples d'Utilisation

#### Modifier les HP/MP
```
Votre choix: 3
Nouvelle valeur HP: 9999
Nouvelle valeur MP: 999
```

#### Modifier l'EXP
```
Votre choix: 4
Nouvelle valeur EXP: 999999
```

#### Rechercher et remplacer
```
Votre choix: 5
Valeur à rechercher: 100
Nouvelle valeur: 500
Remplacer par 500? (o/n): o
```

## 🔍 Données Identifiées

Grâce à l'analyse, nous avons identifié les emplacements suivants:

| Catégorie | Propriétés | Occurrences |
|-----------|-----------|-------------|
| **Items** | ItemList, ItemId, SaveBackPackItem | ~7,010 |
| **Jobs** | FirstJobID, SecondJobID, BackupJob | ~223 |
| **Stats** | RawHP, RawMP, BackupCurrentHP | ~41 HP, ~10k MP* |
| **Expérience** | BackupExp, Org_Exp | ~3 |
| **Compétences** | EquipSupportSkill | ~40 |
| **Armes** | Sword, Dagger, Bow, Axe, Spear, etc. | ~160 chaque |

*Note: Le nombre élevé de "MP" inclut les propriétés "EnumProperty"

## 📊 Fonctionnalités

### ✅ Implémenté
- [x] Parser l'en-tête GVAS
- [x] Identifier les structures de données
- [x] Localiser HP/MP des 8 personnages
- [x] Localiser l'expérience
- [x] Modifier HP/MP/Stats bonus
- [x] Modifier EXP
- [x] **Modifier la progression de l'histoire (chapitres)** ⭐ NOUVEAU!
- [x] Système de backup automatique
- [x] Interface interactive
- [x] Recherche et remplacement de valeurs
- [x] Analyse des IDs de chapitres complétés

### 🚧 En Développement
- [x] Modification de la progression (chapitres principaux) - **FONCTIONNEL**
- [ ] Modification de l'inventaire (items)
- [ ] Modification des jobs/classes
- [ ] Modification des compétences
- [ ] Modification de l'équipement complet

### 🔮 Prévu
- [ ] Interface graphique (GUI)
- [ ] Éditeur d'équipement détaillé
- [ ] Modification des quêtes secondaires
- [ ] Export/Import de personnages
- [ ] Templates de modifications

## 🛠️ Développement

### Ajouter de nouvelles fonctionnalités

1. **Identifier les données**: Utilisez `pattern_analyzer.py` pour rechercher des patterns
2. **Localiser précisément**: Analysez les positions avec `octopath_parser.py`
3. **Implémenter la modification**: Ajoutez une méthode dans `save_editor.py`
4. **Tester**: Vérifiez dans le jeu que les modifications fonctionnent

### Structure du code

```python
# Lecture d'une valeur
value = editor.read_int32_at(position)

# Écriture d'une valeur
editor.write_int32_at(position, new_value)

# Recherche de chaînes
positions = editor.find_string_positions('ItemId')
```

## 📝 Notes Techniques

- **Format d'encodage**: Les chaînes utilisent UTF-8/UTF-16
- **Endianness**: Little-endian (`<` dans struct)
- **Alignement**: Les données sont alignées sur 4 octets
- **Checksums**: Aucun checksum détecté (modifications directes possibles)

## 🐛 Dépannage

**Q: L'éditeur ne trouve pas mes sauvegardes**
- R: Assurez-vous que vos fichiers .sav sont dans le dossier `SaveData/`

**Q: Le jeu ne charge pas ma sauvegarde modifiée**
- R: Restaurez le backup et réessayez avec des valeurs plus raisonnables

**Q: Certaines modifications ne fonctionnent pas**
- R: Toutes les données ne sont pas encore identifiées. Consultez les TODO ci-dessus.

## 🤝 Contribution

Les contributions sont les bienvenues! Si vous découvrez de nouveaux emplacements de données:

1. Documentez vos trouvailles
2. Testez vos modifications
3. Partagez vos résultats

## 📄 License

Cet outil est fourni à des fins éducatives. Utilisez-le à vos propres risques.

## 🔗 Ressources

- [Unreal Engine GVAS Format](https://docs.unrealengine.com/)
- [Octopath Traveler 2 Wiki](https://octopathtraveler.fandom.com/)

---

**Développé avec ❤️ pour la communauté Octopath Traveler 2**
