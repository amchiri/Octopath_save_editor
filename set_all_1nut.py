#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Met TOUS les personnages à 100 HP bonus (= 1 Nourishing Nut)
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_all_1nut'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

# Positions corrigées (+4 bytes)
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

save9 = read_save('SaveData/SaveData9.sav')
data9 = bytearray(save9)

print("="*80)
print("TOUS LES PERSONNAGES → 100 HP BONUS (1 NOURISHING NUT)")
print("="*80)

# Met tous à 100 HP bonus
for pos_info in POSITIONS_HP_BONUS:
    struct.pack_into('<H', data9, pos_info['pos'], 100)

# Vérifie et affiche
print("\nVALEURS MODIFIÉES:")
for pos_info in POSITIONS_HP_BONUS:
    val = struct.unpack('<H', data9[pos_info['pos']:pos_info['pos']+2])[0]
    print(f"  {pos_info['name']:10} @ 0x{pos_info['pos']:08X}: {val} HP bonus")

# Sauvegarde
print("\n" + "="*80)
write_save(Path('SaveData/SaveData9.sav'), bytes(data9))

print("\n✅ Tous les personnages ont maintenant 100 HP bonus (= 1 nut)")
print("   Charge SaveData9 dans le jeu et vérifie leur HP max!")
