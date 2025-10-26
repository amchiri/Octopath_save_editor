#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cherche les blocs de flags avec TRUE (chapitres complétés)
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Trouve tous les AcquisitionFlag avec valeurs
keyword = b'AcquisitionFlag'
bool_keyword = b'BoolProperty'

flags = []
pos = 0

while True:
    pos = save_data.find(keyword, pos)
    if pos == -1:
        break
    
    bool_pos = save_data.find(bool_keyword, pos, pos + 100)
    if bool_pos != -1:
        search_start = bool_pos + 13
        search_end = search_start + 50
        
        for check_pos in range(search_start, search_end):
            val = save_data[check_pos]
            if val in [0, 1]:
                next_bytes = save_data[check_pos:check_pos+4]
                if all(b in [0, 1] for b in next_bytes):
                    flags.append({
                        'flag_pos': pos,
                        'value_pos': check_pos,
                        'value': val
                    })
                    break
    
    pos += 1

print("="*80)
print("CHERCHE LES BLOCS AVEC CHAPITRES COMPLÉTÉS (TRUE)")
print("="*80)

BLOCK_SIZE = 45
num_blocks = len(flags) // BLOCK_SIZE

print(f"\nTotal: {len(flags)} flags en {num_blocks} blocs\n")

# Trouve les blocs avec au moins 1 TRUE
blocks_with_true = []

for block_idx in range(num_blocks):
    start_idx = block_idx * BLOCK_SIZE
    end_idx = start_idx + BLOCK_SIZE
    block_flags = flags[start_idx:end_idx]
    
    true_count = sum(1 for f in block_flags if f['value'] == 1)
    
    if true_count > 0:
        blocks_with_true.append({
            'block_idx': block_idx,
            'start_idx': start_idx,
            'end_idx': end_idx,
            'true_count': true_count,
            'flags': block_flags
        })

print(f"✅ Trouvé {len(blocks_with_true)} blocs avec au moins 1 TRUE\n")

# Affiche ces blocs
for block in blocks_with_true[:10]:  # Limite à 10
    print("="*80)
    print(f"BLOC #{block['block_idx'] + 1} (flags {block['start_idx']}-{block['end_idx']})")
    print(f"  TRUE: {block['true_count']}/{len(block['flags'])}")
    print("="*80)
    
    # Affiche les valeurs
    values_str = ''.join('1' if f['value'] == 1 else '0' for f in block['flags'])
    
    for i in range(0, len(values_str), 15):
        line = values_str[i:i+15]
        print(f"  Flags {i:2}-{min(i+14, len(values_str)-1):2}: {' '.join(line)}")
    
    # Plage d'adresses
    first_flag = block['flags'][0]['flag_pos']
    last_flag = block['flags'][-1]['flag_pos']
    print(f"\n  Plage: 0x{first_flag:08X} - 0x{last_flag:08X}")
    
    # Cherche HP proche pour identifier le personnage
    search_start = max(0, first_flag - 3000)
    search_end = min(len(save_data), last_flag + 3000)
    
    hp_pos = save_data.find(b'RawHP', search_start, search_end)
    if hp_pos != -1:
        hp_value_pos = hp_pos - 8
        if hp_value_pos >= 0:
            hp = struct.unpack('<I', save_data[hp_value_pos:hp_value_pos+4])[0]
            print(f"  → HP proche: {hp}")
            if hp == 878:
                print(f"     🎯 TEMENOS!")
            elif hp == 600:
                print(f"     🎯 THRONÉ!")
    
    print()

print("="*80)
