#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copie directement les bonnes valeurs de SaveData6 vers SaveData9
aux positions EXACTES identifiées
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = filepath + '.backup_v2'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

# Positions EXACTES trouvées
positions = [
    {'pos': 0x0008FD1E, 'name': 'Zone 53 (Temenos)', 'value_save6': 1425},
    {'pos': 0x000933D4, 'name': 'Zone 54 (Throne?)', 'value_save6': 9075},
]

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("COPIE DIRECTE SaveData6 → SaveData9")
print("="*80)

# Modifie SaveData9
data9 = bytearray(save9)

for pos_info in positions:
    pos = pos_info['pos']
    
    # Lit la valeur dans SaveData6
    val6 = struct.unpack('<H', save6[pos:pos+2])[0]
    
    # Lit la valeur actuelle dans SaveData9
    val9_before = struct.unpack('<H', data9[pos:pos+2])[0]
    
    # Écrit la valeur de Save6 dans Save9
    struct.pack_into('<H', data9, pos, val6)
    
    # Vérifie
    val9_after = struct.unpack('<H', data9[pos:pos+2])[0]
    
    print(f"\n{pos_info['name']} @ 0x{pos:08X}")
    print(f"  SaveData6: {val6}")
    print(f"  SaveData9 avant: {val9_before}")
    print(f"  SaveData9 après: {val9_after}")
    print(f"  {'✅ Copié!' if val9_after == val6 else '❌ Échec!'}")

# Sauvegarde
print("\n" + "="*80)
save9_path = Path('SaveData/SaveData9.sav')
write_save(str(save9_path), bytes(data9))

print("\n✅ SaveData9 modifié! Charge-le dans le jeu et vérifie le HP max!")
