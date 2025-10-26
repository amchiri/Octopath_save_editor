#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecteur/Éditeur d'AcquisitionFlag (chapitres débloqués)
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Positions HP pour identifier les personnages
CHARACTERS = [
    {'name': 'Temenos', 'hp_pos': 0x0008E4D4, 'hp': 878},
    {'name': 'Throné', 'hp_pos': 0x00091B8A, 'hp': 600},
]

print("="*80)
print("LECTURE DES AcquisitionFlag")
print("="*80)

for char in CHARACTERS:
    print(f"\n{'='*80}")
    print(f"{char['name'].upper()} (HP={char['hp']})")
    print("="*80)
    
    # Zone de recherche
    search_start = char['hp_pos'] - 5000
    search_end = char['hp_pos']
    
    # Trouve tous les AcquisitionFlag
    flags = []
    pos = search_start
    while pos < search_end:
        pos = save_data.find(b'AcquisitionFlag', pos, search_end)
        if pos == -1:
            break
        flags.append(pos)
        pos += 1
    
    print(f"\nTrouvé {len(flags)} AcquisitionFlag")
    
    if len(flags) > 0:
        # Pattern: La valeur bool est à +64 bytes après "AcquisitionFlag"
        # (après ArrayProperty + BoolProperty)
        BOOL_OFFSET = 64
        
        print(f"\nVALEURS DES FLAGS:")
        
        true_indices = []
        false_indices = []
        
        for i, flag_pos in enumerate(flags, 1):
            value_pos = flag_pos + BOOL_OFFSET
            
            if value_pos < len(save_data):
                bool_value = save_data[value_pos]
                
                if bool_value:
                    true_indices.append(i)
                else:
                    false_indices.append(i)
                
                status = "✅ TRUE" if bool_value else "❌ FALSE"
                
                # Affiche seulement les 10 premiers
                if i <= 10:
                    print(f"  Flag {i:2} @ 0x{value_pos:08X}: {status}")
        
        if len(flags) > 10:
            print(f"  ... ({len(flags) - 10} autres flags)")
        
        print(f"\nSTATISTIQUES:")
        print(f"  ✅ TRUE:  {len(true_indices)}")
        print(f"  ❌ FALSE: {len(false_indices)}")
        
        if true_indices:
            print(f"\nIndices TRUE: {true_indices[:15]}")
            if len(true_indices) > 15:
                print(f"              ... et {len(true_indices) - 15} autres")
        
        if false_indices:
            print(f"\nIndices FALSE: {false_indices[:10]}")
            if len(false_indices) > 10:
                print(f"               ... et {len(false_indices) - 10} autres")

print("\n" + "="*80)
print("ANALYSE:")
print("Les premiers flags TRUE sont probablement les chapitres principaux!")
print("Pour débloquer un chapitre: mettre le flag correspondant à 01 (TRUE)")
print("="*80)
