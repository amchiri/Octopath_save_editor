#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Affiche le hex dump des AcquisitionFlag de Throné pour comprendre la structure
"""

import struct
from pathlib import Path

save_data = open('SaveData/SaveData9.sav', 'rb').read()

# Zone Throné (HP=600)
THRONE_HP = 0x00091B8A
search_start = THRONE_HP - 5000
search_end = THRONE_HP

print("="*80)
print("HEX DUMP DES AcquisitionFlag DE THRONÉ")
print("="*80)

# Trouve le premier AcquisitionFlag
first_flag = save_data.find(b'AcquisitionFlag', search_start, search_end)

if first_flag != -1:
    print(f"\nPremier AcquisitionFlag @ 0x{first_flag:08X}")
    print("\nHex dump (±128 bytes):")
    
    dump_start = max(0, first_flag - 128)
    dump_end = min(len(save_data), first_flag + 256)
    
    for addr in range(dump_start, dump_end, 16):
        hex_bytes = save_data[addr:addr+16]
        hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
        
        marker = ""
        if addr <= first_flag < addr + 16:
            marker = " <- AcquisitionFlag"
        
        print(f"0x{addr:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Cherche le pattern entre AcquisitionFlag
    print("\n" + "="*80)
    print("DISTANCE ENTRE LES FLAGS:")
    print("="*80)
    
    flags = []
    pos = search_start
    while pos < search_end:
        pos = save_data.find(b'AcquisitionFlag', pos, search_end)
        if pos == -1:
            break
        flags.append(pos)
        pos += 1
    
    print(f"\nTrouvé {len(flags)} flags")
    if len(flags) >= 2:
        for i in range(min(5, len(flags) - 1)):
            distance = flags[i+1] - flags[i]
            print(f"  Flag {i+1} → Flag {i+2}: {distance} bytes")
        
        # Affiche quelques flags avec leur contexte
        print("\n" + "="*80)
        print("DÉTAIL DES 3 PREMIERS FLAGS:")
        print("="*80)
        
        for i, flag_pos in enumerate(flags[:3], 1):
            print(f"\nFlag #{i} @ 0x{flag_pos:08X}:")
            
            # Affiche 64 bytes autour
            start = flag_pos
            end = min(len(save_data), flag_pos + 64)
            
            for addr in range(start, end, 16):
                hex_bytes = save_data[addr:addr+16]
                hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
                print(f"  0x{addr:08X}: {hex_str:<48} {ascii_str}")

else:
    print("❌ Aucun AcquisitionFlag trouvé!")
