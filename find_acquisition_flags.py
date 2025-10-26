#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cherche et analyse les AcquisitionFlag (flags de chapitres débloqués)
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("RECHERCHE DES AcquisitionFlag")
print("="*80)

# Cherche AcquisitionFlag
keyword = b'AcquisitionFlag'
positions = []

pos = 0
count = 0
while True:
    pos = save_data.find(keyword, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1
    count += 1

print(f"\nTrouvé {count} occurrences de 'AcquisitionFlag'")

# Groupe par zone (probablement 8 personnages avec plusieurs flags chacun)
print("\n" + "="*80)
print("ANALYSE DES ZONES AcquisitionFlag:")
print("="*80)

# Groupe les positions proches ensemble
zones = []
current_zone = []
last_pos = None

for pos in positions[:100]:  # Limite à 100 premières
    if last_pos is None or pos - last_pos < 1000:
        current_zone.append(pos)
    else:
        if current_zone:
            zones.append(current_zone)
        current_zone = [pos]
    last_pos = pos

if current_zone:
    zones.append(current_zone)

print(f"\nTrouvé {len(zones)} zones de AcquisitionFlag")

for zone_idx, zone in enumerate(zones[:10], 1):  # Limite à 10 zones
    print(f"\n{'='*80}")
    print(f"ZONE #{zone_idx}: {len(zone)} flags")
    print(f"Plage: 0x{zone[0]:08X} - 0x{zone[-1]:08X}")
    print("="*80)
    
    # Analyse les flags dans cette zone
    print("\nFlags dans cette zone:")
    for i, flag_pos in enumerate(zone[:10], 1):  # Limite à 10 flags par zone
        # Cherche BoolProperty après AcquisitionFlag
        bool_pos = save_data.find(b'BoolProperty', flag_pos, flag_pos + 50)
        if bool_pos != -1:
            # La valeur booléenne est après BoolProperty
            # Pattern: BoolProperty\x00[padding][valeur 1 byte]
            value_pos = bool_pos + 13  # BoolProperty (12) + \x00 (1)
            
            # Aligne sur 4 bytes
            while value_pos % 4 != 0:
                value_pos += 1
            
            if value_pos < len(save_data):
                bool_value = save_data[value_pos]
                status = "✅ TRUE" if bool_value else "❌ FALSE"
                print(f"  Flag {i:2} @ 0x{flag_pos:08X} → 0x{value_pos:08X}: {status}")
    
    if len(zone) > 10:
        print(f"  ... ({len(zone) - 10} autres flags)")
    
    # Cherche CharacterID ou HP près de cette zone pour identifier le personnage
    search_start = max(0, zone[0] - 500)
    search_end = min(len(save_data), zone[0] + 500)
    
    # Cherche HP
    hp_keyword = b'RawHP'
    hp_pos = save_data.find(hp_keyword, search_start, search_end)
    if hp_pos != -1:
        hp_value_pos = hp_pos - 8
        if hp_value_pos >= 0:
            hp = struct.unpack('<I', save_data[hp_value_pos:hp_value_pos+4])[0]
            print(f"\n  → HP proche: {hp}")
            if hp == 878:
                print(f"     🎯 C'EST TEMENOS!")
            elif hp == 600:
                print(f"     🎯 C'EST THRONÉ!")

print("\n" + "="*80)
print("CONCLUSION:")
print("Chaque personnage a plusieurs AcquisitionFlag (probablement 1 par chapitre)")
print("Mettre un flag à TRUE = débloquer/compléter ce chapitre")
print("="*80)
