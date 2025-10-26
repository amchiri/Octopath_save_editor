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
data_save6 = open('SaveData/SaveData6.sav', 'rb').read()
data_save9 = open('SaveData/SaveData9.sav', 'rb').read()

print("="*80)
print("COMPARAISON: SaveData6 vs SaveData9")
print("="*80)

print(f"\nSaveData6: {len(data_save6):,} bytes")
print(f"SaveData9: {len(data_save9):,} bytes")
print(f"Différence: {len(data_save9) - len(data_save6):,} bytes")

# 1. Trouver le HP de Throne dans chaque save
print("\n" + "="*80)
print("🔍 POSITION HP DE THRONE")
print("="*80)

def find_throne_hp(data, save_name):
    rawmp_positions = []
    search_pos = 0
    while True:
        pos = data.find(b'RawMP\x00', search_pos)
        if pos == -1:
            break
        rawmp_positions.append(pos)
        search_pos = pos + 1
    
    if len(rawmp_positions) >= 7:
        throne_hp_pos = rawmp_positions[6] - 8  # 7ème perso (index 6)
        throne_hp = read_int32(data, throne_hp_pos)
        throne_sp = read_int32(data, throne_hp_pos + 39)
        throne_level = read_int32(data, throne_hp_pos - 76)
        
        print(f"\n{save_name}:")
        print(f"  Position HP: 0x{throne_hp_pos:08X}")
        print(f"  HP:    {throne_hp}")
        print(f"  SP:    {throne_sp}")
        print(f"  Level: {throne_level}")
        
        return throne_hp_pos, throne_hp, throne_sp, throne_level
    return None, None, None, None

pos6, hp6, sp6, lvl6 = find_throne_hp(data_save6, "SaveData6")
pos9, hp9, sp9, lvl9 = find_throne_hp(data_save9, "SaveData9")

if hp6 and hp9:
    print(f"\n🔥 DIFFÉRENCES:")
    print(f"  HP:    {hp9 - hp6:+d}")
    print(f"  SP:    {sp9 - sp6:+d}")
    print(f"  Level: {lvl9 - lvl6:+d}")

# 2. Quantité de Nourishing Nut (ItemId 2045)
print("\n" + "="*80)
print("🔍 NOURISHING NUT (ItemId 2045)")
print("="*80)

itemid_2045 = struct.pack('<i', 2045)

pos_save6 = data_save6.find(itemid_2045)
if pos_save6 != -1:
    qty_pos6 = pos_save6 - 49
    qty6 = read_int32(data_save6, qty_pos6)
    print(f"\nSaveData6:")
    print(f"  ItemId @ 0x{pos_save6:08X}")
    print(f"  Qty @ 0x{qty_pos6:08X}: {qty6}")
else:
    print(f"\nSaveData6: ItemId 2045 NON TROUVÉ")
    qty6 = 0

pos_save9 = data_save9.find(itemid_2045)
if pos_save9 != -1:
    qty_pos9 = pos_save9 - 49
    qty9 = read_int32(data_save9, qty_pos9)
    print(f"\nSaveData9:")
    print(f"  ItemId @ 0x{pos_save9:08X}")
    print(f"  Qty @ 0x{qty_pos9:08X}: {qty9}")
else:
    print(f"\nSaveData9: ItemId 2045 NON TROUVÉ")
    qty9 = 0

if qty6 and qty9:
    diff = qty6 - qty9
    print(f"\n🎯 CONSOMMÉS: {diff} Nourishing Nuts")
    print(f"   HP Bonus théorique: +{diff * 80} HP")

# 3. Chercher des valeurs qui pourraient être un compteur (valeurs ~50)
print("\n" + "="*80)
print("🔍 RECHERCHE DE VALEURS ~50 DANS CHAQUE FICHIER")
print("="*80)

# Dans SaveData6
print("\nSaveData6 - Valeurs entre 45-55 près de Throne:")
if pos6:
    for offset in range(-1000, 1001, 4):
        p = pos6 + offset
        if 0 <= p < len(data_save6) - 4:
            val = read_int32(data_save6, p)
            if val and 45 <= val <= 55:
                print(f"  HP{offset:+5d} @ 0x{p:08X}: {val}")

# Dans SaveData9  
print("\nSaveData9 - Valeurs entre 0-10 près de Throne:")
if pos9:
    for offset in range(-1000, 1001, 4):
        p = pos9 + offset
        if 0 <= p < len(data_save9) - 4:
            val = read_int32(data_save9, p)
            if val and 0 <= val <= 10:
                print(f"  HP{offset:+5d} @ 0x{p:08X}: {val}")

print("\n" + "="*80)
print("💡 ANALYSE")
print("="*80)
print("\nSi Throne a vraiment 7k HP dans SaveData9 vs beaucoup moins dans SaveData6,")
print("et qu'on ne trouve PAS de compteur, alors:")
print("  → Le HP est recalculé dynamiquement à partir de l'inventaire")
print("  → Aucun compteur n'est stocké dans la save")
print("  → Pour tricher: il suffit de vider l'inventaire de Nourishing Nuts!")
print("="*80)
