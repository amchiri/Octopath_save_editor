#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trouve les AcquisitionFlag où BoolProperty n'est PAS suivi de None
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("RECHERCHE AcquisitionFlag avec BoolProperty != None")
print("="*80)

# Cherche toutes les AcquisitionFlag
keyword = b'AcquisitionFlag'
positions = []

pos = 0
while True:
    pos = save_data.find(keyword, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"\nTrouvé {len(positions)} occurrences de AcquisitionFlag")
print("\nAnalyse des occurrences où BoolProperty n'est PAS suivi de 'None'...\n")

valid_flags = []

for flag_pos in positions[:200]:  # Analyse les 200 premières
    # Cherche BoolProperty après AcquisitionFlag
    bool_pos = save_data.find(b'BoolProperty', flag_pos, flag_pos + 100)
    if bool_pos == -1:
        continue
    
    # Cherche ce qui suit BoolProperty
    check_pos = bool_pos + 12  # len("BoolProperty")
    
    # Regarde les 20 bytes suivants
    following_bytes = save_data[check_pos:check_pos+20]
    
    # Vérifie si c'est "None" ou autre chose
    if not following_bytes.startswith(b'\x00\x04\x00\x00\x00None'):
        # Ce n'est PAS "None" !
        valid_flags.append({
            'flag_pos': flag_pos,
            'bool_pos': bool_pos,
            'check_pos': check_pos,
            'following': following_bytes[:10]
        })

print(f"✅ Trouvé {len(valid_flags)} AcquisitionFlag avec BoolProperty != None\n")

# Affiche les premiers
for i, item in enumerate(valid_flags[:50], 1):
    print("="*80)
    print(f"#{i} - AcquisitionFlag @ 0x{item['flag_pos']:08X}")
    print("="*80)
    
    # Hex dump autour
    start = item['flag_pos']
    end = item['check_pos'] + 30
    
    for addr in range(start, end, 16):
        hex_bytes = save_data[addr:addr+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if addr <= item['flag_pos'] < addr + 16:
            marker = " <- AcquisitionFlag"
        elif addr <= item['bool_pos'] < addr + 16:
            marker = " <- BoolProperty"
        elif addr <= item['check_pos'] < addr + 16:
            marker = " <- Valeur?"
        
        print(f"0x{addr:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Cherche la valeur booléenne
    # Pattern probable: BoolProperty\x00[padding][valeur 1 byte]
    value_search_start = item['bool_pos'] + 12
    value_search_end = value_search_start + 20
    
    # Cherche le premier 00 ou 01 après BoolProperty
    for v_pos in range(value_search_start, value_search_end):
        val = save_data[v_pos]
        if val == 0 or val == 1:
            status = "✅ TRUE" if val == 1 else "❌ FALSE"
            print(f"\n→ Valeur booléenne probable @ 0x{v_pos:08X}: {val} ({status})")
            break
    
    print()

print("="*80)
print(f"TOTAL: {len(valid_flags)} flags trouvés")
print("="*80)
