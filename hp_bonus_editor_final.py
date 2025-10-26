#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ÉDITEUR DE BONUS HP (NOURISHING NUTS) - VERSION FINALE
Positions exactes pour les 8 personnages principaux
"""

import struct
from pathlib import Path
import shutil

# POSITIONS EXACTES des compteurs HP bonus pour chaque personnage
# Ajusté +4 bytes par rapport à la détection automatique
POSITIONS_HP_BONUS = [
    {'name': 'Hikari', 'pos': 0x00081171},
    {'name': 'Agnea', 'pos': 0x00088FB2},
    {'name': 'Partitio', 'pos': 0x0008AB0D},
    {'name': 'Osvald', 'pos': 0x0008C668},
    {'name': 'Throné', 'pos': 0x0008E1C3},
    {'name': 'Temenos', 'pos': 0x0008FD1E},
    {'name': 'Ochette', 'pos': 0x00091879},
    {'name': 'Castti', 'pos': 0x000933D4},
]

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Fichier sauvegardé: {filepath}")

def get_hp_bonus_values(data):
    """Lit les bonus HP actuels"""
    values = []
    for pos_info in POSITIONS_HP_BONUS:
        bonus = struct.unpack('<H', data[pos_info['pos']:pos_info['pos']+2])[0]
        values.append({
            'name': pos_info['name'],
            'pos': pos_info['pos'],
            'bonus': bonus,
            'nuts': bonus // 75
        })
    return values

def set_hp_bonus(data, char_index, nuts_count):
    """Modifie le bonus HP d'un personnage"""
    hp_bonus = nuts_count * 75
    pos = POSITIONS_HP_BONUS[char_index]['pos']
    
    new_data = bytearray(data)
    struct.pack_into('<H', new_data, pos, hp_bonus)
    return bytes(new_data)

def set_all_hp_bonus(data, nuts_count):
    """Modifie le bonus HP de tous les personnages"""
    hp_bonus = nuts_count * 75
    new_data = bytearray(data)
    
    for pos_info in POSITIONS_HP_BONUS:
        struct.pack_into('<H', new_data, pos_info['pos'], hp_bonus)
    
    return bytes(new_data)

def display_hp_bonuses(values):
    """Affiche les bonus HP"""
    print("\n" + "="*80)
    print("BONUS HP ACTUELS (NOURISHING NUTS)")
    print("="*80)
    for idx, val in enumerate(values):
        print(f"{idx+1}. {val['name']:10} @ 0x{val['pos']:08X}: "
              f"{val['bonus']:5} HP bonus ({val['nuts']:3} nuts)")
    print("="*80)

def interactive_edit(save_path):
    """Mode interactif"""
    data = read_save(save_path)
    
    while True:
        values = get_hp_bonus_values(data)
        display_hp_bonuses(values)
        
        print("\nOptions:")
        print("  1-8: Modifier un personnage")
        print("  a: Modifier TOUS les personnages")
        print("  0: Sauvegarder et quitter")
        print("  q: Quitter sans sauvegarder")
        
        choice = input("\nVotre choix: ").strip().lower()
        
        if choice == 'q':
            print("❌ Annulé")
            return
        
        if choice == '0':
            write_save(save_path, data)
            print("\n✅ Modifications sauvegardées!")
            return
        
        if choice == 'a':
            nuts = input("Nombre de nuts pour TOUS (0-130, défaut 121): ").strip()
            nuts = int(nuts) if nuts else 121
            
            if 0 <= nuts <= 130:
                data = set_all_hp_bonus(data, nuts)
                print(f"✅ Tous les personnages: {nuts} nuts ({nuts*75} HP bonus)")
            else:
                print("❌ Valeur invalide")
            continue
        
        try:
            char_idx = int(choice) - 1
            if 0 <= char_idx < 8:
                char_name = POSITIONS_HP_BONUS[char_idx]['name']
                current_nuts = values[char_idx]['nuts']
                
                print(f"\n📝 {char_name} (actuellement: {current_nuts} nuts)")
                nuts = input(f"Nouveau nombre de nuts (0-130): ").strip()
                
                try:
                    nuts = int(nuts)
                    if 0 <= nuts <= 130:
                        data = set_hp_bonus(data, char_idx, nuts)
                        print(f"✅ {char_name}: {nuts} nuts ({nuts*75} HP bonus)")
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
    print("ÉDITEUR DE BONUS HP (NOURISHING NUTS) - VERSION FINALE")
    print("="*80)
    print("Chaque Nourishing Nut donne +75 HP max")
    print("Maximum recommandé: 121 nuts = 9075 HP bonus")
    print("="*80)
    
    save_path = Path('SaveData/SaveData6.sav')
    
    if not save_path.exists():
        print(f"❌ Fichier non trouvé: {save_path}")
        return
    
    interactive_edit(save_path)

if __name__ == '__main__':
    main()
