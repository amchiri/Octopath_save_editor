#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse la zone "Endroll_ClearedMS" qui semble être les chapitres complétés!
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("ANALYSE: Endroll_ClearedMS (Chapitres complétés?)")
print("="*80)

# Position trouvée
pos = 0x000E33F5

print(f"\n'Endroll_ClearedMS' @ 0x{pos:08X}\n")

# Hex dump large autour
start = pos - 64
end = pos + 200

for addr in range(start, end, 16):
    hex_bytes = save_data[addr:addr+16]
    hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
    
    marker = ""
    if addr <= pos < addr + 16:
        marker = " <- Endroll_ClearedMS"
    
    print(f"0x{addr:08X}: {hex_str:<48} {ascii_str}{marker}")

# C'est un ArrayProperty, cherche les valeurs
array_pos = save_data.find(b'ArrayProperty', pos, pos + 30)
if array_pos != -1:
    print(f"\n✅ ArrayProperty trouvé @ 0x{array_pos:08X}")
    
    # Après ArrayProperty, il y a généralement le type d'élément puis les données
    # Pattern: ArrayProperty\x00[size 4 bytes][type]...
    
    data_start = array_pos + 14  # "ArrayProperty\x00"
    
    # Lit le nombre d'éléments (peut être à data_start ou après padding)
    array_size_pos = data_start + 16  # Souvent après padding
    
    print(f"\nRecherche des données du tableau...")
    
    # Affiche les 100 bytes suivants
    print(f"\nDonnées après ArrayProperty:")
    for i in range(0, 100, 16):
        addr = array_pos + 14 + i
        hex_bytes = save_data[addr:addr+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        print(f"  0x{addr:08X}: {hex_str:<48} {ascii_str}")
    
    # Cherche IntProperty après (les éléments du tableau)
    intprop_pos = save_data.find(b'IntProperty', array_pos, array_pos + 100)
    if intprop_pos != -1:
        print(f"\n✅ IntProperty trouvé @ 0x{intprop_pos:08X}")
        print("    → Le tableau contient des Int!")
        
        # Les valeurs sont après IntProperty
        values_start = intprop_pos + 20  # Approximatif
        
        print(f"\nValeurs possibles (Int32):")
        for i in range(10):
            val_pos = values_start + (i * 4)
            if val_pos + 4 < len(save_data):
                val = struct.unpack('<I', save_data[val_pos:val_pos+4])[0]
                if val < 1000:  # Filtre les grandes valeurs
                    print(f"  Position +{i*4:3}: 0x{val_pos:08X} = {val}")

print("\n" + "="*80)
print("Si ce sont les chapitres complétés, on devrait voir:")
print("  - Un tableau d'IDs de chapitres")
print("  - Des valeurs 1-40 environ (8 persos × 5 chapitres)")
print("="*80)
