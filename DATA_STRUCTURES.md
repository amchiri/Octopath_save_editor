# Documentation des Structures de Données - Octopath Traveler 2

## Vue d'ensemble

Ce document décrit les structures de données identifiées dans les fichiers de sauvegarde d'Octopath Traveler 2 (.sav).

## En-tête GVAS

```
Offset  | Taille | Type    | Description
--------|--------|---------|----------------------------------
0x0000  | 4      | ASCII   | Signature "GVAS"
0x0004  | 4      | uint32  | Version de sauvegarde (2)
0x0008  | 4      | uint32  | Version de package (522)
0x000C  | 2      | uint16  | Version UE4 - Major (4)
0x000E  | 2      | uint16  | Version UE4 - Minor (27)
0x0010  | 2      | uint16  | Version UE4 - Patch (2)
0x0012  | 4      | uint32  | Version UE4 - Build (0)
0x0016  | var    | string  | Build Version "++UE4+Release-4.27"
...     | var    | ...     | Formats personnalisés
...     | var    | string  | Type de sauvegarde
```

## Propriétés Identifiées

### Statistiques des Personnages

#### HP (Points de Vie)

**Chaîne de référence**: `RawHP`
- **Occurrences**: ~41 dans SaveData0.sav
- **Type**: IntProperty (int32)
- **Plage de valeurs**: 0 - 99,999
- **Offset typique**: Après la chaîne + ~20-50 octets

**Exemple**:
```
Position: 0x0008788A
Contexte: "RawHP" + metadata UE4 + valeur int32
```

#### MP (Points de Magie)

**Chaîne de référence**: `RawMP`
- **Occurrences**: ~40 (en excluant les EnumProperty)
- **Type**: IntProperty (int32)
- **Plage de valeurs**: 0 - 9,999
- **Offset typique**: Après la chaîne + ~20-50 octets

**Positions identifiées**:
- 0x000878B1
- 0x0008940C
- 0x0008AF67
- etc.

### Expérience

#### BackupExp

**Chaîne de référence**: `BackupExp`
- **Position**: 0x00080E50
- **Type**: IntProperty (int32)
- **Plage de valeurs**: 0 - 99,999,999

#### Org_Exp

**Chaîne de référence**: `Org_Exp`
- **Position**: 0x00080EA4
- **Type**: IntProperty (int32)

### Jobs/Classes

#### FirstJobID

**Chaîne de référence**: `FirstJobID`
- **Type**: IntProperty
- **Description**: ID du job principal du personnage

#### SecondJobID

**Chaîne de référence**: `SecondJobID`
- **Type**: IntProperty
- **Description**: ID du job secondaire du personnage

#### BackupJob

**Chaîne de référence**: `BackupJob`
- **Position**: 0x000514CA
- **Type**: IntProperty

### Inventaire

#### ItemList

**Chaîne de référence**: `ItemList`
- **Occurrences**: ~7,010
- **Type**: ArrayProperty
- **Description**: Liste de tous les items possédés

**Positions clés**:
- 0x0001704A
- 0x00017089

#### ItemId

**Chaîne de référence**: `ItemId`
- **Type**: IntProperty
- **Description**: Identifiant unique de l'item
- **Format probable**: `[ItemId][Quantité]`

#### SaveBackPackItem

**Chaîne de référence**: `SaveBackPackItem`
- **Position**: 0x000170B1
- **Type**: StructProperty
- **Description**: Structure complète d'un item dans l'inventaire

### Compétences

#### EquipSupportSkill

**Chaîne de référence**: `EquipSupportSkill`
- **Occurrences**: ~40
- **Type**: Array ou Struct
- **Description**: Compétences de support équipées

**Positions**:
- 0x00087D6B
- 0x000898C6
- 0x0008B421
- etc.

### Armes

#### Types d'armes identifiés

| Type   | Chaîne        | Occurrences |
|--------|---------------|-------------|
| Épée   | `Sword`       | ~160        |
| Épée   | `SwordFixed`  | ~80         |
| Dague  | `Dagger`      | ~160        |
| Dague  | `DaggerFixed` | ~80         |
| Arc    | `Bow`         | ~80         |
| Arc    | `BowFixed`    | ~80         |
| Hache  | `Axe`         | ~80         |
| Hache  | `AxeFixed`    | ~80         |

**Note**: Les versions "Fixed" semblent être des armes uniques ou équipées.

#### PlayerWeapon

**Chaîne de référence**: `PlayerWeapon`
- **Occurrences**: ~50
- **Type**: StructProperty
- **Description**: Arme équipée par le joueur

**Positions**:
- 0x000CC10B
- 0x000CC887
- 0x000CD003
- etc.

### Autres Données

#### BitFlag

**Nom de propriété**: `BitFlag`
- **Type**: ArrayProperty
- **Taille**: 8,196 octets
- **Description**: Drapeaux de bits pour les événements/progression
- **Position**: Début des données de propriétés

#### PlayerLocation

**Chaîne de référence**: `PlayerLocation`
- **Sous-propriétés**:
  - `levelName` (0x000047D9)
  - `levelId` (0x00004861)

#### PartyChatSaveData

**Chaîne de référence**: `PartyChatSaveData`
- **Position**: 0x00005ABB
- **Occurrences**: ~308 occurrences de "party"
- **Type**: Probablement StructProperty ou ArrayProperty

## Format de Propriété UE4

Les propriétés Unreal Engine 4 suivent généralement ce format:

```
[Longueur du nom] (int32)
[Nom de la propriété] (string)
[Longueur du type] (int32)
[Type de la propriété] (string)
[Taille de la valeur] (uint64)
[GUID] (16 bytes)
[Terminateur] (1 byte, généralement 0x00)
[Valeur] (selon le type)
```

### Types de Propriétés

| Type            | Description           | Exemple            |
|-----------------|----------------------|--------------------|
| IntProperty     | Entier 32-bit signé  | -2147483648 à 2147483647 |
| FloatProperty   | Nombre à virgule     | 3.14159           |
| BoolProperty    | Booléen              | true/false        |
| StrProperty     | Chaîne de caractères | "Hello World"     |
| NameProperty    | Nom (comme string)   | "PlayerName"      |
| ArrayProperty   | Tableau d'éléments   | [1, 2, 3, 4]      |
| StructProperty  | Structure complexe   | {a: 1, b: 2}      |
| ByteProperty    | Byte ou Enum         | 0-255 ou enum     |

## Patterns de Données

### Structures Répétitives

Blocs répétés identifiés (potentiellement des tableaux de personnages/items):

| Taille | Répétitions | Description Probable       |
|--------|-------------|----------------------------|
| 32b    | 2,325       | Petites structures         |
| 64b    | 826         | Données de personnage?     |
| 128b   | 244         | Stats complètes?           |
| 256b   | 98          | Items/Équipement?          |
| 512b   | 38          | Structures de personnages? |
| 1024b  | 16          | Grandes structures         |

### Noms de Personnages (probables)

Les 8 personnages jouables d'Octopath Traveler 2:

1. Hikari
2. Osvald
3. Partitio
4. Ochette
5. Castti
6. Throné
7. Temenos
8. Agnea

**Note**: Ces noms n'ont pas encore été localisés dans les sauvegardes analysées.

## Valeurs de Référence

### Niveaux de Personnages

- **Min**: 1
- **Max**: 99
- **Type**: int32
- **Localisation**: Proximité des chaînes "level", "exp", "character"

### Items

- **IDs d'items**: Probablement des entiers séquentiels
- **Quantité max**: Probablement 99 ou 999 par item
- **Format**: `[ItemID (int32)][Quantité (int32)]`

### Jobs

Les jobs dans Octopath Traveler 2 incluent:

**Jobs de base** (8):
1. Warrior (Guerrier)
2. Dancer (Danseur/Danseuse)
3. Merchant (Marchand)
4. Scholar (Érudit)
5. Apothecary (Apothicaire)
6. Thief (Voleur)
7. Hunter (Chasseur)
8. Cleric (Clerc)

**Jobs secondaires** (12):
- Armsmaster
- Arcanist
- Inventor
- Conjurer
- Etc.

**IDs de jobs**: À déterminer (probablement 0-19)

## Modifications Recommandées

### Valeurs Sûres

Pour éviter de corrompre la sauvegarde:

| Donnée | Min Sûr | Max Sûr  | Max Absolu |
|--------|---------|----------|------------|
| HP     | 1       | 9,999    | 99,999     |
| MP     | 1       | 999      | 9,999      |
| EXP    | 0       | 999,999  | 99,999,999 |
| Level  | 1       | 99       | 99         |
| Items  | 0       | 99       | 999        |

### Précautions

1. **Toujours créer un backup** avant modification
2. **Tester avec des valeurs modérées** avant d'aller aux extrêmes
3. **Modifier une sauvegarde à la fois**
4. **Vérifier dans le jeu** après chaque modification majeure

## Zones Non Identifiées

### À Explorer

- [ ] Positions exactes des niveaux de personnages
- [ ] Structure complète de l'inventaire
- [ ] IDs spécifiques des jobs
- [ ] IDs des items
- [ ] IDs des compétences
- [ ] Progression de l'histoire (quêtes, événements)
- [ ] Données de carte (lieux découverts)
- [ ] Succès/Achievements

### Checksum / Validation

**Statut**: Aucun checksum détecté
- Les modifications directes semblent fonctionner sans recalcul de checksum
- À confirmer avec des tests plus approfondis

## Références

- [Unreal Engine Save Game Documentation](https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/SaveGame/)
- [GVAS Format Analysis](https://github.com/13xforever/gvas-converter)

## Changelog

- **2025-10-22**: Documentation initiale basée sur l'analyse de SaveData0.sav
  - Identification des structures HP/MP/EXP
  - Localisation des chaînes d'items et jobs
  - Analyse des patterns répétitifs
