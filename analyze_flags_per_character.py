#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse les AcquisitionFlag pour chaque personnage
en se basant sur leur position HP
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Positions HP connues (8 personnages)
HP_POSITIONS = [
    {'name': 'Perso 1', 'hp_pos': 0x00087768, 'hp': 0},
    {'name': 'Perso 2', 'hp_pos': 0x000892C3, 'hp': 0},
    {'name': 'Perso 3', 'hp_pos': 0x0008AE1E, 'hp': 0},
    {'name': 'Perso 4', 'hp_pos': 0x0008C979, 'hp': 0},
    {'name': 'Temenos', 'hp_pos': 0x0008E4D4, 'hp': 878},
    {'name': 'Perso 6', 'hp_pos': 0x0009002F, 'hp': 0},
    {'name': 'Throné', 'hp_pos': 0x00091B8A, 'hp': 600},
    {'name': 'Perso 8', 'hp_pos': 0x000936E5, 'hp': 0},
]

print("="*80)
print("ANALYSE DES AcquisitionFlag PAR PERSONNAGE")
print("="*80)

for char in HP_POSITIONS:
    if char['hp'] == 0:
        continue  # Ignore les personnages sans HP
    
    print(f"\n{'='*80}")
    print(f"{char['name'].upper()} (HP={char['hp']} @ 0x{char['hp_pos']:08X})")
    print("="*80)
    
    # Cherche AcquisitionFlag dans une zone autour du HP
    # Les flags sont probablement AVANT les stats HP
    search_start = max(0, char['hp_pos'] - 5000)
    search_end = char['hp_pos']
    
    # Trouve tous les AcquisitionFlag dans cette zone
    flags = []
    pos = search_start
    while pos < search_end:
        pos = save_data.find(b'AcquisitionFlag', pos, search_end)
        if pos == -1:
            break
        flags.append(pos)
        pos += 1
    
    print(f"\nTrouvé {len(flags)} AcquisitionFlag dans la zone")
    
    if len(flags) > 0:
        print(f"Plage: 0x{flags[0]:08X} - 0x{flags[-1]:08X}")
        
        # Analyse les valeurs des flags
        true_count = 0
        false_count = 0
        flag_values = []
        
        for i, flag_pos in enumerate(flags, 1):
            # Cherche BoolProperty après AcquisitionFlag
            bool_pos = save_data.find(b'BoolProperty', flag_pos, flag_pos + 50)
            if bool_pos != -1:
                # La valeur booléenne est après BoolProperty
                value_pos = bool_pos + 13  # BoolProperty (12) + \x00 (1)
                
                # Aligne sur 4 bytes
                while value_pos % 4 != 0:
                    value_pos += 1
                
                if value_pos < len(save_data):
                    bool_value = save_data[value_pos]
                    flag_values.append({
                        'index': i,
                        'flag_pos': flag_pos,
                        'value_pos': value_pos,
                        'value': bool_value
                    })
                    
                    if bool_value:
                        true_count += 1
                    else:
                        false_count += 1
        
        print(f"\nSTATISTIQUES:")
        print(f"  ✅ TRUE:  {true_count}")
        print(f"  ❌ FALSE: {false_count}")
        print(f"  Total:   {len(flag_values)}")
        
        # Affiche les premiers flags TRUE
        print(f"\nPremiers flags TRUE (probablement chapitres complétés):")
        true_flags = [f for f in flag_values if f['value']]
        for f in true_flags[:10]:
            print(f"  Flag {f['index']:3} @ 0x{f['flag_pos']:08X} → TRUE")
        
        if len(true_flags) > 10:
            print(f"  ... ({len(true_flags) - 10} autres flags TRUE)")
        
        # Affiche les premiers flags FALSE
        print(f"\nPremiers flags FALSE:")
        false_flags = [f for f in flag_values if not f['value']]
        for f in false_flags[:5]:
            print(f"  Flag {f['index']:3} @ 0x{f['flag_pos']:08X} → FALSE")
        
        if len(false_flags) > 5:
            print(f"  ... ({len(false_flags) - 5} autres flags FALSE)")

print("\n" + "="*80)
print("ANALYSE:")
print("Si Throné a fait 4 chapitres, elle devrait avoir ~4 flags TRUE")
print("Si Temenos a fait 1 chapitre, il devrait avoir ~1 flag TRUE")
print("(Mais il peut y avoir d'autres flags pour quêtes secondaires, etc.)")
print("="*80)
