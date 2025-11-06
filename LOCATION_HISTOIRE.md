# 📍 LOCALISATION DES DONNEES D'HISTOIRE

## ENDROLL_CLEAREDMS - Chapitres Complétés

### Position dans SaveData0.sav
```
Offset: 0x000E352E (931,118 bytes du debut)
```

### Structure Exacte

```
0x000E352E: "Endroll_ClearedMS\x00"    (18 bytes)
0x000E3540: "ArrayProperty\x00"         (14 bytes)
0x000E354E: Taille du tableau (8 bytes) = 0xCC 00 00 00 00 00 00 00
0x000E3556: "IntProperty\x00"           (13 bytes)
0x000E3563: Padding (1 byte) = 0x00
0x000E3564: Nombre d'elements (4 bytes) = 50 (0x32 00 00 00)
0x000E3568: Debut des donnees
```

### Donnees des IDs de Chapitres

**Position de depart: 0x000E356E**

Chaque ID de chapitre occupe 4 bytes (Int32, little-endian):

```
Position    | ID  | Hex      | Chapitre?
------------|-----|----------|------------------
0x000E356E  | 26  | 1A 00... | Personnage?, Chapitre?
0x000E3572  | 27  | 1B 00... |
0x000E3576  | 21  | 15 00... |
0x000E357A  | 31  | 1F 00... |
0x000E357E  | 33  | 21 00... |
... (25 IDs au total)
```

### IDs Trouvés dans Votre Sauvegarde

**25 chapitres complétés:**
```
1,  7,  8,  9,  10, 11, 12,
17,
21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
31, 32, 33, 34, 35, 36, 37
```

### Pattern Observé

Les IDs vont de **1 à 37**.

Si on a 8 personnages avec 5 chapitres chacun = 40 chapitres maximum:
- IDs 1-5: Personnage 1?
- IDs 6-10: Personnage 2?
- IDs 11-15: Personnage 3?
- IDs 16-20: Personnage 4?
- IDs 21-25: Personnage 5?
- IDs 26-30: Personnage 6?
- IDs 31-35: Personnage 7?
- IDs 36-40: Personnage 8?

**Pattern probable: ID = (Personnage - 1) × 5 + Chapitre**

Exemples:
- ID 1 = Personnage 1, Chapitre 1
- ID 21 = Personnage 5, Chapitre 1
- ID 26 = Personnage 6, Chapitre 1
- ID 37 = Personnage 8, Chapitre 2

---

## Comment Modifier

### Méthode 1: Ajouter un Chapitre

```python
import struct

# Ouvrir le fichier
with open('SaveData/SaveData0.sav', 'r+b') as f:
    data = bytearray(f.read())

    # Position du tableau
    count_pos = 0x000E3567  # Position du nombre d'elements

    # Lire le nombre actuel
    current_count = struct.unpack_from('<I', data, count_pos)[0]

    # Calculer la position où ajouter le nouvel ID
    # Chaque ID = 4 bytes
    new_id_pos = 0x000E356E + (current_count * 4)

    # Ajouter un nouveau chapitre (ex: ID 2)
    new_chapter_id = 2
    struct.pack_into('<i', data, new_id_pos, new_chapter_id)

    # Incrementer le compteur
    struct.pack_into('<I', data, count_pos, current_count + 1)

    # Sauvegarder
    f.seek(0)
    f.write(data)
```

### Méthode 2: Retirer un Chapitre

```python
import struct

# Ouvrir le fichier
with open('SaveData/SaveData0.sav', 'r+b') as f:
    data = bytearray(f.read())

    # Position du tableau
    count_pos = 0x000E3567
    data_start = 0x000E356E

    # Lire le nombre actuel et tous les IDs
    current_count = struct.unpack_from('<I', data, count_pos)[0]

    chapter_ids = []
    for i in range(current_count):
        pos = data_start + (i * 4)
        chapter_id = struct.unpack_from('<i', data, pos)[0]
        chapter_ids.append(chapter_id)

    # Retirer un ID (ex: 26)
    id_to_remove = 26
    if id_to_remove in chapter_ids:
        chapter_ids.remove(id_to_remove)

    # Réécrire le tableau
    for i, chapter_id in enumerate(chapter_ids):
        pos = data_start + (i * 4)
        struct.pack_into('<i', data, pos, chapter_id)

    # Mettre à jour le compteur
    struct.pack_into('<I', data, count_pos, len(chapter_ids))

    # Sauvegarder
    f.seek(0)
    f.write(data)
```

### Méthode 3: Réinitialiser Tous les Chapitres

```python
import struct

# Ouvrir le fichier
with open('SaveData/SaveData0.sav', 'r+b') as f:
    data = bytearray(f.read())

    # Position du compteur
    count_pos = 0x000E3567

    # Mettre le compteur à 0
    struct.pack_into('<I', data, count_pos, 0)

    # Sauvegarder
    f.seek(0)
    f.write(data)
```

---

## Scripts Disponibles

### Pour Analyser
```bash
# Voir les chapitres actuels
python analyze_all_mainstorydata.py

# Voir les positions exactes
python find_completed_chapters.py
```

### Pour Modifier
```bash
# Éditeur interactif
python chapter_editor_mainstory.py
```

---

## ⚠️ IMPORTANT

### Avant TOUTE Modification

1. **BACKUP**: Faites une copie de votre sauvegarde
   ```bash
   cp SaveData/SaveData0.sav SaveData/SaveData0.sav.backup
   ```

2. **Fermez le jeu** complètement

3. **Testez prudemment**: Ajoutez UN SEUL chapitre à la fois

### Valeurs Sûres

- **IDs valides**: 1 à 40
- **Nombre max**: 40 (8 personnages × 5 chapitres)
- **Pas de doublons**: Chaque ID doit être unique

### En Cas de Problème

1. Fermez le jeu
2. Supprimez `SaveData0.sav`
3. Renommez `SaveData0.sav.backup` en `SaveData0.sav`
4. Relancez le jeu

---

## Table de Correspondance (À Confirmer)

| ID  | Personnage Probable | Chapitre |
|-----|-------------------|----------|
| 1   | Hikari            | 1        |
| 2   | Hikari            | 2        |
| 3   | Hikari            | 3        |
| 4   | Hikari            | 4        |
| 5   | Hikari            | 5        |
| 6   | Agnea             | 1        |
| 7   | Agnea             | 2        |
| ... | ...               | ...      |
| 21  | Temenos           | 1        |
| 22  | Temenos           | 2        |
| 23  | Temenos           | 3        |
| 24  | Temenos           | 4        |
| 25  | Temenos           | 5        |
| 26  | Osvald            | 1        |
| 27  | Osvald            | 2        |
| ... | ...               | ...      |
| 36  | Castti            | 1        |
| 37  | Castti            | 2        |
| 38  | Castti            | 3        |
| 39  | Castti            | 4        |
| 40  | Castti            | 5        |

**Note**: L'ordre exact des personnages doit être confirmé en testant dans le jeu!

---

## Prochaines Étapes

1. **Tester le pattern**: Ajouter ID 2 et vérifier quel personnage/chapitre s'active
2. **Documenter**: Noter les résultats dans un fichier `CHAPTER_IDS_TESTS.md`
3. **Compléter la table**: Tester tous les IDs de 1 à 40
4. **Créer un éditeur**: Script facile pour ajouter/retirer des chapitres

---

**Dernière mise à jour**: 27 octobre 2025
**Status**: Position trouvée, pattern à confirmer par tests