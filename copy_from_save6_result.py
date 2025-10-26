#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copie TOUTES les valeurs de DopingParam de SaveData6_result vers SaveData9
SaveData6_result a les bonus HP qui fonctionnent, on copie tout!
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_copy_from_6'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

# Positions des compteurs HP bonus pour les 8 personnages
POSITIONS_HP_BONUS = [
    {'name': 'Hikari', 'pos': 0x00081171},
    {'name': 'Agnea', 'pos': 0x00088FB2},
    {'name': 'Partitio', 'pos': 0x0008AB0D},
    {'name': 'Osvald', 'pos': 0x0008C668},
    {'name': 'Throné', 'pos': 0x0008E1C3},
    {'name': 'Temenos', 'pos': 0x0008FD1E},
    {'name': 'Ochette', 'pos': 0x00091879},
    {'name': 'Castti', 'pos': 0x000933D4},
]

save6_result = read_save('SaveData/SaveData6_result.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("COPIE DES COMPTEURS HP BONUS: SaveData6_result → SaveData9")
print("="*80)

# Lit d'abord les valeurs de SaveData6_result
print("\nVALEURS DANS SaveData6_result (qui fonctionne):")
for pos_info in POSITIONS_HP_BONUS:
    val = struct.unpack('<H', save6_result[pos_info['pos']:pos_info['pos']+2])[0]
    print(f"  {pos_info['name']:10} @ 0x{pos_info['pos']:08X}: {val:5} HP bonus")

# Copie vers SaveData9
data9 = bytearray(save9)

for pos_info in POSITIONS_HP_BONUS:
    # Lit la valeur dans SaveData6_result
    val_from_6 = struct.unpack('<H', save6_result[pos_info['pos']:pos_info['pos']+2])[0]
    
    # Écrit dans SaveData9
    struct.pack_into('<H', data9, pos_info['pos'], val_from_6)

# Vérifie
print("\nVALEURS COPIÉES DANS SaveData9:")
for pos_info in POSITIONS_HP_BONUS:
    val = struct.unpack('<H', data9[pos_info['pos']:pos_info['pos']+2])[0]
    print(f"  {pos_info['name']:10} @ 0x{pos_info['pos']:08X}: {val:5} HP bonus")

# Sauvegarde
print("\n" + "="*80)
write_save(Path('SaveData/SaveData9.sav'), bytes(data9))

print("\n✅ Compteurs HP bonus copiés de SaveData6_result vers SaveData9!")
print("   Charge SaveData9 dans le jeu et vérifie si ça fonctionne maintenant!")
