#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Met Throné et Temenos à 9000 HP bonus
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_9000'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

POSITIONS = {
    'Throné': 0x0008E1C3,
    'Temenos': 0x0008FD1E,
}

save9 = read_save('SaveData/SaveData9.sav')
data9 = bytearray(save9)

print("="*80)
print("THRONÉ → 0 HP BONUS, TEMENOS → 9000 HP BONUS")
print("="*80)

# Met Throné à 0, Temenos à 9000
values = {'Throné': 0, 'Temenos': 9000}

for name, pos in POSITIONS.items():
    val_before = struct.unpack('<H', data9[pos:pos+2])[0]
    struct.pack_into('<H', data9, pos, values[name])
    val_after = struct.unpack('<H', data9[pos:pos+2])[0]
    
    print(f"\n{name}:")
    print(f"  Position: 0x{pos:08X}")
    print(f"  Avant: {val_before} HP bonus")
    print(f"  Après: {val_after} HP bonus")

# Sauvegarde
print("\n" + "="*80)
write_save(Path('SaveData/SaveData9.sav'), bytes(data9))

print("\n✅ Throné: 0 HP bonus, Temenos: 9000 HP bonus!")
print("   Charge SaveData9 dans le jeu et vérifie leur HP max!")
print("   Throné devrait avoir son HP de base, Temenos +9000 HP!")
