#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse des zones 53 et 54 qui ont été mises à zéro dans SaveData9
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def analyze_position(data, pos, name):
    print(f"\n{'='*80}")
    print(f"ANALYSE: {name} @ 0x{pos:08X}")
    print(f"{'='*80}")
    
    # Valeur
    val = struct.unpack('<I', data[pos:pos+4])[0]
    val_short = struct.unpack('<H', data[pos:pos+2])[0]
    
    print(f"Valeur 2 bytes: {val_short} (0x{val_short:04X})")
    print(f"Valeur 4 bytes: {val} (0x{val:08X})")
    
    # Contexte étendu (200 bytes autour)
    ctx_start = max(0, pos - 200)
    ctx_end = min(len(data), pos + 200)
    ctx = data[ctx_start:ctx_end]
    
    # Extrait strings
    strings = []
    current = b''
    for byte in ctx:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    print(f"\nStrings dans le contexte (200 bytes):")
    for s in strings:
        print(f"  - {s}")
    
    # Hex dump détaillé
    print(f"\nHex dump:")
    for i in range(pos-50, pos+50, 16):
        if 0 <= i < len(data):
            hex_data = ' '.join(f'{b:02X}' for b in data[i:i+16])
            ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
            marker = ' <--' if i <= pos < i+16 else ''
            print(f"  0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("ZONES SUSPECTES: Valeurs mises à zéro dans SaveData9")
print("="*80)

# Zone 53
pos53 = 0x0008FD1E
val6_53 = struct.unpack('<H', save6[pos53:pos53+2])[0]
val9_53 = struct.unpack('<H', save9[pos53:pos53+2])[0]
print(f"\nZONE 53 @ 0x{pos53:08X}:")
print(f"  SaveData6: {val6_53} (0x{val6_53:04X})")
print(f"  SaveData9: {val9_53} (0x{val9_53:04X})")
print(f"  Changement: {val6_53} → {val9_53}")

# Zone 54
pos54 = 0x000933D4
val6_54 = struct.unpack('<H', save6[pos54:pos54+2])[0]
val9_54 = struct.unpack('<H', save9[pos54:pos54+2])[0]
print(f"\nZONE 54 @ 0x{pos54:08X}:")
print(f"  SaveData6: {val6_54} (0x{val6_54:04X})")
print(f"  SaveData9: {val9_54} (0x{val9_54:04X})")
print(f"  Changement: {val6_54} → {val9_54}")

print("\n" + "="*80)
print("ANALYSE DÉTAILLÉE SaveData6")
print("="*80)
analyze_position(save6, pos53, "Zone 53 (SaveData6)")
analyze_position(save6, pos54, "Zone 54 (SaveData6)")

print("\n" + "="*80)
print("ANALYSE DÉTAILLÉE SaveData9")
print("="*80)
analyze_position(save9, pos53, "Zone 53 (SaveData9)")
analyze_position(save9, pos54, "Zone 54 (SaveData9)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("Ces deux zones ont été mises à zéro dans SaveData9.")
print("Cela pourrait être lié à:")
print("  - Un reset de compteur/timer")
print("  - Un flag de déblocage")
print("  - Une valeur d'état qui a été réinitialisée")
