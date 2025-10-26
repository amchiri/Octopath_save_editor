"""
Comparaison SaveData6 vs SaveData9
Throne a consommé ~50 Nourishing Nuts de plus dans SaveData9
On cherche des grosses différences (autour de 50, 4000, etc.)
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
print("COMPARAISON: SaveData6 vs SaveData9 (~50 Nourishing Nuts de différence)")
print("="*80)

print(f"\nSaveData6: {len(data_save6)} bytes")
print(f"SaveData9: {len(data_save9)} bytes")

if len(data_save6) != len(data_save9):
    print("\n⚠️  TAILLES DIFFÉRENTES ! Impossible de comparer byte par byte")
    exit()

# 1. Chercher les GROSSES différences (autour de 50, 4000, etc.)
print("\n" + "="*80)
print("🔍 RECHERCHE DE GROSSES DIFFÉRENCES")
print("="*80)

big_diffs = []
for i in range(0, len(data_save6) - 4, 4):
    val6 = read_int32(data_save6, i)
    val9 = read_int32(data_save9, i)
    
    if val6 is not None and val9 is not None:
        diff = val9 - val6
        
        # Grosses différences intéressantes
        if abs(diff) >= 40 and abs(diff) <= 60:  # Autour de 50
            big_diffs.append((i, val6, val9, diff, 'DIFF ~50'))
        elif abs(diff) >= 3500 and abs(diff) <= 4500:  # Autour de 4000
            big_diffs.append((i, val6, val9, diff, 'DIFF ~4000'))
        elif abs(diff) >= 100 and abs(diff) <= 1000:  # Entre 100 et 1000
            big_diffs.append((i, val6, val9, diff, 'DIFF 100-1000'))

if big_diffs:
    print(f"\n✅ Trouvé {len(big_diffs)} grosse(s) différence(s):")
    
    # Grouper par type
    diff_50 = [d for d in big_diffs if 'DIFF ~50' in d[4]]
    diff_4000 = [d for d in big_diffs if 'DIFF ~4000' in d[4]]
    diff_mid = [d for d in big_diffs if 'DIFF 100-1000' in d[4]]
    
    if diff_50:
        print(f"\n🎯 DIFFÉRENCES AUTOUR DE 50 ({len(diff_50)} trouvées):")
        for pos, val6, val9, diff, note in diff_50[:20]:
            print(f"  0x{pos:08X}: {val6:8d} → {val9:8d} (diff: {diff:+d})")
            # Contexte
            ctx = data_save6[max(0,pos-30):pos+40]
            ctx_str = ''.join(chr(b) if 32<=b<127 else '.' for b in ctx)
            print(f"    {ctx_str}")
    
    if diff_4000:
        print(f"\n🔥 DIFFÉRENCES AUTOUR DE 4000 ({len(diff_4000)} trouvées):")
        for pos, val6, val9, diff, note in diff_4000[:20]:
            print(f"  0x{pos:08X}: {val6:8d} → {val9:8d} (diff: {diff:+d})")
            ctx = data_save6[max(0,pos-30):pos+40]
            ctx_str = ''.join(chr(b) if 32<=b<127 else '.' for b in ctx)
            print(f"    {ctx_str}")
    
    if diff_mid:
        print(f"\n💡 DIFFÉRENCES 100-1000 ({len(diff_mid)} trouvées):")
        for pos, val6, val9, diff, note in diff_mid[:30]:
            print(f"  0x{pos:08X}: {val6:8d} → {val9:8d} (diff: {diff:+d})")
else:
    print("\n❌ Aucune grosse différence trouvée")

# 2. Chercher spécifiquement près du HP de Throne
print("\n" + "="*80)
print("🔍 ZONE DU HP DE THRONE")
print("="*80)

# Trouver Throne dans SaveData9
rawmp_pos9 = []
search_pos = 0
while True:
    pos = data_save9.find(b'RawMP\x00', search_pos)
    if pos == -1:
        break
    rawmp_pos9.append(pos)
    search_pos = pos + 1

if len(rawmp_pos9) >= 8:
    throne_hp_pos9 = rawmp_pos9[6] - 8
    
    print(f"\nPosition HP de Throne (SaveData9): 0x{throne_hp_pos9:08X}")
    
    # Comparer la zone autour
    print(f"\nComparaison HP-500 à HP+500:")
    print(f"{'Offset':<10} {'Position':<12} {'Save6':<12} {'Save9':<12} {'DIFF':<12}")
    print("-"*80)
    
    changes_near_throne = []
    for offset in range(-500, 501, 4):
        pos = throne_hp_pos9 + offset
        if pos >= 0 and pos + 4 <= len(data_save6):
            val6 = read_int32(data_save6, pos)
            val9 = read_int32(data_save9, pos)
            
            if val6 != val9 and val6 is not None and val9 is not None:
                diff = val9 - val6
                if abs(diff) >= 40:  # Différence significative
                    changes_near_throne.append((offset, pos, val6, val9, diff))
                    print(f"HP{offset:+4d}    0x{pos:08X}  {val6:<12} {val9:<12} {diff:+12d}")
    
    if not changes_near_throne:
        print("❌ Aucune grosse différence près de Throne")

# 3. Vérifier la quantité de Nourishing Nut
print("\n" + "="*80)
print("🔍 QUANTITÉ DE NOURISHING NUT (ItemId 2045)")
print("="*80)

itemid_2045 = struct.pack('<i', 2045)
pos_2045_save6 = data_save6.find(itemid_2045)
pos_2045_save9 = data_save9.find(itemid_2045)

if pos_2045_save6 != -1 and pos_2045_save9 != -1:
    qty_pos6 = pos_2045_save6 - 49
    qty_pos9 = pos_2045_save9 - 49
    
    qty6 = read_int32(data_save6, qty_pos6)
    qty9 = read_int32(data_save9, qty_pos9)
    
    print(f"\nPosition ItemId 2045:")
    print(f"  SaveData6: 0x{pos_2045_save6:08X}, Qty @ 0x{qty_pos6:08X} = {qty6}")
    print(f"  SaveData9: 0x{pos_2045_save9:08X}, Qty @ 0x{qty_pos9:08X} = {qty9}")
    print(f"  Différence: {qty9 - qty6} (negatif = consommés)")
    print(f"  🔥 Nourishing Nuts consommés: {qty6 - qty9}")

print("\n" + "="*80)
