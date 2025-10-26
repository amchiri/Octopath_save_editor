#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HP BONUS EDITOR - AVEC COMPTEUR LIMITEUR
Position compteur: 0x0008FD1A (4 bytes avant le bonus)
Position bonus: 0x0008FD1E
Le bonus ne s'applique que si compteur >= bonus!
"""

import struct
from pathlib import Path
import shutil

# Positions pour TEMENOS (on va tester sur lui d'abord)
TEMENOS_LIMITER_POS = 0x0008FD1A  # Compteur limiteur (4 bytes avant bonus)
TEMENOS_BONUS_POS = 0x0008FD1E    # Bonus HP actif

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data):
    backup_path = str(filepath) + '.backup_correct'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Sauvegardé: {filepath}")

save_path = Path('SaveData/SaveData9.sav')
save_data = read_save(save_path)
data = bytearray(save_data)

print("="*80)
print("HP BONUS EDITOR - AVEC COMPTEUR LIMITEUR ✅")
print("="*80)

# Lit les valeurs actuelles
limiter = struct.unpack('<H', save_data[TEMENOS_LIMITER_POS:TEMENOS_LIMITER_POS+2])[0]
bonus = struct.unpack('<H', save_data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+2])[0]

print(f"\nVALEURS ACTUELLES TEMENOS:")
print(f"  Compteur limiteur @ 0x{TEMENOS_LIMITER_POS:08X}: {limiter:5}")
print(f"  Bonus HP actif    @ 0x{TEMENOS_BONUS_POS:08X}: {bonus:5}")

print("\n" + "="*80)
print("ENTREZ LA VALEUR DE BONUS HP DÉSIRÉE:")
print("(Le compteur limiteur sera automatiquement mis à la même valeur)")
print("="*80)

try:
    desired_bonus = int(input("\nBonus HP (0-9999): "))
    
    if desired_bonus < 0 or desired_bonus > 9999:
        print("❌ Valeur invalide!")
        exit()
    
    # Met le compteur limiteur ET le bonus à la même valeur
    struct.pack_into('<H', data, TEMENOS_LIMITER_POS, desired_bonus)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, desired_bonus)
    
    print(f"\n✅ Modifications:")
    print(f"  Compteur limiteur: {limiter:5} → {desired_bonus:5}")
    print(f"  Bonus HP:          {bonus:5} → {desired_bonus:5}")
    
    write_save(save_path, bytes(data))
    
    expected_hp = 878 + desired_bonus
    print(f"\n✅ Temenos devrait avoir ~{expected_hp} HP dans le jeu!")
    print("   (878 base + {} bonus)".format(desired_bonus))
    
except ValueError:
    print("❌ Entrée invalide!")
