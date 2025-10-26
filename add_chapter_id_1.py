#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ajouter l'ID 1 (devrait être Hikari Chapitre 1) à la liste des chapitres completés
"""

import struct

SAVE_FILE = r"SaveData\SaveData9.sav"
CLEAREDMS_DATA_START = 0x000E3428

def add_chapter_id(chapter_id):
    """Ajoute un chapter ID à la liste des chapitres completés"""
    
    with open(SAVE_FILE, 'rb') as f:
        data = bytearray(f.read())
    
    print(f"🔍 Recherche du premier slot vide (0xFFFFFFFF)...")
    
    # Parcourir les IDs existants (Int32)
    pos = CLEAREDMS_DATA_START
    slot = 0
    
    while pos < len(data) - 4:
        value = struct.unpack('<I', data[pos:pos+4])[0]
        
        if value == 0xFFFFFFFF:
            print(f"\n✅ Slot vide trouvé à position 0x{pos:08X} (slot #{slot})")
            
            # Écrire le nouvel ID
            data[pos:pos+4] = struct.pack('<I', chapter_id)
            print(f"📝 Écriture de l'ID {chapter_id} (0x{chapter_id:08X})")
            
            # Sauvegarder
            with open(SAVE_FILE, 'wb') as f:
                f.write(data)
            
            print(f"\n💾 Sauvegarde modifiée avec succès!")
            print(f"\n🎮 Chargez SaveData9 dans le jeu pour voir quel chapitre apparaît comme complété")
            
            # Afficher la nouvelle liste
            print(f"\n📋 Liste des chapitres completés:")
            pos2 = CLEAREDMS_DATA_START
            idx = 0
            while pos2 < len(data) - 4:
                val = struct.unpack('<I', data[pos2:pos2+4])[0]
                if val == 0xFFFFFFFF:
                    break
                print(f"  Slot {idx}: ID {val}")
                pos2 += 4
                idx += 1
            
            return True
        
        pos += 4
        slot += 1
    
    print("❌ Aucun slot vide trouvé!")
    return False

if __name__ == "__main__":
    print("=" * 70)
    print("AJOUT DE L'ID 1 (Test: Hikari Chapitre 1?)")
    print("=" * 70)
    add_chapter_id(1)
