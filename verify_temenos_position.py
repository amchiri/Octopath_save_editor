#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérifie si les positions sont correctes en comparant avec SaveData6 backup original
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

# Position Temenos
pos_temenos = 0x0008FD1E

# Charge les différentes versions
save9_original = read_save('SaveData/SaveData9.sav.backup2')  # Original avec 0 HP bonus
save9_current = read_save('SaveData/SaveData9.sav')  # Vient d'être modifié à 9000

print("="*80)
print("VÉRIFICATION POSITION TEMENOS")
print("="*80)

# Lit les valeurs
val_save9_orig = struct.unpack('<H', save9_original[pos_temenos:pos_temenos+2])[0]
val_save9 = struct.unpack('<H', save9_current[pos_temenos:pos_temenos+2])[0]

print(f"\nPosition Temenos: 0x{pos_temenos:08X}")
print(f"  SaveData9 (backup original): {val_save9_orig} HP bonus")
print(f"  SaveData9 (modifié):         {val_save9} HP bonus")

if val_save9_orig == 0:
    print(f"\n✅ Position correcte dans SaveData9 original (0 trouvé)")
else:
    print(f"\n⚠️  SaveData9 original avait: {val_save9_orig}")

if val_save9 == 9000:
    print(f"✅ Modification réussie dans SaveData9 (9000 écrit)")
else:
    print(f"❌ Modification échouée! Attendu 9000, trouvé {val_save9}")

# Hex dump des deux
print(f"\n{'='*80}")
print("HEX DUMP SAVEDATA9 ORIGINAL @ 0x{:08X}:".format(pos_temenos))
print(f"{'='*80}")
for i in range(pos_temenos-16, pos_temenos+32, 16):
    if 0 <= i < len(save9_original):
        hex_data = ' '.join(f'{b:02X}' for b in save9_original[i:i+16])
        ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in save9_original[i:i+16])
        marker = ' <--' if i <= pos_temenos < i+16 else ''
        print(f"  0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

print(f"\n{'='*80}")
print("HEX DUMP SAVEDATA9 MODIFIÉ @ 0x{:08X}:".format(pos_temenos))
print(f"{'='*80}")
for i in range(pos_temenos-16, pos_temenos+32, 16):
    if 0 <= i < len(save9_current):
        hex_data = ' '.join(f'{b:02X}' for b in save9_current[i:i+16])
        ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in save9_current[i:i+16])
        marker = ' <--' if i <= pos_temenos < i+16 else ''
        print(f"  0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

print(f"\n{'='*80}")
print("DIAGNOSTIC")
print(f"{'='*80}")
print("Si les deux positions sont correctes mais que le jeu ne montre pas +9000 HP,")
print("alors peut-être:")
print("  1. Le jeu calcule le HP max autrement (via équipement/level)")
print("  2. Il faut sauvegarder/recharger dans le jeu")
print("  3. Il y a un autre mécanisme qu'on n'a pas encore trouvé")
