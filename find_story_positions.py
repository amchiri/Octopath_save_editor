#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cherche les positions des variables d'histoire dans le fichier
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("RECHERCHE DES VARIABLES D'HISTOIRE")
print("="*80)

# Cherche les strings identifiées
keywords = [
    b'PlayingMainStoryID',
    b'InterruptedMainStoryID',
    b'MainMissionProgressCnt',
]

for keyword in keywords:
    print(f"\n{'='*80}")
    print(f"Recherche: {keyword.decode('ascii')}")
    print("="*80)
    
    pos = 0
    count = 0
    while True:
        pos = save_data.find(keyword, pos)
        if pos == -1:
            break
        
        count += 1
        print(f"\n{count}. Trouvé @ 0x{pos:08X}")
        
        # Hex dump autour (±32 bytes)
        start = max(0, pos - 32)
        end = min(len(save_data), pos + len(keyword) + 32)
        
        for i in range(start, end, 16):
            hex_bytes = save_data[i:i+16]
            hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
            
            marker = ""
            if i <= pos < i + 16:
                marker = f" <- '{keyword.decode('ascii')}'"
            
            print(f"0x{i:08X}: {hex_str:<48} {ascii_str}{marker}")
        
        # La valeur devrait être après "IntProperty"
        intprop_pos = save_data.find(b'IntProperty', pos, pos + 50)
        if intprop_pos != -1:
            # La valeur est généralement quelques bytes après IntProperty
            # Pattern typique: ...IntProperty\x00[padding][valeur 4 bytes]
            value_pos = intprop_pos + 12  # IntProperty (11) + \x00 (1)
            
            # Cherche le prochain alignement sur 4 bytes
            while value_pos % 4 != 0:
                value_pos += 1
            
            if value_pos + 4 < len(save_data):
                value = struct.unpack('<I', save_data[value_pos:value_pos+4])[0]
                print(f"\n   → Valeur probable @ 0x{value_pos:08X}: {value}")
                
                # Affiche aussi les bytes bruts
                raw_bytes = save_data[value_pos:value_pos+4]
                hex_val = ' '.join(f'{b:02X}' for b in raw_bytes)
                print(f"      Bytes: {hex_val}")
        
        pos += 1
        if count >= 10:  # Limite pour ne pas spammer
            print(f"\n   ... (arrêt après 10 occurrences)")
            break

print("\n" + "="*80)
print("RÉSUMÉ")
print("="*80)
