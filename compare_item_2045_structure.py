#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DÉCOUVERTE CRITIQUE: SaveData6 a 99 nuts dans le fichier mais pas accessible dans le jeu!
Il doit y avoir un flag ou une structure qui contrôle l'accès/déverrouillage de l'item.
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def find_item_2045(data):
    """Trouve la position exacte de l'ItemId 2045 (Nourishing Nut)"""
    pos = 0
    while True:
        # Cherche "None" suivi de "ItemId"
        none_pos = data.find(b'None\x00', pos)
        if none_pos == -1:
            break
        
        # Cherche "ItemId" dans les 30 octets suivants
        search_end = min(none_pos + 30, len(data))
        itemid_pos = data.find(b'ItemId\x00', none_pos, search_end)
        
        if itemid_pos != -1:
            # Quantité est 8 bytes avant "None"
            qty_pos = none_pos - 8
            if qty_pos >= 0:
                quantity = struct.unpack('<I', data[qty_pos:qty_pos+4])[0]
                
                # ItemId est 49 bytes après la quantité
                itemid_value_pos = qty_pos + 49
                if itemid_value_pos + 4 <= len(data):
                    itemid = struct.unpack('<I', data[itemid_value_pos:itemid_value_pos+4])[0]
                    
                    if itemid == 2045:  # Nourishing Nut
                        return {
                            'qty_pos': qty_pos,
                            'qty': quantity,
                            'itemid_pos': itemid_value_pos,
                            'none_pos': none_pos,
                            'start_pos': qty_pos - 20  # Un peu avant pour contexte
                        }
        
        pos = none_pos + 1
    
    return None

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("COMPARAISON STRUCTURE ITEM 2045 (NOURISHING NUT)")
print("="*80)
print("SaveData6: 99 nuts dans fichier, MAIS pas accessible dans le jeu ❌")
print("SaveData9: 99 nuts dans fichier, ET accessible dans le jeu ✅")
print("="*80)

item6 = find_item_2045(save6)
item9 = find_item_2045(save9)

if not item6:
    print("\n❌ Item 2045 non trouvé dans SaveData6!")
    exit(1)

if not item9:
    print("\n❌ Item 2045 non trouvé dans SaveData9!")
    exit(1)

print(f"\nSaveData6 Item 2045:")
print(f"  Position quantité: 0x{item6['qty_pos']:08X}")
print(f"  Quantité: {item6['qty']}")
print(f"  Position ItemId: 0x{item6['itemid_pos']:08X}")

print(f"\nSaveData9 Item 2045:")
print(f"  Position quantité: 0x{item9['qty_pos']:08X}")
print(f"  Quantité: {item9['qty']}")
print(f"  Position ItemId: 0x{item9['itemid_pos']:08X}")

# Compare la structure complète autour de l'item (200 bytes avant et après)
print(f"\n{'='*80}")
print("COMPARAISON BYTE PAR BYTE AUTOUR DE L'ITEM")
print(f"{'='*80}")

# Zone à comparer: 200 bytes avant la quantité jusqu'à 200 après l'ItemId
start6 = max(0, item6['qty_pos'] - 200)
end6 = min(len(save6), item6['itemid_pos'] + 200)

start9 = max(0, item9['qty_pos'] - 200)
end9 = min(len(save9), item9['itemid_pos'] + 200)

# Longueur de la zone
len6 = end6 - start6
len9 = end9 - start9

print(f"\nZone SaveData6: 0x{start6:08X} à 0x{end6:08X} ({len6} bytes)")
print(f"Zone SaveData9: 0x{start9:08X} à 0x{end9:08X} ({len9} bytes)")

if len6 != len9:
    print(f"\n⚠️  Les zones ont des tailles différentes!")
    print(f"   On va comparer byte par byte en alignant sur la position de la quantité")

# Compare en alignant sur la position de quantité
offset_diff = item9['qty_pos'] - item6['qty_pos']
print(f"\nDécalage entre les deux saves: {offset_diff} bytes")

# Compare 200 bytes avant et après la quantité
differences = []
for rel_offset in range(-200, 300):
    pos6 = item6['qty_pos'] + rel_offset
    pos9 = item9['qty_pos'] + rel_offset
    
    if 0 <= pos6 < len(save6) and 0 <= pos9 < len(save9):
        if save6[pos6] != save9[pos9]:
            differences.append((rel_offset, pos6, pos9, save6[pos6], save9[pos9]))

print(f"\n✅ Trouvé {len(differences)} différence(s) de bytes")

if differences:
    print("\nDifférences (position relative à la quantité):")
    print("RelOffset  Pos6       Pos9       Byte6  Byte9  Char6 Char9")
    print("-" * 70)
    
    for rel_off, p6, p9, b6, b9 in differences[:50]:  # Max 50
        c6 = chr(b6) if 32 <= b6 <= 126 else '.'
        c9 = chr(b9) if 32 <= b9 <= 126 else '.'
        marker = " <-- QTY" if rel_off == 0 else ""
        print(f"{rel_off:+4d}       0x{p6:08X} 0x{p9:08X} 0x{b6:02X}   0x{b9:02X}   '{c6}'   '{c9}'{marker}")
    
    if len(differences) > 50:
        print(f"\n... et {len(differences) - 50} autres différences")
    
    # Cherche des patterns
    print(f"\n{'='*80}")
    print("ANALYSE DES PATTERNS")
    print(f"{'='*80}")
    
    # Groupes de différences consécutives
    groups = []
    current_group = [differences[0]]
    
    for i in range(1, len(differences)):
        if differences[i][0] == differences[i-1][0] + 1:  # Consécutif
            current_group.append(differences[i])
        else:
            if len(current_group) >= 4:  # Groupe significatif
                groups.append(current_group)
            current_group = [differences[i]]
    
    if len(current_group) >= 4:
        groups.append(current_group)
    
    if groups:
        print(f"\nTrouvé {len(groups)} groupe(s) de bytes consécutifs différents:")
        for idx, group in enumerate(groups):
            print(f"\n  Groupe {idx+1}: {len(group)} bytes consécutifs @ offset {group[0][0]:+d}")
            
            # Extrait les bytes
            bytes6 = bytes([b6 for _, _, _, b6, _ in group])
            bytes9 = bytes([b9 for _, _, _, _, b9 in group])
            
            # Essaye de décoder
            try:
                str6 = bytes6.decode('ascii', errors='ignore')
                str9 = bytes9.decode('ascii', errors='ignore')
                if str6.isprintable() and str9.isprintable():
                    print(f"    Save6: '{str6}'")
                    print(f"    Save9: '{str9}'")
            except:
                pass
            
            # Essaye d'interpréter comme entier si 4 bytes
            if len(group) == 4:
                pos6 = group[0][1]
                pos9 = group[0][2]
                val6 = struct.unpack('<I', save6[pos6:pos6+4])[0]
                val9 = struct.unpack('<I', save9[pos9:pos9+4])[0]
                print(f"    Valeur entière: {val6} → {val9}")
else:
    print("\n✅ Aucune différence! Les structures sont identiques autour de l'item!")
    print("⚠️  Le flag d'accessibilité doit être ailleurs dans le fichier...")
