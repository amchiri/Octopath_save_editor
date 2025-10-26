#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trouve TOUTES les positions DopingParam HP exactes
en cherchant le pattern complet
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

# Charge SaveData6 original (backup)
save6 = read_save('SaveData/SaveData6.sav.backup_v3')

print("="*80)
print("RECHERCHE DE TOUTES LES POSITIONS DOPING HP")
print("="*80)

# On sait que les positions sont avant "MP" dans les sections DopingParam
# Pattern précis: [2 bytes HP bonus][00 00][03 00 00 00]"MP\x00"

positions_found = []

# Cherche tous les "MP" markers
pos = 0
while True:
    mp_pos = save6.find(b'\x03\x00\x00\x00MP\x00', pos)
    if mp_pos == -1:
        break
    
    # La valeur HP bonus est 8 bytes avant
    hp_bonus_pos = mp_pos - 8
    
    if hp_bonus_pos >= 0:
        # Vérifie qu'il y a bien "DopingParam" avant (dans les 200 bytes)
        search_start = max(0, hp_bonus_pos - 200)
        context = save6[search_start:hp_bonus_pos]
        
        if b'DopingParam' in context:
            hp_bonus = struct.unpack('<H', save6[hp_bonus_pos:hp_bonus_pos+2])[0]
            
            # Vérifie aussi qu'il y a "HP" avant "MP"
            hp_marker_pos = save6.rfind(b'\x03\x00\x00\x00HP\x00', hp_bonus_pos - 50, hp_bonus_pos)
            
            if hp_marker_pos != -1:
                positions_found.append({
                    'pos': hp_bonus_pos,
                    'bonus': hp_bonus,
                    'nuts': hp_bonus // 75 if hp_bonus > 0 else 0
                })
    
    pos = mp_pos + 1

print(f"\n✅ Trouvé {len(positions_found)} positions DopingParam HP:\n")

characters = ['Hikari', 'Agnea', 'Partitio', 'Osvald', 'Throné', 'Temenos', 'Ochette', 'Castti']

for idx, pos_info in enumerate(positions_found):
    char_name = characters[idx] if idx < 8 else f"Personnage {idx+1}"
    print(f"{idx+1}. {char_name:10} @ 0x{pos_info['pos']:08X}: "
          f"{pos_info['bonus']:5} HP bonus ({pos_info['nuts']} nuts)")

if len(positions_found) >= 8:
    print("\n" + "="*80)
    print("CODE POUR L'ÉDITEUR:")
    print("="*80)
    print("positions_hp_bonus = [")
    for idx, pos_info in enumerate(positions_found[:8]):
        char_name = characters[idx]
        print(f"    {{'name': '{char_name}', 'pos': 0x{pos_info['pos']:08X}}},")
    print("]")
