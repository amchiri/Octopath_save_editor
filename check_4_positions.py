#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def get_context_with_itemid(data, pos):
    """Regarde si c'est une quantité d'item et trouve l'ItemId"""
    # Si c'est une quantité d'item, l'ItemId est à +49 bytes
    itemid_pos = pos + 49
    if itemid_pos + 4 <= len(data):
        itemid = struct.unpack('<I', data[itemid_pos:itemid_pos+4])[0]
        
        # Cherche "None" après la position
        none_pos = data.find(b'None\x00', pos, pos + 20)
        if none_pos != -1:
            return f"Item quantity, ItemId={itemid}"
    
    # Contexte texte
    ctx = data[max(0, pos-40):min(len(data), pos+60)]
    strings = []
    current = b''
    for byte in ctx:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    return ', '.join(strings[:5]) if strings else '(binary)'

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

positions = [0x00017D54, 0x00017E00, 0x00019E40, 0x00019EEC]

print("="*80)
print("ANALYSE DES 4 POSITIONS QUI ONT CHANGÉ DE 1 → 99")
print("="*80)

for pos in positions:
    val6 = struct.unpack('<I', save6[pos:pos+4])[0]
    val9 = struct.unpack('<I', save9[pos:pos+4])[0]
    
    context = get_context_with_itemid(save9, pos)
    
    print(f"\n0x{pos:08X}: {val6} → {val9}")
    print(f"  Context: {context}")
    
    # Hex dump
    print(f"  Hex dump:")
    for i in range(pos-16, pos+32, 16):
        if 0 <= i < len(save9):
            hex_data = ' '.join(f'{b:02X}' for b in save9[i:i+16])
            ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in save9[i:i+16])
            marker = ' <--' if i <= pos < i+16 else ''
            print(f"    0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("Ces 4 positions ont toutes été modifiées de 1 → 99")
print("Ce sont probablement des quantités d'items dans l'inventaire")
print("Vérifions si ce sont des Nourishing Nuts ou d'autres items")
