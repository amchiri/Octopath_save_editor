#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compare SaveData9 modifié vs SaveData9_result pour voir si les HP bonus ont changé
"""

import struct

def read_save(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

# Positions des compteurs HP bonus
POSITIONS = {
    'Hikari': 0x00081171,
    'Agnea': 0x00088FB2,
    'Partitio': 0x0008AB0D,
    'Osvald': 0x0008C668,
    'Throné': 0x0008E1C3,
    'Temenos': 0x0008FD1E,
    'Ochette': 0x00091879,
    'Castti': 0x000933D4,
}

try:
    save9_modified = read_save('SaveData/SaveData9.sav')
    save9_result = read_save('SaveData/SaveDataresult.sav')
    
    print("="*80)
    print("COMPARAISON: SaveData9 (modifié) vs SaveDataresult (après jeu)")
    print("="*80)
    
    print("\nHP BONUS COMPTEURS:")
    print("-"*80)
    print(f"{'Personnage':<12} {'Position':<12} {'Modifié':<10} {'Résultat':<10} {'Changé?'}")
    print("-"*80)
    
    for name, pos in POSITIONS.items():
        val_modified = struct.unpack('<H', save9_modified[pos:pos+2])[0]
        val_result = struct.unpack('<H', save9_result[pos:pos+2])[0]
        
        changed = "✅ OUI" if val_modified != val_result else "❌ NON"
        
        print(f"{name:<12} 0x{pos:08X}  {val_modified:<10} {val_result:<10} {changed}")
    
    print("\n" + "="*80)
    print("FOCUS: THRONÉ ET TEMENOS")
    print("="*80)
    
    throne_mod = struct.unpack('<H', save9_modified[POSITIONS['Throné']:POSITIONS['Throné']+2])[0]
    throne_res = struct.unpack('<H', save9_result[POSITIONS['Throné']:POSITIONS['Throné']+2])[0]
    
    temenos_mod = struct.unpack('<H', save9_modified[POSITIONS['Temenos']:POSITIONS['Temenos']+2])[0]
    temenos_res = struct.unpack('<H', save9_result[POSITIONS['Temenos']:POSITIONS['Temenos']+2])[0]
    
    print(f"\nThroné @ 0x{POSITIONS['Throné']:08X}:")
    print(f"  Avant (modifié): {throne_mod} HP bonus")
    print(f"  Après (result):  {throne_res} HP bonus")
    print(f"  Différence: {throne_res - throne_mod:+d}")
    
    print(f"\nTemenos @ 0x{POSITIONS['Temenos']:08X}:")
    print(f"  Avant (modifié): {temenos_mod} HP bonus")
    print(f"  Après (result):  {temenos_res} HP bonus")
    print(f"  Différence: {temenos_res - temenos_mod:+d}")
    
    if throne_res != throne_mod or temenos_res != temenos_mod:
        print("\n🎉 LES COMPTEURS ONT CHANGÉ!")
        print("   Le jeu a bien pris en compte les modifications!")
        print("   Les valeurs ont probablement été ajustées après consommation des nuts.")
    else:
        print("\n⚠️  Les compteurs n'ont pas changé.")
        print("   Soit le jeu n'a pas touché aux compteurs,")
        print("   soit aucun nut n'a été consommé dans le jeu.")

except FileNotFoundError as e:
    print(f"❌ Fichier non trouvé: {e}")
    print("\nVérifie que SaveDataresult.sav existe dans le dossier SaveData/")
