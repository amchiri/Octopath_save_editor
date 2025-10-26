#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lit correctement les AcquisitionFlag
Pattern trouvé: valeur booléenne à +96 bytes après "AcquisitionFlag"
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Distance entre AcquisitionFlag et sa valeur
VALUE_OFFSET = 96  # bytes

print("="*80)
print("LECTURE DES AcquisitionFlag")
print("="*80)

# Trouve tous les AcquisitionFlag
keyword = b'AcquisitionFlag'
flags = []

pos = 0
while True:
    pos = save_data.find(keyword, pos)
    if pos == -1:
        break
    
    value_pos = pos + VALUE_OFFSET
    if value_pos < len(save_data):
        value = save_data[value_pos]
        flags.append({
            'flag_pos': pos,
            'value_pos': value_pos,
            'value': value
        })
    
    pos += 1

print(f"\nTrouvé {len(flags)} AcquisitionFlag")

# Groupe par blocs de 45 (probablement 1 personnage = 45 flags)
BLOCK_SIZE = 45
num_blocks = len(flags) // BLOCK_SIZE

print(f"Nombre de blocs de {BLOCK_SIZE}: {num_blocks}")

# Analyse chaque bloc
for block_idx in range(min(10, num_blocks)):  # Limite à 10 blocs
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
    
    print(f"\n  Plage adresses: 0x{block_flags[0]['flag_pos']:08X} - 0x{block_flags[-1]['flag_pos']:08X}")

print("\n" + "="*80)
print("RÉSUMÉ:")
print(f"Total de {len(flags)} flags")
print(f"Organisés en blocs de {BLOCK_SIZE} flags (probablement 1 bloc = 1 personnage)")
print("="*80)
