#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cherche les variables de chapitres COMPLÉTÉS
(pas en cours, mais terminés)
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("RECHERCHE VARIABLES DE CHAPITRES COMPLÉTÉS")
print("="*80)

# Cherche autour de la zone Temenos
TEMENOS_HP = 0x0008E4D4
TEMENOS_STORY_ZONE_START = TEMENOS_HP - 1000
TEMENOS_STORY_ZONE_END = TEMENOS_HP + 2000

print(f"\nZone Temenos: 0x{TEMENOS_STORY_ZONE_START:08X} - 0x{TEMENOS_STORY_ZONE_END:08X}")

# Mots-clés liés aux chapitres complétés
keywords = [
    (b'Complete', 'Complete'),
    (b'Completed', 'Completed'),
    (b'Cleared', 'Cleared'),
    (b'Finished', 'Finished'),
    (b'Chapter', 'Chapter'),
    (b'Story', 'Story'),
    (b'MainStory', 'MainStory'),
    (b'Mission', 'Mission'),
    (b'Progress', 'Progress'),
    (b'Clear', 'Clear'),
]

print("\nSTRINGS TROUVÉES DANS LA ZONE TEMENOS:")
print("="*80)

found_keywords = []

for keyword, name in keywords:
    pos = TEMENOS_STORY_ZONE_START
    while pos < TEMENOS_STORY_ZONE_END:
        pos = save_data.find(keyword, pos, TEMENOS_STORY_ZONE_END)
        if pos == -1:
            break
        
        found_keywords.append({
            'keyword': name,
            'pos': pos,
            'keyword_bytes': keyword
        })
        pos += 1

# Trie par position
found_keywords.sort(key=lambda x: x['pos'])

for item in found_keywords:
    print(f"\n'{item['keyword']}' @ 0x{item['pos']:08X}")
    
    # Affiche le contexte
    start = max(0, item['pos'] - 32)
    end = min(len(save_data), item['pos'] + len(item['keyword_bytes']) + 48)
    
    for i in range(start, end, 16):
        hex_bytes = save_data[i:i+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if i <= item['pos'] < i + 16:
            marker = f" <- '{item['keyword']}'"
        
        print(f"  0x{i:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Cherche IntProperty après
    intprop_pos = save_data.find(b'IntProperty', item['pos'], item['pos'] + 50)
    if intprop_pos != -1:
        value_pos = intprop_pos + 12
        while value_pos % 4 != 0:
            value_pos += 1
        
        if value_pos + 4 < len(save_data):
            value = struct.unpack('<I', save_data[value_pos:value_pos+4])[0]
            print(f"  → Valeur @ 0x{value_pos:08X}: {value}")

print("\n" + "="*80)
print("Si rien n'est trouvé, cherchons des COMPTEURS (1-8)...")
print("="*80)

# Cherche des valeurs 1-5 près de CharacterID ou Level
characterid_keyword = b'CharacterID'
pos = save_data.find(characterid_keyword, TEMENOS_STORY_ZONE_START, TEMENOS_STORY_ZONE_END)

if pos != -1:
    print(f"\n'CharacterID' trouvé @ 0x{pos:08X}")
    
    # Cherche des compteurs dans les 200 bytes AVANT CharacterID
    search_start = max(0, pos - 200)
    search_end = pos
    
    print(f"Recherche de compteurs 1-5 entre 0x{search_start:08X} et 0x{search_end:08X}:")
    
    for check_pos in range(search_start, search_end):
        val = save_data[check_pos]
        if 1 <= val <= 5:
            # Contexte
            hex_around = ' '.join(f'{b:02X}' for b in save_data[check_pos-4:check_pos+5])
            print(f"  0x{check_pos:08X}: [{hex_around}] = {val}")
