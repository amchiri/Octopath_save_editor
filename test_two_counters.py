#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de l'hypothèse des DEUX compteurs:
- Position -6 bytes: Compteur de nuts consommés (limite max)
- Position +0 bytes: Bonus HP actif (ne peut pas dépasser le compteur)
"""

import struct
from pathlib import Path
import shutil

# Pour Temenos (on teste sur lui)
TEMENOS_COUNTER_POS = 0x0008FD18  # Compteur nuts (6 bytes avant)
TEMENOS_BONUS_POS = 0x0008FD1E    # Bonus HP actif

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def write_save(filepath, data, suffix=''):
    backup_path = str(filepath) + f'.backup{suffix}'
    shutil.copy(filepath, backup_path)
    print(f"✅ Backup: {backup_path}")
    
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"✅ Sauvegardé: {filepath}")

save_path = Path('SaveData/SaveData9.sav')
save_data = read_save(save_path)

print("="*80)
print("TEST HYPOTHÈSE: DEUX COMPTEURS POUR TEMENOS")
print("="*80)

# Lit les valeurs actuelles
counter = struct.unpack('<H', save_data[TEMENOS_COUNTER_POS:TEMENOS_COUNTER_POS+2])[0]
bonus = struct.unpack('<H', save_data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+2])[0]

print(f"\nVALEURS ACTUELLES:")
print(f"  Position 0x{TEMENOS_COUNTER_POS:08X}: {counter:5} (compteur nuts?)")
print(f"  Position 0x{TEMENOS_BONUS_POS:08X}: {bonus:5} (bonus HP actif?)")

print("\n" + "="*80)
print("TESTS POSSIBLES:")
print("  1) Mettre compteur=9999, bonus=100 (beaucoup de nuts, petit bonus)")
print("  2) Mettre compteur=100, bonus=100 (égaux)")
print("  3) Mettre compteur=500, bonus=500 (égaux, valeur moyenne)")
print("  4) Mettre compteur=9999, bonus=9999 (maximum partout)")
print("  5) Mettre compteur=0, bonus=0 (reset complet)")
print("  0) Annuler")
print("="*80)

choice = input("\nChoix: ").strip()

data = bytearray(save_data)

if choice == '1':
    print("\nTest: compteur=9999, bonus=100")
    struct.pack_into('<H', data, TEMENOS_COUNTER_POS, 9999)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, 100)
    write_save(save_path, bytes(data), '_test1')
    print("\n✅ Temenos devrait avoir ~978 HP (878 base + 100 bonus)")

elif choice == '2':
    print("\nTest: compteur=100, bonus=100")
    struct.pack_into('<H', data, TEMENOS_COUNTER_POS, 100)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, 100)
    write_save(save_path, bytes(data), '_test2')
    print("\n✅ Temenos devrait avoir ~978 HP (878 base + 100 bonus)")

elif choice == '3':
    print("\nTest: compteur=500, bonus=500")
    struct.pack_into('<H', data, TEMENOS_COUNTER_POS, 500)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, 500)
    write_save(save_path, bytes(data), '_test3')
    print("\n✅ Temenos devrait avoir ~1378 HP (878 base + 500 bonus)")

elif choice == '4':
    print("\nTest: compteur=9999, bonus=9999")
    struct.pack_into('<H', data, TEMENOS_COUNTER_POS, 9999)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, 9999)
    write_save(save_path, bytes(data), '_test4')
    print("\n✅ Temenos devrait avoir ~10877 HP (878 base + 9999 bonus)")

elif choice == '5':
    print("\nTest: compteur=0, bonus=0")
    struct.pack_into('<H', data, TEMENOS_COUNTER_POS, 0)
    struct.pack_into('<H', data, TEMENOS_BONUS_POS, 0)
    write_save(save_path, bytes(data), '_test5')
    print("\n✅ Temenos devrait avoir 878 HP (base, aucun bonus)")

else:
    print("\nAnnulé.")
    exit()

# Vérification
counter_new = struct.unpack('<H', data[TEMENOS_COUNTER_POS:TEMENOS_COUNTER_POS+2])[0]
bonus_new = struct.unpack('<H', data[TEMENOS_BONUS_POS:TEMENOS_BONUS_POS+2])[0]

print(f"\nVALEURS ÉCRITES:")
print(f"  Position 0x{TEMENOS_COUNTER_POS:08X}: {counter_new:5}")
print(f"  Position 0x{TEMENOS_BONUS_POS:08X}: {bonus_new:5}")

print("\n" + "="*80)
print("Charge SaveData9 dans le jeu et vérifie les HP de Temenos!")
print("="*80)
