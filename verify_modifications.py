#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérifie les positions EXACTES trouvées dans SaveData6 vs ce qu'on a modifié dans SaveData9
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("VÉRIFICATION DES POSITIONS EXACTES")
print("="*80)

# Positions exactes trouvées dans l'analyse précédente
zones = [
    {
        'name': 'Zone 53 (Temenos)',
        'pos': 0x0008FD1E,
        'expected_save6': 1425,
        'expected_save9_before': 0
    },
    {
        'name': 'Zone 54 (Throne?)',
        'pos': 0x000933D4,
        'expected_save6': 9075,
        'expected_save9_before': 0
    }
]

for zone in zones:
    pos = zone['pos']
    
    print(f"\n{zone['name']} @ 0x{pos:08X}")
    
    # Lit la valeur actuelle
    val6 = struct.unpack('<H', save6[pos:pos+2])[0]
    val9_current = struct.unpack('<H', save9[pos:pos+2])[0]
    
    print(f"  SaveData6:        {val6} (attendu: {zone['expected_save6']})")
    print(f"  SaveData9 actuel: {val9_current}")
    
    if val6 == zone['expected_save6']:
        print(f"  ✅ SaveData6 OK")
    else:
        print(f"  ❌ SaveData6 ne correspond pas!")
    
    if val9_current == 9075:
        print(f"  ✅ SaveData9 a été modifié à 9075 (121 nuts)")
    elif val9_current == 0:
        print(f"  ❌ SaveData9 est toujours à 0 - modification n'a pas marché!")
    
    # Contexte
    print(f"\n  Hex dump SaveData9 @ 0x{pos:08X}:")
    for i in range(pos-16, pos+32, 16):
        if 0 <= i < len(save9):
            hex_data = ' '.join(f'{b:02X}' for b in save9[i:i+16])
            ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in save9[i:i+16])
            marker = ' <--' if i <= pos < i+16 else ''
            print(f"    0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

print("\n" + "="*80)
print("RECHERCHE: Où l'éditeur a-t-il écrit?")
print("="*80)

# Cherche toutes les valeurs 9075 (0x2373) dans SaveData9
target = 9075
found_positions = []

for pos in range(0, len(save9) - 2):
    val = struct.unpack('<H', save9[pos:pos+2])[0]
    if val == target:
        found_positions.append(pos)

print(f"\nTrouvé {len(found_positions)} occurrence(s) de la valeur 9075 dans SaveData9:")
for pos in found_positions[:20]:  # Max 20
    # Contexte
    ctx = save9[max(0, pos-20):min(len(save9), pos+30)]
    strings = []
    current = b''
    for byte in ctx:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    context = ', '.join(strings[:3]) if strings else '(binary)'
    print(f"  0x{pos:08X}: {context}")
