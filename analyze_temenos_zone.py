#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérifie si mes scripts ont accidentellement écrit 4 bytes au lieu de 2
"""

import struct
from pathlib import Path

save_path = Path('SaveData/SaveData9.sav')
save_data = open(save_path, 'rb').read()

TEMENOS_COUNTER_POS = 0x0008FD18  # 6 bytes avant
TEMENOS_BONUS_POS = 0x0008FD1E    # Position qu'on modifiait

print("="*80)
print("ANALYSE DÉTAILLÉE DE LA ZONE TEMENOS")
print("="*80)

# Hex dump de toute la zone
print("\nHEX DUMP (0x0008FD10 à 0x0008FD30):")
start = 0x0008FD10
end = 0x0008FD30

for i in range(start, end, 16):
    hex_bytes = save_data[i:i+16]
    hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
    print(f"0x{i:08X}: {hex_str:<48} {ascii_str}")

# Marque les positions importantes
print("\n" + "="*80)
print("POSITIONS IMPORTANTES:")
print(f"  0x{TEMENOS_COUNTER_POS:08X}: Position -6 bytes (compteur nuts?)")
print(f"  0x{TEMENOS_BONUS_POS:08X}: Position +0 bytes (bonus HP)")
print("="*80)

# Lit les valeurs avec différentes tailles
print("\nLECTURES À 0x0008FD18 (compteur nuts?):")
val_2bytes = struct.unpack('<H', save_data[TEMENOS_COUNTER_POS:TEMENOS_COUNTER_POS+2])[0]
val_4bytes = struct.unpack('<I', save_data[TEMENOS_COUNTER_POS:TEMENOS_COUNTER_POS+4])[0]
print(f"  2 bytes (uint16): {val_2bytes:5} (0x{val_2bytes:04X})")
print(f"  4 bytes (uint32): {val_4bytes:10} (0x{val_4bytes:08X})")

print("\nLECTURES À 0x0008FD1E (bonus HP):")
val_2bytes = struct.unpack('<H', save_data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+2])[0]
val_4bytes = struct.unpack('<I', save_data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+4])[0]
print(f"  2 bytes (uint16): {val_2bytes:5} (0x{val_2bytes:04X})")
print(f"  4 bytes (uint32): {val_4bytes:10} (0x{val_4bytes:08X})")

print("\n" + "="*80)
print("ANALYSE:")

# Vérifie si les 6 bytes entre les deux positions sont cohérents
between = save_data[TEMENOS_COUNTER_POS+2:TEMENOS_BONUS_POS]
print(f"\nBytes ENTRE les deux positions:")
print(f"  {' '.join(f'{b:02X}' for b in between)}")

# Cherche des patterns
if save_data[TEMENOS_COUNTER_POS:TEMENOS_COUNTER_POS+2] == save_data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+2]:
    print("\n⚠️  Les deux positions ont la MÊME valeur!")
    print("     Cela suggère qu'elles sont liées ou que l'une copie l'autre.")
else:
    print("\n✅ Les deux positions ont des valeurs DIFFÉRENTES.")
    print("     Ce sont probablement deux compteurs indépendants.")
