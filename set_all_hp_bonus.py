#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Met 9075 HP bonus pour TOUS les personnages dans SaveData6
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = filepath + '.backup_final'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

def find_all_doping_positions(data):
    """Trouve toutes les positions DopingParam HP pour les 8 personnages"""
    positions = []
    pattern_doping = b'DopingParam'
    
    pos = 0
    while True:
        pos = data.find(pattern_doping, pos)
        if pos == -1:
            break
        
        # Cherche "HP" dans les 200 bytes suivants
        hp_marker = data.find(b'\x03\x00\x00\x00HP\x00', pos, pos + 200)
        if hp_marker != -1:
            # Cherche "MP" dans les 50 bytes après "HP"
            mp_marker = data.find(b'\x03\x00\x00\x00MP\x00', hp_marker, hp_marker + 50)
            if mp_marker != -1:
                # La valeur HP bonus est 8 bytes avant "MP"
                hp_bonus_pos = mp_marker - 8
                
                if hp_bonus_pos >= 0:
                    hp_bonus = struct.unpack('<H', data[hp_bonus_pos:hp_bonus_pos+2])[0]
                    positions.append({
                        'pos': hp_bonus_pos,
                        'bonus': hp_bonus
                    })
        
        pos += 1
    
    return positions[:8]  # Seulement les 8 premiers

save6 = read_save('SaveData/SaveData6.sav')

print("="*80)
print("ÉDITEUR HP BONUS - TOUS LES PERSONNAGES")
print("="*80)

# Trouve toutes les positions
positions = find_all_doping_positions(save6)

if len(positions) < 8:
    print(f"❌ Erreur: Seulement {len(positions)} positions trouvées (attendu 8)")
    exit(1)

characters = ['Hikari', 'Agnea', 'Partitio', 'Osvald', 'Throné', 'Temenos', 'Ochette', 'Castti']

print(f"\nTrouvé {len(positions)} personnages\n")

# Affiche les valeurs actuelles
print("VALEURS ACTUELLES:")
for idx, (char, pos_info) in enumerate(zip(characters, positions)):
    nuts = pos_info['bonus'] // 75
    print(f"  {idx+1}. {char:10} @ 0x{pos_info['pos']:08X}: {pos_info['bonus']:5} HP bonus ({nuts} nuts)")

# Demande confirmation
print("\n" + "="*80)
nuts_count = input("Combien de Nourishing Nuts pour tous? (par défaut 121 = 9075 HP): ").strip()

if not nuts_count:
    nuts_count = 121
else:
    try:
        nuts_count = int(nuts_count)
    except:
        print("❌ Valeur invalide, utilisation de 121")
        nuts_count = 121

hp_bonus = nuts_count * 75

print(f"\n✅ Application de {nuts_count} nuts ({hp_bonus} HP bonus) à tous les personnages...")

# Modifie
data6 = bytearray(save6)

for pos_info in positions:
    struct.pack_into('<H', data6, pos_info['pos'], hp_bonus)

# Vérifie
print("\nVALEURS APRÈS MODIFICATION:")
for idx, (char, pos_info) in enumerate(zip(characters, positions)):
    new_val = struct.unpack('<H', data6[pos_info['pos']:pos_info['pos']+2])[0]
    nuts = new_val // 75
    print(f"  {idx+1}. {char:10} @ 0x{pos_info['pos']:08X}: {new_val:5} HP bonus ({nuts} nuts)")

# Sauvegarde
print("\n" + "="*80)
save6_path = Path('SaveData/SaveData6.sav')
write_save(str(save6_path), bytes(data6))

print("\n✅ SaveData6 modifié!")
print("   Tous les personnages ont maintenant le même bonus HP!")
