#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyser le pattern des IDs de chapitres completés
IDs actuels: 26, 27, 21, 31, 33
"""

import struct

def analyze_pattern():
    """Analyse les IDs de chapitres pour trouver le pattern réel"""
    
    # IDs actuellement dans la sauvegarde
    chapter_ids = [26, 27, 21, 31, 33]
    
    print("=" * 70)
    print("ANALYSE DES IDs DE CHAPITRES")
    print("=" * 70)
    
    print("\n📊 IDs trouvés dans Endroll_ClearedMS:")
    for i, cid in enumerate(chapter_ids, 1):
        print(f"  Slot {i}: ID {cid} (0x{cid:02X})")
    
    print("\n" + "=" * 70)
    print("HYPOTHÈSES DE DÉCODAGE")
    print("=" * 70)
    
    # Hypothèse 1: (Personnage * 5) + Chapitre
    print("\n💡 Hypothèse 1: ID = (Personnage × 5) + Chapitre")
    print("   (Personnages 0-7, Chapitres 1-5)")
    for cid in chapter_ids:
        char = cid // 5
        chapter = cid % 5
        if chapter == 0:
            chapter = 5
            char -= 1
        print(f"  ID {cid:2d} → Personnage {char}, Chapitre {chapter}")
    
    # Hypothèse 2: (Personnage * 6) + Chapitre  
    print("\n💡 Hypothèse 2: ID = (Personnage × 6) + Chapitre")
    print("   (Personnages 0-7, Chapitres 1-5)")
    for cid in chapter_ids:
        char = cid // 6
        chapter = cid % 6
        if chapter == 0:
            chapter = 6
            char -= 1
        print(f"  ID {cid:2d} → Personnage {char}, Chapitre {chapter}")
    
    # Hypothèse 3: Groupes de 10
    print("\n💡 Hypothèse 3: ID = (Personnage × 10) + Chapitre")
    print("   (Personnages 0-7, Chapitres 1-5)")
    for cid in chapter_ids:
        char = cid // 10
        chapter = cid % 10
        print(f"  ID {cid:2d} → Personnage {char}, Chapitre {chapter}")
    
    # Hypothèse 4: Base 20 (deux chiffres en base 10)
    print("\n💡 Hypothèse 4: ID comme '2 chiffres' (dizaines + unités)")
    print("   Dizaines = Personnage, Unités = Chapitre")
    for cid in chapter_ids:
        char = cid // 10
        chapter = cid % 10
        print(f"  ID {cid:2d} → Personnage {char}, Chapitre {chapter}")
    
    # Analyse des différences
    print("\n" + "=" * 70)
    print("ANALYSE DES DIFFÉRENCES ENTRE IDs")
    print("=" * 70)
    sorted_ids = sorted(chapter_ids)
    print(f"\nIDs triés: {sorted_ids}")
    for i in range(len(sorted_ids) - 1):
        diff = sorted_ids[i+1] - sorted_ids[i]
        print(f"  {sorted_ids[i]} → {sorted_ids[i+1]}: +{diff}")
    
    # Range analysis
    print("\n" + "=" * 70)
    print("ANALYSE DES RANGES")
    print("=" * 70)
    print(f"\nID minimum: {min(chapter_ids)}")
    print(f"ID maximum: {max(chapter_ids)}")
    print(f"Range totale: {max(chapter_ids) - min(chapter_ids)}")
    
    # Regroupement par dizaines
    print("\n📦 Regroupement par dizaines:")
    by_tens = {}
    for cid in chapter_ids:
        tens = cid // 10
        if tens not in by_tens:
            by_tens[tens] = []
        by_tens[tens].append(cid)
    
    for tens in sorted(by_tens.keys()):
        print(f"  20-29: {by_tens[tens] if tens == 2 else 'aucun'}")
        print(f"  30-39: {by_tens[tens] if tens == 3 else 'aucun'}")
    
    print("\n" + "=" * 70)
    print("OBSERVATION:")
    print("  - 3 IDs dans les 20-29: 26, 27, 21")
    print("  - 2 IDs dans les 30-39: 31, 33")
    print("  - Pattern probable: dizaines = personnage, unités = chapitre")
    print("  - ID 21 = Personnage 2, Chapitre 1")
    print("  - ID 26 = Personnage 2, Chapitre 6 ??? (impossible, 5 chapitres max)")
    print("  - ID 27 = Personnage 2, Chapitre 7 ??? (impossible)")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("HYPOTHÈSE RÉVISÉE")
    print("=" * 70)
    print("\nPeut-être que les IDs ne suivent pas une formule mathématique simple.")
    print("Il faut tester méthodiquement en ajoutant des IDs connus du jeu.")
    print("\n🧪 Suggestion de tests:")
    print("  1. Ajouter ID 1, 2, 3, 4, 5 (premiers IDs possibles)")
    print("  2. Ajouter ID 10, 11, 12, 13, 14 (dizaines)")
    print("  3. Observer quel personnage/chapitre s'active dans le jeu")
    
    # Suggestion de tous les IDs à tester
    print("\n" + "=" * 70)
    print("IDs POSSIBLES À TESTER (si pattern = dizaines×10 + chapitre)")
    print("=" * 70)
    
    characters = ["Hikari", "Agnea", "Partitio", "Osvald", "Throné", "Temenos", "Ochette", "Castti"]
    
    print("\nSi le pattern est: ID = (Perso × 10) + Chapitre")
    print("Alors voici les IDs attendus pour chaque personnage:\n")
    
    for char_idx, char_name in enumerate(characters):
        ids = [char_idx * 10 + ch for ch in range(1, 6)]
        print(f"  {char_name:10} (#{char_idx}): {ids}")
    
    print("\n⚠️  MAIS les IDs existants ne suivent pas ce pattern!")
    print("     ID 21 devrait être Perso 2 Chapitre 1")
    print("     Mais on a aussi 26, 27 qui dépassent 25...")

if __name__ == "__main__":
    analyze_pattern()
