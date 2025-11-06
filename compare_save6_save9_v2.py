"""
Comparaison SaveData6 vs SaveData9 (tailles différentes)
Focus sur les valeurs clés: HP de Throne, quantité de Nourishing Nut
"""

import struct

def read_int32(data, pos):
    if pos < 0 or pos + 4 > len(data):
        return None
    return struct.unpack('<i', data[pos:pos+4])[0]

# Charger les deux sauvegardes
data_save6 = open('C:/Users/polom/OneDrive/Bureau/Octopath_save/SaveData/SaveData8.sav', 'rb').read()
data_save9 = open('C:/Users/polom/OneDrive/Bureau/Octopath_save/SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("COMPARAISON: SaveData6 vs SaveData9")
print("="*80)

print(f"\nSaveData8: {len(data_save6):,} bytes")
print(f"SaveData9: {len(data_save9):,} bytes")
print(f"Différence: {len(data_save9) - len(data_save6):,} bytes")

# 1. Trouver le HP de Throne dans chaque save
print("\n" + "="*80)
print("🔍 POSITION HP DE THRONE")
print("="*80)

for i in 