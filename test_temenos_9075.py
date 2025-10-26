#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Met 9075 HP bonus pour Temenos dans SaveData6
(même bonus que Throné)
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = filepath + '.backup_test'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

# Position de Temenos
temenos_pos = 0x0008FD1E
throne_pos = 0x000933D4

save6 = read_save('SaveData/SaveData6.sav')

print("="*80)
print("TEST: 9075 HP BONUS POUR TEMENOS")
print("="*80)

# Modifie SaveData6
data6 = bytearray(save6)

# Lit les valeurs actuelles
temenos_before = struct.unpack('<H', data6[temenos_pos:temenos_pos+2])[0]
throne_before = struct.unpack('<H', data6[throne_pos:throne_pos+2])[0]

print(f"\nAVANT:")
print(f"  Temenos @ 0x{temenos_pos:08X}: {temenos_before} HP bonus ({temenos_before//75} nuts)")
print(f"  Throné  @ 0x{throne_pos:08X}: {throne_before} HP bonus ({throne_before//75} nuts)")

# Met 9075 pour Temenos
struct.pack_into('<H', data6, temenos_pos, 9075)

# Vérifie
temenos_after = struct.unpack('<H', data6[temenos_pos:temenos_pos+2])[0]
throne_after = struct.unpack('<H', data6[throne_pos:throne_pos+2])[0]

print(f"\nAPRÈS:")
print(f"  Temenos @ 0x{temenos_pos:08X}: {temenos_after} HP bonus ({temenos_after//75} nuts)")
print(f"  Throné  @ 0x{throne_pos:08X}: {throne_after} HP bonus ({throne_after//75} nuts)")

if temenos_after == 9075:
    print(f"\n✅ Temenos modifié: {temenos_before} → {temenos_after} HP bonus")
else:
    print(f"\n❌ Échec de la modification!")

# Sauvegarde
print("\n" + "="*80)
save6_path = Path('SaveData/SaveData6.sav')
write_save(str(save6_path), bytes(data6))

print("\n✅ SaveData6 modifié!")
print("   Charge-le dans le jeu et vérifie le HP max de Temenos!")
print("   Il devrait avoir le même HP max que Throné maintenant.")
