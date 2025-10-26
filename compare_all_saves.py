#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse: Quelle save permet d'accéder aux Nourishing Nuts?
Comparons SaveData6, SaveData9, et SaveData9_9nutshell
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def find_nuts_quantity(data):
    """Trouve la quantité de Nourishing Nuts (ItemId 2045)"""
    pos = 0
    while True:
        none_pos = data.find(b'None\x00', pos)
        if none_pos == -1:
            break
        
        search_end = min(none_pos + 30, len(data))
        itemid_pos = data.find(b'ItemId\x00', none_pos, search_end)
        
        if itemid_pos != -1:
            qty_pos = none_pos - 8
            if qty_pos >= 0:
                quantity = struct.unpack('<I', data[qty_pos:qty_pos+4])[0]
                itemid_value_pos = qty_pos + 49
                if itemid_value_pos + 4 <= len(data):
                    itemid = struct.unpack('<I', data[itemid_value_pos:itemid_value_pos+4])[0]
                    
                    if itemid == 2045:
                        return {'qty': quantity, 'pos': qty_pos}
        
        pos = none_pos + 1
    
    return None

def check_doping_values(data, name):
    """Vérifie les valeurs aux positions DopingParam"""
    positions = [0x0008FD1E, 0x000933D4]
    
    print(f"\n{name}:")
    for pos in positions:
        val = struct.unpack('<H', data[pos:pos+2])[0]
        print(f"  @ 0x{pos:08X}: {val}")

print("="*80)
print("ANALYSE: Quelle save donne accès aux Nourishing Nuts?")
print("="*80)

# Liste toutes les saves
saves = [
    ('SaveData6', 'SaveData/SaveData6.sav'),
    ('SaveData9', 'SaveData/SaveData9.sav'),
    ('SaveData9_9nutshell', 'SaveData/SaveData9_9nutshell.sav'),
]

for name, path in saves:
    try:
        data = read_save(path)
        nuts = find_nuts_quantity(data)
        
        print(f"\n{'='*80}")
        print(f"{name}")
        print(f"{'='*80}")
        print(f"Taille: {len(data)} bytes")
        
        if nuts:
            print(f"Nourishing Nuts: {nuts['qty']} @ 0x{nuts['pos']:08X}")
        else:
            print("Nourishing Nuts: NON TROUVÉ")
        
        check_doping_values(data, "Valeurs DopingParam")
        
    except FileNotFoundError:
        print(f"\n{name}: ❌ Fichier non trouvé")

print("\n" + "="*80)
print("QUESTIONS:")
print("="*80)
print("1. Dans quelle(s) save(s) peux-tu accéder aux Nourishing Nuts dans le jeu?")
print("2. Quelle est la vraie différence entre une save où tu peux accéder")
print("   aux nuts et une où tu ne peux pas?")
