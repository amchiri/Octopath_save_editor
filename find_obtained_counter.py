#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
THÉORIE: Le jeu stocke le NOMBRE TOTAL DE NUTS OBTENUS, pas consommés.
HP bonus = (TOTAL_OBTENUS - INVENTAIRE_ACTUEL) × 75

Si vrai, alors:
- SaveData9_9nutshell: 90 en inventaire après consommation
- SaveData9: 99 en inventaire après édition
- Le jeu pense qu'on a OBTENU 9 nuts de plus
- Donc TOTAL_OBTENUS devrait être 9 plus élevé dans SaveData9

Cherchons un compteur qui a AUGMENTÉ de 9 entre SaveData9_9nutshell et SaveData9
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def find_differences_by_value(data1, data2, target_diff, tolerance=2):
    """
    Trouve des positions où une valeur 4-bytes a changé d'environ target_diff
    """
    results = []
    
    # S'assurer que les deux fichiers ont la même taille
    if len(data1) != len(data2):
        print(f"⚠️  Tailles différentes: {len(data1)} vs {len(data2)}")
        min_len = min(len(data1), len(data2))
    else:
        min_len = len(data1)
    
    # Scan par 4 bytes
    for pos in range(0, min_len - 4, 1):
        try:
            val1 = struct.unpack('<I', data1[pos:pos+4])[0]
            val2 = struct.unpack('<I', data2[pos:pos+4])[0]
            
            # Valeurs raisonnables (0-500)
            if 0 < val1 < 500 and 0 < val2 < 500:
                diff = val2 - val1
                if target_diff - tolerance <= diff <= target_diff + tolerance:
                    results.append((pos, val1, val2, diff))
        except:
            pass
    
    return results

# Charge les saves
save9_9nut = read_save('SaveData/SaveData9_9nutshell.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("RECHERCHE: Compteur qui a AUGMENTÉ de 9")
print("SaveData9_9nutshell → SaveData9 (après édition inventaire 90→99)")
print("="*80)

# Cherche valeurs qui ont augmenté de 9 (±2)
results = find_differences_by_value(save9_9nut, save9, target_diff=9, tolerance=2)

print(f"\n✅ Trouvé {len(results)} position(s) où la valeur a augmenté de ~9:\n")

for pos, val1, val2, diff in results[:20]:  # Limite à 20 premiers
    # Contexte
    ctx = save9[max(0, pos-40):min(len(save9), pos+60)]
    strings = []
    current = b''
    for byte in ctx:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    context_str = ', '.join(strings[:5]) if strings else '(binary)'
    
    print(f"0x{pos:08X}: {val1} → {val2} (diff: +{diff})")
    print(f"  Context: {context_str}")
    print()

if len(results) > 20:
    print(f"... et {len(results) - 20} autres résultats")

print("\n" + "="*80)
print("INTERPRÉTATION")
print("="*80)
print("Si on trouve un compteur qui a augmenté de exactement 9:")
print("  → C'est probablement le compteur TOTAL_NUTS_OBTAINED")
print("  → Le jeu calcule: consommés = obtenus - inventaire")
print("  → Modifier ce compteur donnerait le bonus HP sans changer l'inventaire!")
