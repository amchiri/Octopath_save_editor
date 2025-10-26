#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def find_character_hp_positions(data):
    """Trouve les positions HP pour tous les 8 personnages"""
    positions = []
    # Cherche "RawMP" 
    marker = b'RawMP'
    pos = 0
    while True:
        pos = data.find(marker, pos)
        if pos == -1:
            break
        # La valeur HP est 8 octets AVANT "RawMP"
        hp_pos = pos - 8
        if hp_pos >= 0:
            positions.append(hp_pos)
        pos += 1
    
    return positions[:8]  # Seulement les 8 premiers (les persos)

# Charge les saves
save6 = read_save('SaveData/SaveData6.sav')
save9 = read_save('SaveData/SaveData9.sav')

# Trouve les positions HP dans les deux saves
hp_positions_6 = find_character_hp_positions(save6)
hp_positions_9 = find_character_hp_positions(save9)

print("="*80)
print("RECHERCHE DE COMPTEURS PAR PERSONNAGE")
print("="*80)

characters = ['Hikari', 'Agnea', 'Partitio', 'Osvald', 'Throné', 'Temenos', 'Ochette', 'Castti']

for idx, (char_name, hp6, hp9) in enumerate(zip(characters, hp_positions_6, hp_positions_9)):
    print(f"\n{'='*80}")
    print(f"PERSONNAGE {idx+1}: {char_name}")
    print(f"{'='*80}")
    print(f"Position HP Save6: 0x{hp6:08X}")
    print(f"Position HP Save9: 0x{hp9:08X}")
    
    # Lit HP/SP/Level
    hp_val_6 = struct.unpack('<I', save6[hp6:hp6+4])[0]
    hp_val_9 = struct.unpack('<I', save9[hp9:hp9+4])[0]
    
    sp_val_6 = struct.unpack('<I', save6[hp6+39:hp6+43])[0]
    sp_val_9 = struct.unpack('<I', save9[hp9+39:hp9+43])[0]
    
    level_6 = struct.unpack('<I', save6[hp6-76:hp6-72])[0]
    level_9 = struct.unpack('<I', save9[hp9-76:hp9-72])[0]
    
    print(f"  HP: {hp_val_6} → {hp_val_9}")
    print(f"  SP: {sp_val_6} → {sp_val_9}")
    print(f"  Level: {level_6} → {level_9}")
    
    # Cherche dans un range de -500 à +500 autour du HP
    # pour des valeurs qui ont augmenté de 40-70
    print(f"\n  Recherche de compteur augmenté de 40-70...")
    found = []
    
    search_start = max(0, hp6 - 500)
    search_end = min(len(save6), hp6 + 500)
    
    for offset6 in range(search_start, search_end, 4):  # Par pas de 4 (entier)
        try:
            val6 = struct.unpack('<I', save6[offset6:offset6+4])[0]
            
            # Trouve position correspondante dans save9
            offset9 = offset6 + (hp9 - hp6)  # Ajuste pour le décalage
            if offset9 < 0 or offset9 + 4 > len(save9):
                continue
                
            val9 = struct.unpack('<I', save9[offset9:offset9+4])[0]
            
            # Si valeur entre 0-200 et a augmenté de 40-70
            if 0 < val6 < 200 and 0 < val9 < 200:
                diff = val9 - val6
                if 40 <= diff <= 70:
                    rel_offset = offset6 - hp6
                    found.append((offset6, offset9, val6, val9, diff, rel_offset))
        except:
            pass
    
    if found:
        print(f"  ✅ Trouvé {len(found)} candidat(s):")
        for off6, off9, v6, v9, d, rel in found:
            print(f"    @ HP{rel:+d} (0x{off6:08X} → 0x{off9:08X}): {v6} → {v9} (diff: {d})")
            
            # Affiche contexte
            ctx = save9[max(0, off9-30):min(len(save9), off9+30)]
            strings = []
            current = b''
            for byte in ctx:
                if 32 <= byte <= 126:
                    current += bytes([byte])
                else:
                    if len(current) > 3:
                        strings.append(current.decode('ascii', errors='ignore'))
                    current = b''
            if strings:
                print(f"      Context strings: {', '.join(strings[:3])}")
    else:
        print(f"  ❌ Aucun compteur trouvé")

print(f"\n{'='*80}")
print("RÉSUMÉ")
print(f"{'='*80}")
print("Si un compteur de Nourishing Nut existe, il devrait:")
print("  - Être au même offset relatif pour tous les personnages")
print("  - Avoir augmenté de ~50 pour Throné (qui a consommé)")
print("  - Être stable pour les autres personnages")
