#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ÉDITEUR DE BONUS HP (NOURISHING NUTS)

Modifie directement les compteurs DopingParam HP pour chaque personnage.
Chaque Nourishing Nut consommé donne +75 HP max.

Structure trouvée:
- Section "DopingParam" pour chaque personnage
- Valeur 2 bytes juste avant la string "MP"
- Représente le bonus HP total accumulé
"""

import struct
from pathlib import Path
import shutil

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    # Backup
    backup_path = filepath + '.backup'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Sauvegarde modifiée: {filepath}")

def find_doping_hp_positions(data):
    """
    Trouve toutes les positions des compteurs DopingParam HP
    
    Pattern trouvé:
    - Section "DopingParam" contient "HP", "MP", "BP"  
    - La valeur bonus HP est juste avant "MP"
    - Structure: [HP bonus 2 bytes][00 00 03 00 00 00]"MP"
    """
    positions = []
    
    # Cherche "DopingParam" puis "HP" puis trouve la valeur avant "MP"
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
                # Structure: [val 2 bytes][00 00][03 00 00 00]"MP"
                hp_bonus_pos = mp_marker - 8
                
                if hp_bonus_pos >= 0:
                    hp_bonus = struct.unpack('<H', data[hp_bonus_pos:hp_bonus_pos+2])[0]
                    positions.append({
                        'pos': hp_bonus_pos,
                        'bonus': hp_bonus,
                        'nuts_consumed': hp_bonus // 75 if hp_bonus > 0 else 0
                    })
        
        pos += 1
    
    return positions

def display_hp_bonuses(positions):
    """Affiche les bonus HP de tous les personnages"""
    characters = ['Hikari', 'Agnea', 'Partitio', 'Osvald', 'Throné', 'Temenos', 'Ochette', 'Castti']
    
    print("\n" + "="*80)
    print("BONUS HP ACTUELS (NOURISHING NUTS)")
    print("="*80)
    
    for idx, (char, pos_info) in enumerate(zip(characters, positions)):
        nuts = pos_info['nuts_consumed']
        bonus = pos_info['bonus']
        print(f"{idx+1}. {char:10} @ 0x{pos_info['pos']:08X}: "
              f"{bonus:5} HP bonus ({nuts} Nourishing Nuts)")
    
    print("="*80)

def set_hp_bonus(data, position, nuts_count):
    """
    Modifie le bonus HP d'un personnage
    nuts_count: nombre de Nourishing Nuts consommés (chacun donne +75 HP)
    """
    hp_bonus = nuts_count * 75
    
    # Vérifie que la valeur ne dépasse pas le max (9999 HP)
    if hp_bonus > 9999:
        print(f"⚠️  Attention: {nuts_count} nuts = {hp_bonus} HP bonus, mais le jeu cap à 9999 HP")
    
    # Écrit la nouvelle valeur (2 bytes, little-endian)
    new_data = bytearray(data)
    struct.pack_into('<H', new_data, position, hp_bonus)
    
    return bytes(new_data)

def interactive_edit(save_path):
    """Mode interactif pour éditer les bonus HP"""
    data = read_save(save_path)
    
    # Trouve toutes les positions
    positions = find_doping_hp_positions(data)
    
    if len(positions) < 8:
        print(f"❌ Erreur: Seulement {len(positions)} positions trouvées (attendu 8)")
        return
    
    characters = ['Hikari', 'Agnea', 'Partitio', 'Osvald', 'Throné', 'Temenos', 'Ochette', 'Castti']
    
    while True:
        display_hp_bonuses(positions)
        
        print("\nOptions:")
        print("  1-8: Modifier le bonus HP d'un personnage")
        print("  9: Mettre tous les personnages au max (121 nuts = 9075 HP bonus)")
        print("  0: Sauvegarder et quitter")
        print("  q: Quitter sans sauvegarder")
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == 'q':
            print("❌ Annulé, aucune modification sauvegardée.")
            return
        
        if choice == '0':
            # Sauvegarder
            write_save(save_path, data)
            print("\n✅ Modifications sauvegardées!")
            return
        
        if choice == '9':
            # Max pour tous
            print("\n🚀 Application du maximum (121 nuts) à tous les personnages...")
            for pos_info in positions:
                data = set_hp_bonus(data, pos_info['pos'], 121)
                pos_info['bonus'] = 121 * 75
                pos_info['nuts_consumed'] = 121
            print("✅ Tous les personnages sont maintenant au maximum!")
            continue
        
        try:
            char_idx = int(choice) - 1
            if 0 <= char_idx < 8:
                char_name = characters[char_idx]
                current_nuts = positions[char_idx]['nuts_consumed']
                
                print(f"\n📝 Modification de {char_name}")
                print(f"   Actuellement: {current_nuts} Nourishing Nuts consommés")
                
                new_nuts = input(f"   Nouveau nombre de nuts (0-130): ").strip()
                
                try:
                    new_nuts = int(new_nuts)
                    if 0 <= new_nuts <= 130:
                        data = set_hp_bonus(data, positions[char_idx]['pos'], new_nuts)
                        positions[char_idx]['bonus'] = new_nuts * 75
                        positions[char_idx]['nuts_consumed'] = new_nuts
                        print(f"✅ {char_name} : {new_nuts} nuts ({new_nuts * 75} HP bonus)")
                    else:
                        print("❌ Valeur invalide (0-130)")
                except ValueError:
                    print("❌ Nombre invalide")
            else:
                print("❌ Choix invalide")
        except ValueError:
            print("❌ Choix invalide")

def main():
    print("="*80)
    print("ÉDITEUR DE BONUS HP (NOURISHING NUTS)")
    print("="*80)
    print("Modifie les compteurs de Nourishing Nuts consommés")
    print("Chaque nut donne +75 HP max")
    print("="*80)
    
    save_path = Path('SaveData/SaveData9.sav')
    
    if not save_path.exists():
        print(f"❌ Fichier non trouvé: {save_path}")
        return
    
    interactive_edit(str(save_path))

if __name__ == '__main__':
    main()
