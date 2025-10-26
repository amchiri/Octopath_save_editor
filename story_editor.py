#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
STORY PROGRESSION EDITOR
Trouve et modifie:
- PlayingMainStoryID (ID de l'histoire en cours)
- InterruptedMainStoryID (ID de l'histoire interrompue)
- MainMissionProgressCnt (compteur de progression)
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_story'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Sauvegardé: {filepath}")

def find_story_properties(data):
    """Trouve toutes les occurrences des propriétés d'histoire"""
    
    properties = [
        b'PlayingMainStoryID\x00',
        b'InterruptedMainStoryID\x00',
        b'MainMissionProgressCnt\x00',
    ]
    
    results = []
    
    for prop_name in properties:
        pos = 0
        while True:
            pos = data.find(prop_name, pos)
            if pos == -1:
                break
            
            prop_str = prop_name.decode('ascii').rstrip('\x00')
            
            # La valeur IntProperty est généralement 8-20 bytes après le nom
            # Pattern: [Nom]\x00...[Type]\x00...[Valeur 4 bytes]
            
            # Cherche "IntProperty" après le nom
            int_prop_pos = data.find(b'IntProperty\x00', pos, pos + 50)
            
            if int_prop_pos != -1:
                # La valeur est généralement 8-16 bytes après "IntProperty"
                # Essayons plusieurs offsets
                for offset in [8, 12, 16, 20]:
                    value_pos = int_prop_pos + offset
                    if value_pos + 4 <= len(data):
                        value = struct.unpack('<I', data[value_pos:value_pos+4])[0]
                        
                        results.append({
                            'name': prop_str,
                            'name_pos': pos,
                            'value_pos': value_pos,
                            'value': value
                        })
                        break
            
            pos += 1
    
    return results

save_path = Path('SaveData/SaveData9.sav')
save_data = read_save(save_path)

print("="*80)
print("STORY PROGRESSION EDITOR")
print("="*80)

print("\nRecherche des propriétés d'histoire...")
results = find_story_properties(save_data)

if not results:
    print("❌ Aucune propriété trouvée!")
    exit()

print(f"\n✅ Trouvé {len(results)} propriétés:\n")

# Groupe par type de propriété
from collections import defaultdict
grouped = defaultdict(list)
for r in results:
    grouped[r['name']].append(r)

for prop_name, instances in grouped.items():
    print(f"\n{prop_name}:")
    for i, inst in enumerate(instances, 1):
        print(f"  {i}. @ 0x{inst['value_pos']:08X} = {inst['value']}")

print("\n" + "="*80)
print("CONTEXTE AUTOUR DE LA PREMIÈRE OCCURRENCE:")
print("="*80)

if results:
    first = results[0]
    pos = first['name_pos']
    
    print(f"\nHex dump @ 0x{pos:08X} (±64 bytes):")
    start = max(0, pos - 64)
    end = min(len(save_data), pos + 128)
    
    for i in range(start, end, 16):
        hex_bytes = save_data[i:i+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if i <= pos < i + 16:
            marker = " <- Property name"
        elif i <= first['value_pos'] < i + 16:
            marker = " <- Value"
        
        print(f"0x{i:08X}: {hex_str:<48} {ascii_str}{marker}")

print("\n" + "="*80)
print("INSTRUCTIONS:")
print("Vérifiez les valeurs ci-dessus et indiquez:")
print("1. Quelle occurrence correspond à quel personnage")
print("2. Les nouvelles valeurs souhaitées (ex: changer MainMissionProgressCnt)")
print("="*80)
