#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trouve TOUTES les positions HP actuelles en cherchant RawMP
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Cherche toutes les occurrences de "RawMP"
mp_keyword = b'RawMP'
positions = []

pos = 0
while True:
    pos = save_data.find(mp_keyword, pos)
    if pos == -1:
        break
    
    # HP est 8 bytes AVANT "RawMP"
    hp_pos = pos - 8
    if hp_pos >= 0:
        hp_value = struct.unpack('<I', save_data[hp_pos:hp_pos+4])[0]
        positions.append({'hp_pos': hp_pos, 'hp_value': hp_value, 'mp_pos': pos})
    
    pos += 1

print("="*80)
print(f"POSITIONS HP ACTUELLES (trouvé {len(positions)} occurrences de RawMP)")
print("="*80)

for i, p in enumerate(positions, 1):
    print(f"{i:2}. HP actuel @ 0x{p['hp_pos']:08X} = {p['hp_value']:5} HP")
