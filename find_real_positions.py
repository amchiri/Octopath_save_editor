#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche les VRAIES positions des compteurs HP bonus
On sait que:
- Temenos: 0x0008FD1E ✅ (confirmé)
- Throné: 0x000933D4 ✅ (confirmé, c'était l'adresse de Castti!)
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Positions qu'on PENSAIT avoir
OLD_POSITIONS = [
    {'name': 'Hikari', 'pos': 0x00081171},
    {'name': 'Agnea', 'pos': 0x00088FB2},
    {'name': 'Partitio', 'pos': 0x0008AB0D},
    {'name': 'Osvald', 'pos': 0x0008C668},
    {'name': 'Throné', 'pos': 0x0008E1C3},   # ❌ FAUX! Vraie: 0x000933D4
    {'name': 'Temenos', 'pos': 0x0008FD1E},  # ✅ CORRECT!
    {'name': 'Ochette', 'pos': 0x00091879},
    {'name': 'Castti', 'pos': 0x000933D4},   # ❌ FAUX! C'était Throné!
]

print("="*80)
print("VÉRIFICATION DES POSITIONS")
print("="*80)

print("\nPOSITIONS CONFIRMÉES:")
print("  Temenos: 0x0008FD1E ✅")
print("  Throné:  0x000933D4 ✅ (c'était l'ancienne position de Castti!)")

print("\n" + "="*80)
print("RECHERCHE DU PATTERN AUTOUR DE TEMENOS (qui fonctionne):")
print("="*80)

# Analyse autour de Temenos pour trouver le pattern
temenos_pos = 0x0008FD1E
print(f"\nHex dump autour de Temenos @ 0x{temenos_pos:08X}:")
for offset in range(-32, 32, 16):
    pos = temenos_pos + offset
    hex_bytes = save_data[pos:pos+16]
    hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
    
    marker = ""
    if pos == temenos_pos:
        marker = " <- Temenos HP bonus"
    
    print(f"0x{pos:08X}: {hex_str}{marker}")

# Cherche "MP" qui devrait être après le compteur HP
print("\n" + "="*80)
print("RECHERCHE DE 'MP' APRÈS TEMENOS:")
search_start = temenos_pos
search_end = temenos_pos + 20
mp_pos = save_data.find(b'MP\x00', search_start, search_end)
if mp_pos != -1:
    distance = mp_pos - temenos_pos
    print(f"✅ Trouvé 'MP' à 0x{mp_pos:08X} (distance: {distance} bytes après HP bonus)")
else:
    print("❌ 'MP' non trouvé dans les 20 bytes suivants")

# Maintenant analyse Throné
throne_pos = 0x000933D4
print("\n" + "="*80)
print(f"HEX DUMP AUTOUR DE THRONÉ @ 0x{throne_pos:08X}:")
print("="*80)
for offset in range(-32, 32, 16):
    pos = throne_pos + offset
    hex_bytes = save_data[pos:pos+16]
    hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
    
    marker = ""
    if pos == throne_pos:
        marker = " <- Throné HP bonus"
    
    print(f"0x{pos:08X}: {hex_str}{marker}")

# Cherche "MP" après Throné
search_start = throne_pos
search_end = throne_pos + 20
mp_pos = save_data.find(b'MP\x00', search_start, search_end)
if mp_pos != -1:
    distance = mp_pos - throne_pos
    print(f"\n✅ Trouvé 'MP' à 0x{mp_pos:08X} (distance: {distance} bytes après HP bonus)")
else:
    print("\n❌ 'MP' non trouvé dans les 20 bytes suivants")

print("\n" + "="*80)
print("CONCLUSION:")
print("Si on trouve le même pattern (distance au 'MP'), on peut")
print("rechercher tous les 'MP' et trouver les vraies positions!")
print("="*80)
