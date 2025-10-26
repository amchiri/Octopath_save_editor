#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def get_context(data, pos, size=100):
    start = max(0, pos-size)
    end = min(len(data), pos+size)
    return data[start:end]

def analyze_candidate(data6, data9, pos6, pos9, name=""):
    print(f"\n{'='*80}")
    print(f"ANALYSE: {name}")
    print(f"{'='*80}")
    
    # Valeur
    val6 = struct.unpack('<I', data6[pos6:pos6+4])[0]
    val9 = struct.unpack('<I', data9[pos9:pos9+4])[0]
    print(f"Valeur Save6 @ 0x{pos6:08X}: {val6}")
    print(f"Valeur Save9 @ 0x{pos9:08X}: {val9}")
    print(f"Différence: {val9 - val6}")
    
    # Contexte étendu
    ctx = get_context(data9, pos9, 200)
    print(f"\nContexte étendu (200 bytes autour de la position):")
    
    # Cherche des noms de propriété
    strings = []
    current = b''
    for byte in ctx:
        if 32 <= byte <= 126:  # ASCII imprimable
            current += bytes([byte])
        else:
            if len(current) > 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    if strings:
        print("Strings trouvées dans le contexte:")
        for s in strings:
            print(f"  - {s}")
    
    # Affiche hex dump
    print(f"\nHex dump autour de 0x{pos9:08X}:")
    start = max(0, pos9-50)
    for i in range(start, min(len(data9), pos9+50), 16):
        hex_data = ' '.join(f'{b:02X}' for b in data9[i:i+16])
        ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data9[i:i+16])
        marker = ' <--' if i <= pos9 < i+16 else ''
        print(f"  0x{i:08X}: {hex_data:<48} {ascii_data}{marker}")

# Charge les saves
save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

# Top candidats à analyser en détail
candidates = [
    # Les 3 premiers qui ont l'air les plus intéressants
    (0x00000908, 0x00000980, "Candidate #1: diff +48, très tôt dans le fichier"),
    (0x00001204, 0x00001208, "Candidate #2: diff +62, début du fichier"),
    (0x0039F32C, 0x0039F378, "Candidate #3: diff +54, près de MainStoryData"),
    
    # Ceux avec des patterns "AbilityList" - pourraient être liés aux stats/bonus
    (0x00054F94, 0x00054F44, "Candidate #4: AbilityList pattern"),
    
    # Ceux avec "SaveEquipmentDataID" - équipements pourraient affecter stats
    (0x0008932C, 0x000893D8, "Candidate #5: SaveEquipmentDataID"),
]

for pos6, pos9, name in candidates:
    analyze_candidate(save6, save9, pos6, pos9, name)

print(f"\n{'='*80}")
print("RÉSUMÉ")
print(f"{'='*80}")
print("On cherche un compteur qui:")
print("  1. A augmenté d'environ 50-60 entre Save6 et Save9")
print("  2. Représente le nombre total de Nourishing Nuts consommés")
print("  3. N'est PAS la quantité d'inventaire (déjà trouvée)")
print("  4. Est utilisé par le jeu pour calculer le bonus HP")
