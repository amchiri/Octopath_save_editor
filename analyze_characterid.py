#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse détaillée autour de CharacterID pour chaque personnage
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("ANALYSE AUTOUR DE CharacterID POUR TOUS LES PERSONNAGES")
print("="*80)

# Cherche toutes les occurrences de CharacterID
characterid_keyword = b'CharacterID'
positions = []

pos = 0
while True:
    pos = save_data.find(characterid_keyword, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"\nTrouvé {len(positions)} occurrences de 'CharacterID'")
print("\nAnalyse des 8 premières (les 8 personnages):\n")

for i, pos in enumerate(positions[:8], 1):
    print("="*80)
    print(f"PERSONNAGE #{i} - CharacterID @ 0x{pos:08X}")
    print("="*80)
    
    # Hex dump autour
    start = max(0, pos - 32)
    end = min(len(save_data), pos + 80)
    
    for addr in range(start, end, 16):
        hex_bytes = save_data[addr:addr+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if addr <= pos < addr + 16:
            marker = " <- CharacterID"
        
        print(f"0x{addr:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Trouve la valeur IntProperty après CharacterID
    intprop_pos = save_data.find(b'IntProperty', pos, pos + 30)
    if intprop_pos != -1:
        value_pos = intprop_pos + 12
        while value_pos % 4 != 0:
            value_pos += 1
        
        if value_pos + 4 < len(save_data):
            char_id = struct.unpack('<I', save_data[value_pos:value_pos+4])[0]
            print(f"\n→ CharacterID value @ 0x{value_pos:08X}: {char_id}")
    
    # Cherche Level après
    level_pos = save_data.find(b'Level', pos, pos + 100)
    if level_pos != -1:
        intprop_pos2 = save_data.find(b'IntProperty', level_pos, level_pos + 30)
        if intprop_pos2 != -1:
            value_pos2 = intprop_pos2 + 12
            while value_pos2 % 4 != 0:
                value_pos2 += 1
            
            if value_pos2 + 4 < len(save_data):
                level = struct.unpack('<I', save_data[value_pos2:value_pos2+4])[0]
                print(f"→ Level @ 0x{value_pos2:08X}: {level}")
    
    # Cherche HP
    hp_pos = save_data.find(b'RawHP', pos, pos + 200)
    if hp_pos != -1:
        hp_value_pos = hp_pos - 8
        if hp_value_pos >= 0:
            hp = struct.unpack('<I', save_data[hp_value_pos:hp_value_pos+4])[0]
            print(f"→ HP @ 0x{hp_value_pos:08X}: {hp}")
    
    print()

print("="*80)
print("IDENTIFICATION:")
print("Temenos devrait avoir HP = 878")
print("Throné devrait avoir HP = 600")
print("="*80)
