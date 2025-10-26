#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TEST: Met Hikari à 100 HP bonus (= 1 Nourishing Nut si +100 HP par nut)
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_test2'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

POSITIONS = {
    'Hikari': 0x00081171,
    'Throné': 0x0008E1C3,
    'Temenos': 0x0008FD1E,
}

save6 = read_save('SaveData/SaveData6.sav')
data6 = bytearray(save6)

print("="*80)
print("TEST: 100 HP bonus pour Hikari, 9075 pour Temenos")
print("="*80)

# Met Hikari à 100 HP bonus (= 1 nut si +100 HP/nut)
struct.pack_into('<H', data6, POSITIONS['Hikari'], 100)

# Garde Temenos à 9075 pour comparer
struct.pack_into('<H', data6, POSITIONS['Temenos'], 9075)

# Vérifie
hikari_val = struct.unpack('<H', data6[POSITIONS['Hikari']:POSITIONS['Hikari']+2])[0]
temenos_val = struct.unpack('<H', data6[POSITIONS['Temenos']:POSITIONS['Temenos']+2])[0]

print(f"\nHikari  @ 0x{POSITIONS['Hikari']:08X}: {hikari_val} HP bonus")
print(f"Temenos @ 0x{POSITIONS['Temenos']:08X}: {temenos_val} HP bonus")

# Sauvegarde
write_save(Path('SaveData/SaveData6.sav'), bytes(data6))

print("\n" + "="*80)
print("INSTRUCTIONS:")
print("="*80)
print("1. Charge SaveData6 dans le jeu")
print("2. Note le HP MAX de Hikari (devrait être HP_BASE + 100)")
print("3. Note le HP MAX de Temenos (devrait être HP_BASE + 9075)")
print("4. Vérifie si la différence correspond à 1 nut vs beaucoup de nuts!")
