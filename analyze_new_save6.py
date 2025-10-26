#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse de la NOUVELLE SaveData6 (modifiée à 20:35)
Compare avec SaveData9 pour trouver les différences
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def find_character_hp_positions(data):
    """Trouve les positions HP pour tous les 8 personnages"""
    positions = []
    marker = b'RawMP'
    pos = 0
    while True:
        pos = data.find(marker, pos)
        if pos == -1:
            break
        hp_pos = pos - 8
        if hp_pos >= 0:
            positions.append(hp_pos)
        pos += 1
    return positions[:8]

def scan_all_items(data):
    """Scan tous les items dans l'inventaire"""
    items = []
    pos = 0
    
    while True:
        # Cherche "None" suivi de "ItemId" dans les 30 octets suivants
        none_pos = data.find(b'None\x00', pos)
        if none_pos == -1:
            break
        
        # Cherche "ItemId" dans les 30 octets suivants
        search_end = min(none_pos + 30, len(data))
        itemid_marker = b'ItemId\x00'
        itemid_pos = data.find(itemid_marker, none_pos, search_end)
        
        if itemid_pos != -1:
            # Quantité est 8 bytes avant "None"
            qty_pos = none_pos - 8
            if qty_pos >= 0:
                quantity = struct.unpack('<I', data[qty_pos:qty_pos+4])[0]
                
                # ItemId est 49 bytes après la quantité
                itemid_value_pos = qty_pos + 49
                if itemid_value_pos + 4 <= len(data):
                    itemid = struct.unpack('<I', data[itemid_value_pos:itemid_value_pos+4])[0]
                    
                    if quantity > 0 and itemid > 0:
                        items.append({
                            'qty_pos': qty_pos,
                            'itemid': itemid,
                            'quantity': quantity
                        })
        
        pos = none_pos + 1
    
    return items

# Charge les saves
save6_new = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("ANALYSE DE LA NOUVELLE SaveData6")
print("="*80)
print(f"Taille SaveData6: {len(save6_new)} bytes")
print(f"Taille SaveData9: {len(save9)} bytes")
print(f"Même taille: {'✅' if len(save6_new) == len(save9) else '❌'}")

# Analyse Throné
hp_positions_6 = find_character_hp_positions(save6_new)
hp_positions_9 = find_character_hp_positions(save9)

print(f"\n{'='*80}")
print("PERSONNAGE: THRONÉ (personnage #5)")
print(f"{'='*80}")

throne_idx = 4  # Index 4 = 5ème personnage
hp6 = hp_positions_6[throne_idx]
hp9 = hp_positions_9[throne_idx]

print(f"Position HP Save6: 0x{hp6:08X}")
print(f"Position HP Save9: 0x{hp9:08X}")

# Lit HP/SP/Level
hp_val_6 = struct.unpack('<I', save6_new[hp6:hp6+4])[0]
hp_val_9 = struct.unpack('<I', save9[hp9:hp9+4])[0]

sp_val_6 = struct.unpack('<I', save6_new[hp6+39:hp6+43])[0]
sp_val_9 = struct.unpack('<I', save9[hp9+39:hp9+43])[0]

level_6 = struct.unpack('<I', save6_new[hp6-76:hp6-72])[0]
level_9 = struct.unpack('<I', save9[hp9-76:hp9-72])[0]

print(f"\nHP actuel: {hp_val_6} → {hp_val_9}")
print(f"SP actuel: {sp_val_6} → {sp_val_9}")
print(f"Level: {level_6} → {level_9}")

# Scan inventaire
print(f"\n{'='*80}")
print("INVENTAIRE: NOURISHING NUTS (ItemId 2045)")
print(f"{'='*80}")

items6 = scan_all_items(save6_new)
items9 = scan_all_items(save9)

# Trouve Nourishing Nuts
nuts_6 = [item for item in items6 if item['itemid'] == 2045]
nuts_9 = [item for item in items9 if item['itemid'] == 2045]

if nuts_6:
    n6 = nuts_6[0]
    print(f"SaveData6: {n6['quantity']} Nourishing Nuts @ 0x{n6['qty_pos']:08X}")
else:
    print("SaveData6: ❌ Pas de Nourishing Nuts trouvés!")

if nuts_9:
    n9 = nuts_9[0]
    print(f"SaveData9: {n9['quantity']} Nourishing Nuts @ 0x{n9['qty_pos']:08X}")
else:
    print("SaveData9: ❌ Pas de Nourishing Nuts trouvés!")

if nuts_6 and nuts_9:
    diff = n9['quantity'] - n6['quantity']
    print(f"\nDifférence inventaire: {diff:+d} nuts")

# Cherche des différences significatives
print(f"\n{'='*80}")
print("RECHERCHE DE DIFFÉRENCES GLOBALES")
print(f"{'='*80}")

differences = []
for pos in range(0, min(len(save6_new), len(save9)) - 4, 4):
    try:
        val6 = struct.unpack('<I', save6_new[pos:pos+4])[0]
        val9 = struct.unpack('<I', save9[pos:pos+4])[0]
        
        if val6 != val9 and 0 < val6 < 500 and 0 < val9 < 500:
            diff = val9 - val6
            if abs(diff) >= 10:  # Différences significatives
                differences.append((pos, val6, val9, diff))
    except:
        pass

print(f"Trouvé {len(differences)} différence(s) de valeurs entières significatives (≥10)")
print("\nTop 10 différences:")
for pos, v6, v9, d in sorted(differences, key=lambda x: abs(x[3]), reverse=True)[:10]:
    print(f"  0x{pos:08X}: {v6} → {v9} (diff: {d:+d})")
