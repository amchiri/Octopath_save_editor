"""
Éditeur de personnages CORRIGÉ avec les vraies positions
Basé sur l'analyse de SaveData9
"""

import struct
from pathlib import Path
import shutil


# POSITIONS RÉELLES trouvées dans SaveData9
# Pattern: HP à position X, SP à position X+39
TEMENOS_POSITIONS = {
    'name': 'Temenos',
    'hp_pos': 0x0008E4D4,      # HP = 946
    'sp_pos': 0x0008E4FB,      # SP = 125 (offset +39 depuis HP)
}

THRONE_POSITIONS = {
    'name': 'Throne',
    'hp_pos': 0x00091B8A,      # HP = 432
    'sp_pos': 0x00091BB1,      # SP = 100 (offset +39 depuis HP)
}

# Patterns découverts:
SP_OFFSET_FROM_HP = 39          # SP est à HP+39 octets
LEVEL_OFFSET_FROM_HP = -76      # Level est à HP-76 octets
HP_BONUS_OFFSET_FROM_HP = -156  # Compteur Nourishing Nuts (×75 HP max chacun)


def find_character_hp_positions(data: bytes) -> list:
    """
    Trouve toutes les positions RawHP dans le fichier
    La valeur HP est juste AVANT "RawMP"
    """
    mp_keyword = b'RawMP'
    positions = []
    
    pos = 0
    while True:
        pos = data.find(mp_keyword, pos)
        if pos == -1:
            break
        
        # La valeur HP est 8 octets AVANT "RawMP"
        # Pattern: ...VALEUR_HP(4 bytes)[type 4 bytes]RawMP...
        hp_value_pos = pos - 8
        if hp_value_pos >= 0:
            positions.append(hp_value_pos)
        
        pos += 1
    
    return positions


def read_int32(data: bytes, pos: int) -> int:
    """Lit un int32 little-endian"""
    return struct.unpack('<i', data[pos:pos+4])[0]


def write_int32(data: bytearray, pos: int, value: int):
    """Écrit un int32 little-endian"""
    data[pos:pos+4] = struct.pack('<i', value)


def display_all_characters(filepath: str):
    """Affiche les stats de tous les personnages détectés"""
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    hp_positions = find_character_hp_positions(data)
    
    print("\n" + "="*70)
    print(f"Personnages trouvés dans {Path(filepath).name}")
    print("="*70 + "\n")
    
    for i, hp_pos in enumerate(hp_positions[:8], 1):  # Les 8 premiers
        hp_value = read_int32(data, hp_pos)
        sp_pos = hp_pos + SP_OFFSET_FROM_HP
        sp_value = read_int32(data, sp_pos) if sp_pos + 4 <= len(data) else None
        level_pos = hp_pos + LEVEL_OFFSET_FROM_HP
        level_value = read_int32(data, level_pos) if level_pos >= 0 else None
        hp_bonus_pos = hp_pos + HP_BONUS_OFFSET_FROM_HP
        hp_bonus_count = read_int32(data, hp_bonus_pos) if hp_bonus_pos >= 0 else None
        
        print(f"Personnage {i}:")
        if level_value is not None:
            print(f"  Niveau: {level_value:3d}")
        print(f"  HP: {hp_value:6d}  (position: 0x{hp_pos:08X})")
        if sp_value is not None:
            print(f"  SP: {sp_value:6d}  (position: 0x{sp_pos:08X})")
        if hp_bonus_count is not None and hp_bonus_count > 0:
            print(f"  Bonus HP max: {hp_bonus_count} nuts (+{hp_bonus_count * 75} HP)")
        print()


def modify_character(filepath: str, char_index: int, new_hp: int = None, new_sp: int = None, new_level: int = None, new_hp_bonus: int = None):
    """
    Modifie un personnage spécifique
    char_index: 1-8 (numéro du personnage)
    new_hp_bonus: nombre de Nourishing Nuts (chaque nut = +75 HP max)
    """
    
    # Créé un backup
    backup_path = Path(filepath).with_suffix('.sav.backup')
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backup créé: {backup_path.name}")
    
    # Charge le fichier
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())
    
    # Trouve les positions HP
    hp_positions = find_character_hp_positions(data)
    
    if char_index < 1 or char_index > len(hp_positions):
        print(f"❌ Numéro de personnage invalide! (1-{len(hp_positions)})")
        return
    
    hp_pos = hp_positions[char_index - 1]
    sp_pos = hp_pos + SP_OFFSET_FROM_HP
    level_pos = hp_pos + LEVEL_OFFSET_FROM_HP
    hp_bonus_pos = hp_pos + HP_BONUS_OFFSET_FROM_HP
    
    # Lit les valeurs actuelles
    current_hp = read_int32(data, hp_pos)
    current_sp = read_int32(data, sp_pos)
    current_level = read_int32(data, level_pos) if level_pos >= 0 else None
    current_hp_bonus = read_int32(data, hp_bonus_pos) if hp_bonus_pos >= 0 else None
    
    print(f"\nPersonnage {char_index}:")
    if current_level is not None:
        print(f"  Niveau actuel: {current_level}")
    print(f"  HP actuel: {current_hp}")
    print(f"  SP actuel: {current_sp}")
    if current_hp_bonus is not None and current_hp_bonus > 0:
        print(f"  Bonus HP max actuel: {current_hp_bonus} nuts (+{current_hp_bonus * 75} HP)")
    
    # Modifie
    if new_level is not None and level_pos >= 0:
        write_int32(data, level_pos, new_level)
        print(f"  → Nouveau niveau: {new_level}")
    
    if new_hp_bonus is not None and hp_bonus_pos >= 0:
        write_int32(data, hp_bonus_pos, new_hp_bonus)
        print(f"  → Nouveau bonus HP max: {new_hp_bonus} nuts (+{new_hp_bonus * 75} HP)")
    
    if new_hp is not None:
        write_int32(data, hp_pos, new_hp)
        print(f"  → Nouveau HP: {new_hp}")
    
    if new_sp is not None:
        write_int32(data, sp_pos, new_sp)
        print(f"  → Nouveau SP: {new_sp}")
    
    # Sauvegarde
    with open(filepath, 'wb') as f:
        f.write(data)
    
    print(f"\n✓ Modifications sauvegardées dans {Path(filepath).name}")


def interactive_menu():
    """Menu interactif"""
    
    save_dir = Path(__file__).parent / "SaveData"
    save_files = sorted(save_dir.glob("*.sav"))
    
    if not save_files:
        print("Aucun fichier de sauvegarde trouvé!")
        return
    
    print("="*70)
    print("Éditeur de Personnages Octopath Traveler 2 (CORRIGÉ)")
    print("="*70 + "\n")
    
    print("Fichiers disponibles:")
    for i, f in enumerate(save_files):
        print(f"  {i}: {f.name}")
    
    try:
        choice = int(input("\nChoisissez un fichier: "))
        if choice < 0 or choice >= len(save_files):
            print("Choix invalide!")
            return
    except ValueError:
        print("Choix invalide!")
        return
    
    selected_file = str(save_files[choice])
    
    while True:
        print("\n" + "="*70)
        print("Menu:")
        print("  1. Afficher tous les personnages")
        print("  2. Modifier un personnage")
        print("  3. Modifier tous les personnages")
        print("  0. Quitter")
        print("="*70)
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == '0':
            break
        
        elif choice == '1':
            display_all_characters(selected_file)
        
        elif choice == '2':
            try:
                char_num = int(input("Numéro du personnage (1-8): "))
                level = input("Nouveau niveau (vide pour ignorer): ").strip()
                hp_bonus = input("Bonus HP max - nombre de nuts (vide pour ignorer): ").strip()
                hp = input("Nouveau HP (vide pour ignorer): ").strip()
                sp = input("Nouveau SP (vide pour ignorer): ").strip()
                
                new_level = int(level) if level else None
                new_hp_bonus = int(hp_bonus) if hp_bonus else None
                new_hp = int(hp) if hp else None
                new_sp = int(sp) if sp else None
                
                modify_character(selected_file, char_num, new_hp, new_sp, new_level, new_hp_bonus)
                
            except ValueError as e:
                print(f"Erreur: {e}")
        
        elif choice == '3':
            try:
                hp = input("Nouveau HP pour tous (vide pour ignorer): ").strip()
                sp = input("Nouveau SP pour tous (vide pour ignorer): ").strip()
                
                new_hp = int(hp) if hp else None
                new_sp = int(sp) if sp else None
                
                if new_hp is None and new_sp is None:
                    print("Aucune modification spécifiée!")
                    continue
                
                # Créé un backup
                backup_path = Path(selected_file).with_suffix('.sav.backup')
                shutil.copy2(selected_file, backup_path)
                print(f"✓ Backup créé: {backup_path.name}\n")
                
                # Charge le fichier
                with open(selected_file, 'rb') as f:
                    data = bytearray(f.read())
                
                # Trouve les positions HP
                hp_positions = find_character_hp_positions(data)
                
                print(f"Modification de {len(hp_positions[:8])} personnages...\n")
                
                for i, hp_pos in enumerate(hp_positions[:8], 1):
                    sp_pos = hp_pos + SP_OFFSET_FROM_HP
                    
                    current_hp = read_int32(data, hp_pos)
                    current_sp = read_int32(data, sp_pos)
                    
                    print(f"Personnage {i}:")
                    
                    if new_hp is not None:
                        write_int32(data, hp_pos, new_hp)
                        print(f"  HP: {current_hp} → {new_hp}")
                    
                    if new_sp is not None:
                        write_int32(data, sp_pos, new_sp)
                        print(f"  SP: {current_sp} → {new_sp}")
                
                # Sauvegarde
                with open(selected_file, 'wb') as f:
                    f.write(data)
                
                print(f"\n✓ Tous les personnages modifiés!")
                
            except ValueError as e:
                print(f"Erreur: {e}")
        
        else:
            print("Choix invalide!")
    
    print("\nAu revoir!")


if __name__ == "__main__":
    interactive_menu()
