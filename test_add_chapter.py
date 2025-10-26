#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test: Ajoute le chapitre 1 (ID=1) à la liste des chapitres complétés
"""

import struct
from pathlib import Path
import shutil

save_path = Path('SaveData/SaveData9.sav')
save_data = open(save_path, 'rb').read()

print("="*80)
print("TEST: AJOUT DU CHAPITRE ID=1 À LA LISTE")
print("="*80)

# Position du tableau Endroll_ClearedMS
ARRAY_START = 0x000E3428  # Première valeur (26)

# Lit les valeurs actuelles
print("\nVALEURS ACTUELLES:")
current_values = []
for i in range(10):
    pos = ARRAY_START + (i * 4)
    val = struct.unpack('<I', save_data[pos:pos+4])[0]
    if val != 0xFFFFFFFF:  # Pas -1 (vide)
        current_values.append(val)
        print(f"  Position {i}: {val} (0x{val:02X})")
    else:
        print(f"  Position {i}: VIDE (0xFFFFFFFF)")
        if len(current_values) >= 5:  # Arrête après avoir listé les valeurs réelles
            break

print(f"\n✅ Total: {len(current_values)} chapitres complétés")

# Remplace la première valeur VIDE par 1
data = bytearray(save_data)

# Cherche le premier 0xFFFFFFFF
first_empty_pos = None
for i in range(50):  # Cherche dans les 50 premières positions
    pos = ARRAY_START + (i * 4)
    val = struct.unpack('<I', save_data[pos:pos+4])[0]
    if val == 0xFFFFFFFF:
        first_empty_pos = pos
        first_empty_idx = i
        break

if first_empty_pos:
    print(f"\n✅ Première position vide trouvée: position {first_empty_idx} @ 0x{first_empty_pos:08X}")
    print(f"   Modification: 0xFFFFFFFF → 1 (chapitre ID=1)")
    
    # Écrit la valeur 1
    struct.pack_into('<I', data, first_empty_pos, 1)
    
    # Backup et sauvegarde
    backup_path = str(save_path) + '.backup_chapter_test'
    shutil.copy(save_path, backup_path)
    print(f"\n✅ Backup: {backup_path}")
    
    with open(save_path, 'wb') as f:
        f.write(data)
    print(f"✅ Sauvegarde modifiée: {save_path}")
    
    # Vérifie
    print("\nVÉRIFICATION:")
    new_val = struct.unpack('<I', data[first_empty_pos:first_empty_pos+4])[0]
    print(f"  Nouvelle valeur @ 0x{first_empty_pos:08X}: {new_val}")
    
    print("\n" + "="*80)
    print("TEST À FAIRE:")
    print("1. Charge SaveData9 dans le jeu")
    print("2. Vérifie si un nouveau chapitre apparaît comme 'complété'")
    print("3. Note QUEL chapitre/personnage correspond à l'ID=1")
    print("="*80)
else:
    print("\n❌ Aucune position vide trouvée!")

print("\n" + "="*80)
print("EXPLICATION:")
print("Si ça fonctionne, on saura que:")
print("  - Endroll_ClearedMS = liste des chapitres complétés")
print("  - Les IDs correspondent à: (personnage × 5) + chapitre")
print("  - On pourra créer un éditeur complet!")
print("="*80)
