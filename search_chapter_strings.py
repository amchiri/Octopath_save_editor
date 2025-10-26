#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cherche tous les strings intéressants liés aux chapitres/histoire
"""

import re
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("RECHERCHE DE STRINGS LIÉS AUX CHAPITRES/HISTOIRE")
print("="*80)

# Mots-clés à chercher
keywords = [
    # Chapitres
    b'Chapter', b'chapter', b'CHAPTER',
    # Histoire
    b'Story', b'story', b'STORY',
    b'MainStory', b'mainstory',
    # Progression
    b'Progress', b'progress',
    b'Complete', b'complete', b'Completed', b'completed',
    b'Clear', b'clear', b'Cleared', b'cleared',
    b'Finish', b'finish', b'Finished', b'finished',
    # Missions
    b'Quest', b'quest', b'Mission', b'mission',
    # Numéros de chapitres possibles
    b'Ch1', b'Ch2', b'Ch3', b'Ch4', b'Ch5',
    b'CH1', b'CH2', b'CH3', b'CH4', b'CH5',
    b'Ch_1', b'Ch_2', b'Ch_3', b'Ch_4', b'Ch_5',
    # Status
    b'Status', b'status', b'State', b'state',
    b'Flag', b'flag', b'Flags', b'flags',
    # Étapes
    b'Step', b'step', b'Stage', b'stage', b'Phase', b'phase',
]

found_strings = {}

for keyword in keywords:
    positions = []
    pos = 0
    while True:
        pos = save_data.find(keyword, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1
    
    if positions:
        found_strings[keyword.decode('ascii', errors='ignore')] = positions[:20]  # Max 20 occurrences

# Affiche les résultats
print(f"\n✅ Trouvé {len(found_strings)} mots-clés différents\n")

for keyword, positions in sorted(found_strings.items(), key=lambda x: len(x[1]), reverse=True):
    count = len(positions)
    print(f"\n{'='*80}")
    print(f"'{keyword}': {count} occurrences")
    print("="*80)
    
    # Affiche les 5 premières occurrences avec contexte
    for i, pos in enumerate(positions[:5], 1):
        print(f"\n  #{i} @ 0x{pos:08X}")
        
        # Context: 50 bytes avant et après
        start = max(0, pos - 50)
        end = min(len(save_data), pos + len(keyword) + 50)
        
        context = save_data[start:end]
        
        # Cherche des strings lisibles autour
        # Pattern: suite de caractères imprimables de 3+ caractères
        readable = re.findall(b'[\x20-\x7E]{3,}', context)
        
        if readable:
            print(f"     Context: {' | '.join(s.decode('ascii', errors='ignore') for s in readable[:5])}")
        
        # Affiche le hex dump court
        hex_short = ' '.join(f'{b:02X}' for b in save_data[pos:pos+16])
        print(f"     Hex: {hex_short}")

print("\n" + "="*80)
print("RECHERCHE DE PATTERNS NUMÉRIQUES")
print("="*80)

# Cherche des patterns comme "Chapter_1", "Story_2", etc.
print("\nRecherche de patterns avec numéros (1-8)...")

for num in range(1, 9):
    patterns = [
        f'Chapter{num}'.encode(),
        f'Chapter_{num}'.encode(),
        f'Chapter {num}'.encode(),
        f'Story{num}'.encode(),
        f'Story_{num}'.encode(),
        f'Story {num}'.encode(),
        f'Quest{num}'.encode(),
        f'Quest_{num}'.encode(),
        f'Mission{num}'.encode(),
        f'Mission_{num}'.encode(),
    ]
    
    for pattern in patterns:
        pos = save_data.find(pattern)
        if pos != -1:
            print(f"  ✅ Trouvé '{pattern.decode('ascii')}' @ 0x{pos:08X}")

print("\n" + "="*80)
print("SUGGESTIONS POUR IDENTIFIER LES CHAPITRES:")
print("="*80)
print("""
1. Cherche des compteurs 1-5 ou 0-4 (pour 5 chapitres par personnage)
2. Cherche des variables comme 'CurrentChapter', 'ChapterID', etc.
3. Compare deux sauvegardes pour voir ce qui change
4. Les chapitres sont peut-être stockés comme des IDs numériques dans
   les variables PlayingMainStoryID / MainMissionProgressCnt
""")
