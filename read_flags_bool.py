#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lit les valeurs booléennes directement après BoolProperty
Pattern: AcquisitionFlag → BoolProperty → [padding] → valeur
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("LECTURE DES AcquisitionFlag (méthode BoolProperty)")
print("="*80)

# Trouve tous les AcquisitionFlag qui sont suivis de BoolProperty
keyword = b'AcquisitionFlag'
bool_keyword = b'BoolProperty'

flags = []
pos = 0

while True:
    pos = save_data.find(keyword, pos)
    if pos == -1:
        break
    
    # Cherche BoolProperty dans les 100 bytes suivants
    bool_pos = save_data.find(bool_keyword, pos, pos + 100)
    if bool_pos != -1:
        # La valeur est après Bool Property\x00 avec padding
        # Cherche le pattern: après BoolProperty, skip jusqu'au prochain 00 ou 01
        search_start = bool_pos + 13  # "BoolProperty\x00"
        search_end = search_start + 50
        
        # Cherche les bytes 00 ou 01
        for check_pos in range(search_start, search_end):
            val = save_data[check_pos]
            # Regarde si c'est un pattern de booléens (00 ou 01 répétés)
            if val in [0, 1]:
                # Vérifie que les prochains bytes sont aussi 00/01
                next_bytes = save_data[check_pos:check_pos+4]
                if all(b in [0, 1] for b in next_bytes):
                    flags.append({
                        'flag_pos': pos,
                        'bool_pos': bool_pos,
                        'value_pos': check_pos,
                        'value': val
                    })
                    break
    
    pos += 1

print(f"\nTrouvé {len(flags)} AcquisitionFlag avec valeurs")

# Groupe par blocs
BLOCK_SIZE = 45
num_blocks = len(flags) // BLOCK_SIZE

print(f"Nombre de blocs de {BLOCK_SIZE}: {num_blocks}")

# Analyse les premiers blocs
for block_idx in range(min(10, num_blocks)):
    start_idx = block_idx * BLOCK_SIZE
    end_idx = start_idx + BLOCK_SIZE
    block_flags = flags[start_idx:end_idx]
    
    true_count = sum(1 for f in block_flags if f['value'] == 1)
    false_count = sum(1 for f in block_flags if f['value'] == 0)
    
    print(f"\n{'='*80}")
    print(f"BLOC #{block_idx + 1} (flags {start_idx}-{end_idx})")
    print(f"  TRUE: {true_count}, FALSE: {false_count}")
    print("="*80)
    
    # Affiche les valeurs
    values_str = ''.join('1' if f['value'] == 1 else '0' for f in block_flags[:45])
    
    # Affiche par ligne de 15
    for i in range(0, len(values_str), 15):
        line = values_str[i:i+15]
        print(f"  Flags {i:2}-{i+14:2}: {' '.join(line)}")
    
    # Affiche quelques positions pour debug
    if block_idx < 2:
        print(f"\n  Exemples de positions:")
        for i in [0, 1, 14, 29, 44]:
            if i < len(block_flags):
                f = block_flags[i]
                print(f"    Flag {i:2}: value=0x{f['value_pos']:08X} (={f['value']})")

print("\n" + "="*80)
