# 📖 Guide de Modification de la Progression de l'Histoire

## Vue d'ensemble

Ce document explique comment modifier la progression de l'histoire dans les sauvegardes d'Octopath Traveler 2, en particulier les chapitres complétés par chaque personnage.

## 🎯 Structure des Données d'Histoire

### Endroll_ClearedMS

**Emplacement**: Structure `MainStoryData` dans la sauvegarde

Cette propriété contient un **tableau d'IDs de chapitres complétés** pour l'écran de générique final.

#### Format

```
[Endroll_ClearedMS]
  ├── Nombre d'éléments (int32)
  ├── ID Chapitre 1 (int32)
  ├── ID Chapitre 2 (int32)
  ├── ID Chapitre 3 (int32)
  └── ...
```

#### Exemple de Données

```python
# Exemple trouvé dans une sauvegarde:
chapter_ids = [26, 27, 21, 31, 33]
# Représente 5 chapitres complétés
```

## 🔢 Format des IDs de Chapitres

### Hypothèses Testées

Plusieurs hypothèses ont été testées pour comprendre le format des IDs:

#### ❓ Hypothèse 1: (Personnage × 5) + Chapitre
```
ID = (CharacterID × 5) + ChapterNumber
```
**Statut**: Non confirmé

#### ❓ Hypothèse 2: (Personnage × 10) + Chapitre
```
ID = (CharacterID × 10) + ChapterNumber
Exemple: ID 21 = Personnage 2, Chapitre 1
```
**Statut**: Partiellement validé, mais certains IDs (26, 27) dépassent 25

#### ⚠️ Observation

Les IDs actuellement trouvés:
- **20-29**: IDs 21, 26, 27 (3 chapitres)
- **30-39**: IDs 31, 33 (2 chapitres)

**Conclusion actuelle**: Le pattern n'est pas une simple formule mathématique. Il faut tester méthodiquement en ajoutant des IDs connus.

## 🎮 Les 8 Personnages

| ID | Personnage | Chapitres (5 total) |
|----|-----------|---------------------|
| 0  | Hikari    | 1, 2, 3, 4, 5       |
| 1  | Agnea     | 1, 2, 3, 4, 5       |
| 2  | Partitio  | 1, 2, 3, 4, 5       |
| 3  | Osvald    | 1, 2, 3, 4, 5       |
| 4  | Throné    | 1, 2, 3, 4, 5       |
| 5  | Temenos   | 1, 2, 3, 4, 5       |
| 6  | Ochette   | 1, 2, 3, 4, 5       |
| 7  | Castti    | 1, 2, 3, 4, 5       |

**Note**: L'ordre exact des personnages dans le jeu peut varier.

## 🧪 Tests Recommandés

Pour identifier le pattern correct des IDs de chapitres:

### Test 1: IDs Séquentiels de Base
```python
test_ids = [1, 2, 3, 4, 5]  # Premiers IDs possibles
```
Observer dans le jeu quel personnage et quel chapitre s'activent.

### Test 2: IDs par Dizaines
```python
test_ids = [10, 11, 12, 13, 14]  # Première dizaine
test_ids = [20, 21, 22, 23, 24]  # Deuxième dizaine
```

### Test 3: IDs Existants + 1
```python
# Puisque 21, 26, 27, 31, 33 existent
test_ids = [22, 23, 24, 25]  # Compléter la série
test_ids = [28, 29, 30]      # Entre 27 et 31
test_ids = [32, 34, 35]      # Autour de 31-33
```

## 🛠️ Outils Disponibles

### 1. chapter_editor_mainstory.py

Éditeur principal pour modifier les chapitres complétés.

```bash
python chapter_editor_mainstory.py
```

**Fonctionnalités**:
- Afficher les chapitres actuellement complétés
- Ajouter un nouveau chapitre par ID
- Retirer un chapitre
- Réinitialiser tous les chapitres

### 2. analyze_chapter_pattern.py

Analyse le pattern des IDs de chapitres.

```bash
python analyze_chapter_pattern.py
```

**Sortie**:
- Hypothèses de décodage des IDs
- Analyse des différences entre IDs
- Regroupement par dizaines
- IDs possibles à tester

### 3. find_completed_chapters.py

Localise les chapitres complétés dans une sauvegarde.

```bash
python find_completed_chapters.py
```

## 📝 Utilisation: Modifier les Chapitres

### Exemple 1: Ajouter un Chapitre

```python
# Dans chapter_editor_mainstory.py
votre_choix: 2
ID du chapitre à ajouter: 1

# Résultat
✓ Chapitre ID 1 ajouté
✓ Nouveau total: 6 chapitres
```

### Exemple 2: Voir les Chapitres Actuels

```python
votre_choix: 1

# Résultat
Chapitres complétés: [26, 27, 21, 31, 33]
Total: 5 chapitres
```

### Exemple 3: Réinitialiser

```python
votre_choix: 4

# Résultat
⚠️ Tous les chapitres seront supprimés
Confirmer? (o/n): o
✓ Tous les chapitres ont été réinitialisés
```

## 🔍 Structure Technique

### Position de MainStoryData

Le bloc `MainStoryData` se trouve après l'en-tête GVAS et contient:

```
[MainStoryData]
  ├── Endroll_ClearedMS (ArrayProperty)
  │   ├── Nombre d'IDs (int32)
  │   └── Liste des IDs (int32[])
  ├── CurrentChapter (IntProperty) [?]
  └── Autres données d'histoire
```

### Format de Endroll_ClearedMS

```python
# Structure en mémoire
offset: position dans le fichier
+0x00: longueur du nom "Endroll_ClearedMS" (int32)
+0x04: nom "Endroll_ClearedMS" (string)
+XX:   type "ArrayProperty" (string)
+XX:   taille du tableau (uint64)
+XX:   nombre d'éléments (int32)
+XX:   type des éléments "IntProperty" (string)
+XX:   terminateur (0x00)
+XX:   ID 1 (int32)
+XX:   ID 2 (int32)
...
```

## ⚠️ Précautions

### Avant de Modifier

1. **Backup obligatoire**: Toujours créer une copie de votre sauvegarde
2. **Fermez le jeu**: Ne modifiez jamais une sauvegarde pendant que le jeu est ouvert
3. **Testez prudemment**: Ajoutez les IDs un par un et testez dans le jeu

### Valeurs Sûres

- **Nombre de chapitres**: 0 - 40 (8 personnages × 5 chapitres)
- **IDs de chapitres**: Probablement 1 - 40
- **Pas de doublons**: Ne pas ajouter le même ID deux fois

### En Cas de Problème

Si le jeu ne charge pas ou crash:

1. Fermez le jeu
2. Restaurez le backup `.sav.backup`
3. Réessayez avec des IDs différents
4. Consultez la documentation du jeu pour l'ordre des chapitres

## 🔬 Recherche en Cours

### Questions Non Résolues

- [ ] Quel est le pattern exact des IDs de chapitres?
- [ ] Y a-t-il d'autres propriétés liées aux chapitres?
- [ ] Comment fonctionnent les quêtes secondaires?
- [ ] Y a-t-il des flags de progression séparés?

### À Tester

1. Tester tous les IDs de 1 à 40 systématiquement
2. Comparer plusieurs sauvegardes à différents stades
3. Analyser les sauvegardes après chaque chapitre complété
4. Vérifier s'il y a des checksums ou validations

## 📚 Références

### Scripts Connexes

- [find_mainstorydata.py](find_mainstorydata.py) - Localise MainStoryData
- [search_chapter_strings.py](search_chapter_strings.py) - Cherche les chaînes de chapitres
- [analyze_clearedms.py](analyze_clearedms.py) - Analyse Endroll_ClearedMS

### Documentation

- [DATA_STRUCTURES.md](DATA_STRUCTURES.md) - Toutes les structures identifiées
- [CHARACTERS_FOUND.md](CHARACTERS_FOUND.md) - Positions des 8 personnages

## 💡 Conseils

### Méthodologie de Test

1. **Sauvegarde de référence**: Gardez une sauvegarde au début de chaque chapitre
2. **Tests incrémentaux**: Ajoutez un seul ID à la fois
3. **Documentation**: Notez quel ID correspond à quel chapitre
4. **Partage**: Partagez vos découvertes avec la communauté

### Identifier les IDs

```python
# Méthode suggérée
1. Complétez un chapitre dans le jeu
2. Copiez la sauvegarde (avant et après)
3. Comparez les deux fichiers avec compare_saves.py
4. Identifiez les nouveaux IDs ajoutés
5. Documentez: ID X = Personnage Y, Chapitre Z
```

## 🎯 Objectif Final

Créer une table de correspondance complète:

| ID  | Personnage | Chapitre | Vérifié |
|-----|-----------|----------|---------|
| 1   | ?         | ?        | ❌      |
| 2   | ?         | ?        | ❌      |
| ... | ...       | ...      | ...     |
| 21  | ?         | ?        | ✅ Trouvé |
| 26  | ?         | ?        | ✅ Trouvé |
| 27  | ?         | ?        | ✅ Trouvé |
| 31  | ?         | ?        | ✅ Trouvé |
| 33  | ?         | ?        | ✅ Trouvé |
| ... | ...       | ...      | ...     |
| 40  | ?         | ?        | ❌      |

---

**Dernière mise à jour**: 26 octobre 2025
**Status**: En cours de recherche
