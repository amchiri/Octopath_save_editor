#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Approche différente: Comparer SaveData avec progression différente
Si vous avez une sauvegarde où Temenos est au chapitre 1 vs chapitre 2,
on peut trouver ce qui change!
"""

import struct
from pathlib import Path

print("="*80)
print("MÉTHODE DE RECHERCHE DES FLAGS D'HISTOIRE")
print("="*80)

print("\nPOUR TROUVER LES FLAGS D'HISTOIRE, J'AI BESOIN DE:")
print("\n1. DEUX SAUVEGARDES avec progression différente")
print("   Par exemple:")
print("   - SaveDataA: Temenos chapitre 1 non complété")
print("   - SaveDataB: Temenos chapitre 1 complété (ou chapitre 2)")
print("\n2. Comparer les différences entre les deux fichiers")
print("   Les flags qui changent = progression d'histoire!")

print("\n" + "="*80)
print("AUTRE MÉTHODE - CHERCHER DES PATTERNS:")
print("="*80)

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Zone connue de Temenos (autour du HP bonus)
TEMENOS_ZONE_START = 0x0008E000
TEMENOS_ZONE_END = 0x00090000

print(f"\nAnalyse de la zone Temenos (0x{TEMENOS_ZONE_START:08X} - 0x{TEMENOS_ZONE_END:08X})")

# Cherche des strings qui pourraient être des IDs de quêtes/chapitres
print("\nSTRINGS dans la zone Temenos:")

strings_found = []
current_string = bytearray()
string_start = None

for pos in range(TEMENOS_ZONE_START, TEMENOS_ZONE_END):
    byte = save_data[pos]
    
    if 32 <= byte < 127 or byte == ord('_'):  # Caractère imprimable
        if string_start is None:
            string_start = pos
        current_string.append(byte)
    else:
        if len(current_string) >= 5:  # String d'au moins 5 caractères
            try:
                text = current_string.decode('ascii')
                if any(keyword in text.lower() for keyword in ['chapter', 'story', 'quest', 'complete', 'flag', 'progress']):
                    strings_found.append({
                        'pos': string_start,
                        'text': text
                    })
            except:
                pass
        current_string = bytearray()
        string_start = None

if strings_found:
    print("\n✅ STRINGS INTÉRESSANTES TROUVÉES:")
    for s in strings_found[:20]:  # Limite à 20
        print(f"  0x{s['pos']:08X}: '{s['text']}'")
else:
    print("\n❌ Aucune string de chapitre/histoire trouvée")
    print("   Les flags doivent être des IDs numériques!")

# Cherche des valeurs 1-5 (chapitres potentiels)
print("\n" + "="*80)
print("VALEURS 1-5 dans la zone (chapitres potentiels):")
print("="*80)

chapter_candidates = []
for pos in range(TEMENOS_ZONE_START, TEMENOS_ZONE_END):
    val = save_data[pos]
    if 1 <= val <= 5:
        # Regarde le contexte autour
        before = save_data[max(0, pos-4):pos]
        after = save_data[pos+1:pos+5]
        
        # Si entouré de beaucoup de 0x00, c'est probablement un flag
        if before.count(0) >= 2 or after.count(0) >= 2:
            chapter_candidates.append({'pos': pos, 'val': val})

print(f"\nTrouvé {len(chapter_candidates)} positions avec valeurs 1-5:")
for i, c in enumerate(chapter_candidates[:30]):  # Limite à 30
    hex_around = ' '.join(f'{b:02X}' for b in save_data[c['pos']-2:c['pos']+3])
    print(f"{i+1:3}. 0x{c['pos']:08X}: [{hex_around}] = {c['val']}")

print("\n" + "="*80)
print("RECOMMANDATION:")
print("Pour identifier précisément les flags d'histoire, le plus")
print("efficace serait de me fournir DEUX sauvegardes:")
print("  - Une au début de l'histoire de Temenos")
print("  - Une après avoir avancé d'un chapitre")
print("Je comparerai les différences pour trouver exactement")
print("où sont stockés les flags de progression!")
print("="*80)
