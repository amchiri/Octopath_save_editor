#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche des flags d'histoire/chapitres pour Temenos
On va chercher des patterns de compteurs/flags autour de sa position
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Positions connues pour Temenos
TEMENOS_HP_CURRENT = 0x0008E4D4
TEMENOS_HP_BONUS = 0x0008FD1E

print("="*80)
print("RECHERCHE FLAGS D'HISTOIRE - TEMENOS")
print("="*80)

print("\nPOSITIONS CONNUES:")
print(f"  HP actuel:  0x{TEMENOS_HP_CURRENT:08X}")
print(f"  HP bonus:   0x{TEMENOS_HP_BONUS:08X}")

# Cherche le nom "Temenos" dans le fichier
temenos_name = b'Temenos\x00'
print("\n" + "="*80)
print("RECHERCHE DU NOM 'Temenos':")
print("="*80)

pos = 0
count = 0
while True:
    pos = save_data.find(temenos_name, pos)
    if pos == -1:
        break
    
    count += 1
    print(f"\n{count}. 'Temenos' trouvé @ 0x{pos:08X}")
    
    # Affiche les données autour
    print(f"   Hex dump (±64 bytes):")
    start = max(0, pos - 64)
    end = min(len(save_data), pos + 64)
    
    for i in range(start, end, 16):
        hex_bytes = save_data[i:i+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if i <= pos < i + 16:
            marker = " <- 'Temenos'"
        
        print(f"   0x{i:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Cherche des patterns intéressants après le nom
    print("\n   ANALYSE des 100 bytes APRÈS le nom:")
    
    # Cherche des mots-clés liés aux chapitres/histoire
    keywords = [
        (b'Chapter', 'Chapter'),
        (b'Story', 'Story'),
        (b'Progress', 'Progress'),
        (b'Quest', 'Quest'),
        (b'Flag', 'Flag'),
        (b'Complete', 'Complete'),
        (b'Level', 'Level'),
    ]
    
    search_start = pos
    search_end = min(len(save_data), pos + 200)
    
    for keyword, name in keywords:
        kw_pos = save_data.find(keyword, search_start, search_end)
        if kw_pos != -1:
            distance = kw_pos - pos
            print(f"   ✅ '{name}' trouvé à +{distance} bytes (0x{kw_pos:08X})")
    
    # Cherche des petits entiers (1-8 pour chapitres)
    print("\n   Valeurs uint8 dans les 50 bytes suivants:")
    for offset in range(8, 50, 1):
        check_pos = pos + offset
        if check_pos < len(save_data):
            val = save_data[check_pos]
            if 0 <= val <= 8:  # Chapitres possibles (1-5 ou 1-8?)
                print(f"   Offset +{offset:2}: {val} @ 0x{check_pos:08X}")
    
    pos += 1
    if count >= 3:  # Limite à 3 occurrences pour ne pas trop spammer
        break

print("\n" + "="*80)
print("SUGGESTIONS:")
print("1. Chercher des patterns de compteurs 0-5 ou 0-8 (chapitres)")
print("2. Chercher des flags booléens autour du nom")
print("3. Comparer deux saves avec chapitres différents")
print("="*80)
