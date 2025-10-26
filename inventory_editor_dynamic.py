"""
Éditeur d'inventaire DYNAMIQUE - Détection automatique des items
"""

import struct
from pathlib import Path
import shutil

def scan_all_items(data):
    """
    Scanne TOUS les items dans le fichier de sauvegarde.
    Retourne la liste de leurs positions (offset de la quantité).
    """
    positions = []
    
    # Chercher toutes les occurrences de "None" suivies de "ItemId"
    search_pos = 0
    while True:
        none_pos = data.find(b'None\x00', search_pos)
        if none_pos == -1:
            break
        
        # Vérifier si "ItemId" est proche après (dans les 30 bytes)
        itemid_pos = data.find(b'ItemId\x00', none_pos, none_pos + 30)
        if itemid_pos != -1:
            # La quantité est 8 bytes AVANT "None"
            qty_pos = none_pos - 8
            if qty_pos >= 0:
                positions.append(qty_pos)
        
        search_pos = none_pos + 1
    
    return sorted(positions)

def read_int32(data, pos):
    return struct.unpack('<i', data[pos:pos+4])[0]

def write_int32(data, pos, value):
    data[pos:pos+4] = struct.pack('<i', value)

def display_inventory(filepath):
    """Affiche l'inventaire aux positions détectées"""
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Scanner dynamiquement
    item_positions = scan_all_items(data)
    
    print("\n" + "="*70)
    print(f"INVENTAIRE - {Path(filepath).name} - {len(item_positions)} items détectés")
    print("="*70)
    print(f"\n{'#':<4} {'Position':<12} {'Quantité':<10} {'ItemId':<10}")
    print("-" * 70)
    
    for i, pos in enumerate(item_positions, 1):
        try:
            qty = read_int32(data, pos)
            itemid = read_int32(data, pos + 49)  # ItemId est 49 bytes après qty
            if qty > 0:
                print(f"{i:<4} 0x{pos:08X}  {qty:<10} {itemid:<10}")
        except:
            pass

def modify_position(filepath, position, new_quantity):
    """Modifie la quantité à une position spécifique"""
    
    backup_path = Path(filepath).with_suffix('.sav.backup')
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backup créé: {backup_path.name}")
    
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())
    
    old_qty = read_int32(data, position)
    write_int32(data, position, new_quantity)
    
    print(f"\nPosition 0x{position:08X}:")
    print(f"  Quantité: {old_qty} → {new_quantity}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    
    print(f"\n✓ Modifications sauvegardées!")

def set_all_to_99(filepath):
    """Met TOUS les items détectés à 99"""
    
    backup_path = Path(filepath).with_suffix('.sav.backup2')
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backup créé: {backup_path.name}")
    
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())
    
    # Scanner dynamiquement
    item_positions = scan_all_items(data)
    
    print(f"\n🔧 Modification de {len(item_positions)} items à 99...")
    print("-" * 70)
    
    for i, pos in enumerate(item_positions, 1):
        try:
            old_qty = read_int32(data, pos)
            write_int32(data, pos, 99)
            itemid = read_int32(data, pos + 49)
            print(f"  #{i:3d} @ 0x{pos:08X}: {old_qty:5d} → 99 (ItemId={itemid})")
        except Exception as e:
            print(f"  #{i:3d} @ 0x{pos:08X}: ERREUR - {e}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    
    print(f"\n✓ {len(item_positions)} items modifiés à 99!")

def interactive_menu():
    save_dir = Path(__file__).parent / "SaveData"
    save_files = sorted(save_dir.glob("*.sav"))
    
    print("="*70)
    print("Éditeur d'Inventaire DYNAMIQUE - Octopath Traveler 2")
    print("="*70 + "\n")
    
    print("Fichiers disponibles:")
    for i, f in enumerate(save_files):
        print(f"  {i}: {f.name}")
    
    try:
        choice = int(input("\nChoisissez un fichier: "))
        selected_file = str(save_files[choice])
    except:
        print("Choix invalide!")
        return
    
    while True:
        print("\n" + "="*70)
        print("Menu:")
        print("  1. Afficher l'inventaire (détection auto)")
        print("  2. Modifier une position")
        print("  3. Mettre TOUS les items à 99 (détection auto)")
        print("  0. Quitter")
        print("="*70)
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == '0':
            break
        
        elif choice == '1':
            display_inventory(selected_file)
        
        elif choice == '2':
            try:
                pos_str = input("Position (ex: 0x00017090): ").strip()
                if pos_str.startswith('0x'):
                    position = int(pos_str, 16)
                else:
                    position = int(pos_str)
                
                quantity = int(input("Nouvelle quantité: "))
                
                if quantity < 0:
                    print("❌ La quantité ne peut pas être négative!")
                    continue
                
                modify_position(selected_file, position, quantity)
                
            except ValueError as e:
                print(f"Erreur: {e}")
        
        elif choice == '3':
            try:
                confirm = input("Mettre TOUS les items détectés à 99? (oui/non): ").lower()
                if confirm in ['oui', 'o', 'yes', 'y']:
                    set_all_to_99(selected_file)
            except Exception as e:
                print(f"Erreur: {e}")
        
        else:
            print("Choix invalide!")
    
    print("\nAu revoir!")

if __name__ == "__main__":
    interactive_menu()
