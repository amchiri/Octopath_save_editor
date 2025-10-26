#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compare les positions dans le backup original vs ce qu'on vient de modifier
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

# Les positions ORIGINALES qu'on avait trouvées
original_positions = [
    {'pos': 0x0008FD1E, 'name': 'Zone 53 (Temenos)', 'expected': 1425},
    {'pos': 0x000933D4, 'name': 'Zone 54 (Throne)', 'expected': 9075},
]

# Charge le backup ORIGINAL (avant toute modification)
save6_original = read_save('SaveData/SaveData6.sav.backup_v3')

print("="*80)
print("VÉRIFICATION DES POSITIONS ORIGINALES")
print("="*80)

for pos_info in original_positions:
    pos = pos_info['pos']
    val = struct.unpack('<H', save6_original[pos:pos+2])[0]
    
    print(f"\n{pos_info['name']} @ 0x{pos:08X}")
    print(f"  Valeur dans backup original: {val}")
    print(f"  Valeur attendue: {pos_info['expected']}")
    print(f"  {'✅ OK!' if val == pos_info['expected'] else '❌ PAS BON!'}")
    
    # Hex dump
    print(f"\n  Hex dump:")
    for i in range(pos-16, pos+32, 16):
        if 0 <= i < len(save6_original):
            hex_data = ' '.join(f'{b:02X}' for b in save6_original[i:i+16])
            ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in save6_original[i:i+16])
            marker = ' <--' if i <= pos < i+16 else ''
            print(f"    0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

# Maintenant vérifions ce qu'on a modifié
print("\n" + "="*80)
print("POSITIONS MODIFIÉES PAR LE SCRIPT")
print("="*80)

modified_positions = [
    {'name': 'Temenos', 'pos': 0x0008FD1A},
    {'name': 'Castti', 'pos': 0x000933D0},
]

save6_current = read_save('SaveData/SaveData6.sav')

for pos_info in modified_positions:
    pos = pos_info['pos']
    val = struct.unpack('<H', save6_current[pos:pos+2])[0]
    
    print(f"\n{pos_info['name']} @ 0x{pos:08X}")
    print(f"  Valeur actuelle: {val}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("Il y a un décalage de 4 bytes!")
print("  Position originale Temenos: 0x0008FD1E")
print("  Position trouvée par script: 0x0008FD1A (4 bytes avant!)")
print("")
print("  Position originale Throne: 0x000933D4")
print("  Position trouvée par script: 0x000933D0 (4 bytes avant!)")
