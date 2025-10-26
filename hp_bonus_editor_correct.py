#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HP BONUS EDITOR - VERSION CORRECTE
Position corrigée: 0x0008FD18 (6 bytes AVANT l'ancienne position)
Cette position a été confirmée fonctionnelle par test utilisateur!
"""

import struct
from pathlib import Path
import shutil

# POSITIONS CORRIGÉES - 6 bytes AVANT les anciennes positions!
POSITIONS_HP_BONUS = [
    {'name': 'Hikari', 'pos': 0x0008116B},   # 0x00081171 - 6 = 0x0008116B
    {'name': 'Agnea', 'pos': 0x00088FAC},    # 0x00088FB2 - 6 = 0x00088FAC
    {'name': 'Partitio', 'pos': 0x0008AB07}, # 0x0008AB0D - 6 = 0x0008AB07
    {'name': 'Osvald', 'pos': 0x0008C662},   # 0x0008C668 - 6 = 0x0008C662
    {'name': 'Throné', 'pos': 0x0008E1BD},   # 0x0008E1C3 - 6 = 0x0008E1BD
    {'name': 'Temenos', 'pos': 0x0008FD18},  # 0x0008FD1E - 6 = 0x0008FD18 ✅ CONFIRMÉ!
    {'name': 'Ochette', 'pos': 0x00091873},  # 0x00091879 - 6 = 0x00091873
    {'name': 'Castti', 'pos': 0x000933CE},   # 0x000933D4 - 6 = 0x000933CE
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

def get_hp_bonus_values(save_data):
    """Lit les valeurs HP bonus pour tous les personnages"""
    values = {}
    for pos_info in POSITIONS_HP_BONUS:
        val = struct.unpack('<H', save_data[pos_info['pos']:pos_info['pos']+2])[0]
        values[pos_info['name']] = val
    return values

def set_hp_bonus(save_data, character_name, value):
    """Modifie le bonus HP d'un personnage"""
    data = bytearray(save_data)
    
    pos_info = next((p for p in POSITIONS_HP_BONUS if p['name'] == character_name), None)
    if not pos_info:
        print(f"❌ Personnage '{character_name}' non trouvé!")
        return None
    
    if value < 0 or value > 9999:
        print(f"❌ Valeur invalide: {value} (doit être entre 0 et 9999)")
        return None
    
    old_val = struct.unpack('<H', data[pos_info['pos']:pos_info['pos']+2])[0]
    struct.pack_into('<H', data, pos_info['pos'], value)
    
    print(f"✅ {character_name:10} @ 0x{pos_info['pos']:08X}: {old_val:5} → {value:5} HP bonus")
    return bytes(data)

def set_all_hp_bonus(save_data, value):
    """Modifie le bonus HP de TOUS les personnages à la même valeur"""
    data = bytearray(save_data)
    
    if value < 0 or value > 9999:
        print(f"❌ Valeur invalide: {value} (doit être entre 0 et 9999)")
        return None
    
    print(f"\n{'Personnage':<12} {'Position':<12} {'Ancien':<8} {'Nouveau':<8}")
    print("="*50)
    
    for pos_info in POSITIONS_HP_BONUS:
        old_val = struct.unpack('<H', data[pos_info['pos']:pos_info['pos']+2])[0]
        struct.pack_into('<H', data, pos_info['pos'], value)
        print(f"{pos_info['name']:<12} 0x{pos_info['pos']:08X}   {old_val:<8} {value:<8}")
    
    return bytes(data)

def interactive_edit():
    """Mode interactif pour éditer les bonus HP"""
    save_path = Path('SaveData/SaveData9.sav')
    
    if not save_path.exists():
        print(f"❌ Fichier non trouvé: {save_path}")
        return
    
    save_data = read_save(save_path)
    
    print("="*80)
    print("HP BONUS EDITOR - POSITIONS CORRECTES ✅")
    print("="*80)
    
    # Affiche les valeurs actuelles
    print("\nVALEURS ACTUELLES:")
    values = get_hp_bonus_values(save_data)
    for name, val in values.items():
        print(f"  {name:10}: {val:5} HP bonus")
    
    print("\n" + "="*80)
    print("OPTIONS:")
    print("  1) Modifier un personnage spécifique")
    print("  2) Mettre tous les personnages à la même valeur")
    print("  3) Mettre TOUS à 100 (1 Nourishing Nut)")
    print("  4) Mettre TOUS à 9999 (maximum)")
    print("  5) Afficher hex dump de Temenos (vérification)")
    print("  0) Quitter")
    print("="*80)
    
    choice = input("\nChoix: ").strip()
    
    if choice == '1':
        print("\nPersonnages disponibles:")
        for i, pos_info in enumerate(POSITIONS_HP_BONUS, 1):
            print(f"  {i}) {pos_info['name']}")
        
        char_num = input("Numéro du personnage: ").strip()
        try:
            char_idx = int(char_num) - 1
            if 0 <= char_idx < len(POSITIONS_HP_BONUS):
                char_name = POSITIONS_HP_BONUS[char_idx]['name']
                new_val = int(input(f"Nouvelle valeur pour {char_name} (0-9999): "))
                
                modified_data = set_hp_bonus(save_data, char_name, new_val)
                if modified_data:
                    write_save(save_path, modified_data)
        except ValueError:
            print("❌ Entrée invalide!")
    
    elif choice == '2':
        try:
            new_val = int(input("Valeur pour TOUS les personnages (0-9999): "))
            modified_data = set_all_hp_bonus(save_data, new_val)
            if modified_data:
                print("\n" + "="*80)
                write_save(save_path, modified_data)
        except ValueError:
            print("❌ Entrée invalide!")
    
    elif choice == '3':
        print("\nMise à 100 HP bonus (1 Nourishing Nut) pour tous...")
        modified_data = set_all_hp_bonus(save_data, 100)
        if modified_data:
            print("\n" + "="*80)
            write_save(save_path, modified_data)
    
    elif choice == '4':
        print("\nMise à 9999 HP bonus (maximum) pour tous...")
        modified_data = set_all_hp_bonus(save_data, 9999)
        if modified_data:
            print("\n" + "="*80)
            write_save(save_path, modified_data)
    
    elif choice == '5':
        pos = 0x0008FD18
        print(f"\nHEX DUMP de Temenos @ 0x{pos:08X} (±16 bytes):")
        start = max(0, pos - 16)
        end = min(len(save_data), pos + 16)
        
        for i in range(start, end, 16):
            hex_str = ' '.join(f'{b:02X}' for b in save_data[i:i+16])
            offset_str = f"0x{i:08X}"
            
            # Marque la position exacte
            if i <= pos < i + 16:
                marker = ' ' * ((pos - i) * 3) + '^^'
                print(f"{offset_str}: {hex_str}")
                print(f"           {marker} <- Position Temenos HP bonus")
            else:
                print(f"{offset_str}: {hex_str}")
        
        val = struct.unpack('<H', save_data[pos:pos+2])[0]
        print(f"\nValeur actuelle: {val} HP bonus ({val} nuts consommés)")

if __name__ == '__main__':
    interactive_edit()
