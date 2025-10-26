#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Met les compteurs DopingParam à 0 dans SaveData6
pour débloquer l'accès aux Nourishing Nuts
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = filepath + '.backup_v3'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

# Positions EXACTES
positions = [
    {'pos': 0x0008FD1E, 'name': 'Zone 53 (Temenos)'},
    {'pos': 0x000933D4, 'name': 'Zone 54 (Throne)'},
]

save6 = read_save('SaveData/SaveData6.sav')

print("="*80)
print("RESET DES COMPTEURS DOPING → 0 (SaveData6)")
print("="*80)

# Modifie SaveData6
data6 = bytearray(save6)

for pos_info in positions:
    pos = pos_info['pos']
    
    # Lit la valeur actuelle
    val_before = struct.unpack('<H', data6[pos:pos+2])[0]
    
    # Met à 0
    struct.pack_into('<H', data6, pos, 0)
    
    # Vérifie
    val_after = struct.unpack('<H', data6[pos:pos+2])[0]
    
    print(f"\n{pos_info['name']} @ 0x{pos:08X}")
    print(f"  Avant: {val_before}")
    print(f"  Après: {val_after}")
    print(f"  {'✅ Reset à 0!' if val_after == 0 else '❌ Échec!'}")

# Sauvegarde
print("\n" + "="*80)
save6_path = Path('SaveData/SaveData6.sav')
write_save(str(save6_path), bytes(data6))

print("\n✅ SaveData6 modifié!")
print("   Charge-le dans le jeu et vérifie si tu peux maintenant")
print("   accéder aux Nourishing Nuts!")
