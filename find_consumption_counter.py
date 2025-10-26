"""
Recherche d'un compteur de CONSOMMATION
Si SaveData6 a moins de nuts consommés et SaveData9 en a plus consommés,
cherchons un compteur qui AUGMENTE entre les deux
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
print("RECHERCHE D'UN COMPTEUR DE CONSOMMATION")
print("="*80)

# Trouver les positions HP de Throne dans chaque save
def find_throne_hp_pos(data):
    rawmp_pos = []
    search_pos = 0
    while True:
        pos = data.find(b'RawMP\x00', search_pos)
        if pos == -1:
            break
        rawmp_pos.append(pos)
        search_pos = pos + 1
    if len(rawmp_pos) >= 7:
        return rawmp_pos[6] - 8
    return None

throne_hp_save6 = find_throne_hp_pos(data_save6)
throne_hp_save9 = find_throne_hp_pos(data_save9)

print(f"\nPosition HP Throne SaveData6: 0x{throne_hp_save6:08X}")
print(f"Position HP Throne SaveData9: 0x{throne_hp_save9:08X}")

# Comparer la zone autour du HP de Throne
print("\n" + "="*80)
print("COMPARAISON ZONE HP-1000 à HP+1000 DE THRONE")
print("="*80)
print("\nCherche des valeurs qui ont AUGMENTÉ significativement:")
print(f"{'Offset':<10} {'Pos6':<12} {'Pos9':<12} {'Val6':<10} {'Val9':<10} {'DIFF':<10}")
print("-"*80)

found_counters = []

for offset in range(-1000, 1001, 4):
    pos6 = throne_hp_save6 + offset
    pos9 = throne_hp_save9 + offset
    
    # Vérifier que les positions sont valides dans les deux fichiers
    if 0 <= pos6 < len(data_save6) - 4 and 0 <= pos9 < len(data_save9) - 4:
        val6 = read_int32(data_save6, pos6)
        val9 = read_int32(data_save9, pos9)
        
        if val6 is not None and val9 is not None:
            diff = val9 - val6
            
            # Chercher augmentations entre 30 et 80 (environ 50-60 nuts)
            if 30 <= diff <= 80:
                found_counters.append((offset, pos6, pos9, val6, val9, diff))
                print(f"HP{offset:+4d}    0x{pos6:08X}  0x{pos9:08X}  {val6:<10} {val9:<10} +{diff:<9}")
                
                # Contexte
                ctx = data_save9[max(0, pos9-30):pos9+30]
                ctx_str = ''.join(chr(b) if 32<=b<127 else '.' for b in ctx)
                if any(word in ctx_str for word in ['HP', 'Item', 'Count', 'Character', 'Bonus']):
                    print(f"         Context: {ctx_str}")

if found_counters:
    print(f"\n✅ Trouvé {len(found_counters)} compteur(s) potentiel(s) !")
else:
    print("\n❌ Aucun compteur trouvé dans cette zone")

# Chercher aussi PARTOUT dans le fichier
print("\n" + "="*80)
print("RECHERCHE GLOBALE: AUGMENTATIONS DE 30-80 PARTOUT")
print("="*80)

global_counters = []

# Stratégie: chercher des patterns répétés
# Les offsets entre Save6 et Save9 peuvent être différents à cause de la taille
# Donc on cherche des VALEURS dans SaveData9 qui sont ~50 plus grandes que dans SaveData6

print("\nCherche des valeurs entre 40-70 dans SaveData9...")

values_in_save9 = []
for i in range(0, len(data_save9) - 4, 4):
    val9 = read_int32(data_save9, i)
    if val9 and 40 <= val9 <= 70:
        values_in_save9.append((i, val9))

print(f"Trouvé {len(values_in_save9)} valeurs entre 40-70 dans SaveData9")

# Pour chaque valeur, chercher si SaveData6 a une valeur ~50 moins dans une zone proche
print("\nVérifie si ces valeurs ont augmenté de ~50...")

for pos9, val9 in values_in_save9[:100]:  # Limite à 100
    # Chercher dans SaveData6 dans une zone ±200 bytes
    for search_offset in range(-200, 201, 4):
        pos6 = pos9 + search_offset
        if 0 <= pos6 < len(data_save6) - 4:
            val6 = read_int32(data_save6, pos6)
            if val6 and val6 > 0:
                diff = val9 - val6
                if 40 <= diff <= 65:  # Augmentation de ~50
                    print(f"\n🎯 TROUVÉ!")
                    print(f"  Save6 @ 0x{pos6:08X}: {val6}")
                    print(f"  Save9 @ 0x{pos9:08X}: {val9}")
                    print(f"  Diff: +{diff}")
                    
                    # Contexte
                    ctx = data_save9[max(0, pos9-40):pos9+40]
                    ctx_str = ''.join(chr(b) if 32<=b<127 else '.' for b in ctx)
                    print(f"  Context: {ctx_str}")
                    
                    global_counters.append((pos6, pos9, val6, val9, diff))
                    break  # Trouvé, passer au suivant

if global_counters:
    print(f"\n✅ Trouvé {len(global_counters)} compteur(s) global(aux) potentiel(s)!")
else:
    print("\n❌ Aucun compteur global trouvé")

print("\n" + "="*80)
