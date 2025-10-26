#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche globale de toutes les différences entre SaveData6 et SaveData9
pour trouver le flag qui contrôle l'accessibilité de l'item 2045
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

print("="*80)
print("RECHERCHE EXHAUSTIVE DE TOUTES LES DIFFÉRENCES")
print("="*80)
print(f"SaveData6: {len(save6)} bytes")
print(f"SaveData9: {len(save9)} bytes")
print("="*80)

# Même taille, on peut comparer byte par byte
if len(save6) != len(save9):
    print("⚠️  Tailles différentes, comparaison impossible!")
    exit(1)

print("\nRecherche de toutes les différences byte par byte...")

differences = []
for pos in range(len(save6)):
    if save6[pos] != save9[pos]:
        differences.append(pos)

print(f"✅ Trouvé {len(differences)} byte(s) différent(s) ({len(differences)*100/len(save6):.4f}%)")

# Groupe les différences consécutives
groups = []
if differences:
    current_group = [differences[0]]
    
    for i in range(1, len(differences)):
        if differences[i] == differences[i-1] + 1:
            current_group.append(differences[i])
        else:
            groups.append(current_group)
            current_group = [differences[i]]
    
    groups.append(current_group)

print(f"\nGroupé en {len(groups)} zone(s) de différences:")
print("\n" + "="*80)

for idx, group in enumerate(groups):
    start = group[0]
    end = group[-1]
    size = len(group)
    
    print(f"\nZONE {idx+1}: 0x{start:08X} - 0x{end:08X} ({size} bytes)")
    
    # Contexte textuel avant la zone
    ctx_start = max(0, start - 50)
    ctx_before = save9[ctx_start:start]
    strings_before = []
    current = b''
    for byte in ctx_before:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings_before.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    if strings_before:
        print(f"  Contexte avant: {', '.join(strings_before[-3:])}")
    
    # Affiche les bytes différents
    if size <= 16:
        print(f"  SaveData6: {' '.join(f'{save6[p]:02X}' for p in group)}")
        print(f"  SaveData9: {' '.join(f'{save9[p]:02X}' for p in group)}")
        
        # Essaye d'interpréter
        if size == 4:
            val6 = struct.unpack('<I', save6[start:start+4])[0]
            val9 = struct.unpack('<I', save9[start:start+4])[0]
            print(f"  Valeur int32: {val6} → {val9} (diff: {val9-val6:+d})")
        
        # Essaye string
        bytes6 = bytes([save6[p] for p in group])
        bytes9 = bytes([save9[p] for p in group])
        try:
            if all(32 <= b <= 126 for b in bytes6) and all(32 <= b <= 126 for b in bytes9):
                print(f"  String: '{bytes6.decode('ascii')}' → '{bytes9.decode('ascii')}'")
        except:
            pass
    else:
        # Trop grand, affiche juste les premiers et derniers
        print(f"  Premiers bytes:")
        print(f"    SaveData6: {' '.join(f'{save6[p]:02X}' for p in group[:8])}...")
        print(f"    SaveData9: {' '.join(f'{save9[p]:02X}' for p in group[:8])}...")
    
    # Contexte textuel après la zone
    ctx_end = min(len(save9), end + 50)
    ctx_after = save9[end+1:ctx_end]
    strings_after = []
    current = b''
    for byte in ctx_after:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings_after.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    if strings_after:
        print(f"  Contexte après: {', '.join(strings_after[:3])}")

print("\n" + "="*80)
print("RÉSUMÉ")
print("="*80)
print(f"Total: {len(groups)} zone(s) différente(s)")
print("\nL'une de ces zones contient probablement le flag qui contrôle")
print("si l'item 2045 (Nourishing Nut) est accessible ou non.")
