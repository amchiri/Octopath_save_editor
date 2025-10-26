#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Éditeur de chapitres basé sur MainStoryData
Permet de marquer des chapitres comme complétés en modifiant State
"""

import struct

SAVE_FILE = r"SaveData\SaveData9.sav"

def find_all_stories():
    """Trouve toutes les structures MainStorySaveData"""
    
    with open(SAVE_FILE, 'rb') as f:
        data = f.read()
    
    stories = []
    
    # Chercher toutes les occurrences de "StoryID"
    pos = 0
    story_positions = []
    
    while True:
        pos = data.find(b'StoryID\x00', pos)
        if pos == -1:
            break
        
        # Vérifier si c'est dans la zone MainStoryData (autour de 0x0039F000)
        if 0x0039F000 <= pos <= 0x003A8000:
            story_positions.append(pos)
        
        pos += 1
    
    print(f"✅ Trouvé {len(story_positions)} structures StoryID dans MainStoryData\n")
    
    # Pour chaque position, extraire les valeurs
    for idx, story_pos in enumerate(story_positions):
        # Lire StoryID (Int32 à +29 bytes après "StoryID\x00")
        storyid_value_pos = story_pos + 29
        story_id = struct.unpack('<I', data[storyid_value_pos:storyid_value_pos+4])[0]
        
        # Chercher CurrentTaskID après StoryID
        search_window = data[story_pos:story_pos+200]
        taskid_offset = search_window.find(b'CurrentTaskID\x00')
        if taskid_offset != -1:
            # Valeur à +29 bytes après "CurrentTaskID\x00"
            taskid_value_pos = story_pos + taskid_offset + 29
            current_task = struct.unpack('<I', data[taskid_value_pos:taskid_value_pos+4])[0]
        else:
            current_task = -1
        
        # Chercher State
        state_offset = search_window.find(b'State\x00')
        if state_offset != -1:
            # Valeur à +25 bytes après "State\x00"
            state_value_pos = story_pos + state_offset + 25
            state = struct.unpack('<I', data[state_value_pos:state_value_pos+4])[0]
        else:
            state = -1
        
        # Chercher ConfirmedFlag
        flag_offset = search_window.find(b'ConfirmedFlag\x00')
        if flag_offset != -1:
            # Valeur à +33 bytes après "ConfirmedFlag\x00"
            flag_value_pos = story_pos + flag_offset + 33
            confirmed = bool(data[flag_value_pos])
        else:
            confirmed = False
        
        stories.append({
            'index': idx,
            'storyid_pos': storyid_value_pos,
            'story_id': story_id,
            'task_id': current_task,
            'state_pos': state_value_pos if state_offset != -1 else None,
            'state': state,
            'confirmed_pos': flag_value_pos if flag_offset != -1 else None,
            'confirmed': confirmed
        })
    
    return stories

def display_stories(stories):
    """Affiche toutes les histoires"""
    
    print("=" * 80)
    print("LISTE DES MAINST ORYDATA")
    print("=" * 80)
    print(f"{'#':<4} {'StoryID':<10} {'TaskID':<10} {'State':<8} {'Confirmed':<10} {'Positions'}")
    print("-" * 80)
    
    for story in stories:
        print(f"{story['index']:<4} {story['story_id']:<10} {story['task_id']:<10} "
              f"{story['state']:<8} {story['confirmed']!s:<10} "
              f"0x{story['storyid_pos']:08X}")

def set_story_complete(story_index, story_id, state_value=5):
    """
    Active une histoire et la marque comme complétée
    
    Args:
        story_index: Index de la structure MainStorySaveData (0-26)
        story_id: L'ID de l'histoire à activer
        state_value: Valeur du State (5 semble être "complété")
    """
    
    stories = find_all_stories()
    
    if story_index >= len(stories):
        print(f"❌ Index {story_index} invalide (max: {len(stories)-1})")
        return False
    
    story = stories[story_index]
    
    with open(SAVE_FILE, 'rb') as f:
        data = bytearray(f.read())
    
    print(f"\n📝 Modification de MainStoryData[{story_index}]:")
    print(f"   StoryID: {story['story_id']} → {story_id}")
    print(f"   State: {story['state']} → {state_value}")
    
    # Écrire le nouveau StoryID
    data[story['storyid_pos']:story['storyid_pos']+4] = struct.pack('<I', story_id)
    
    # Écrire le nouveau State
    if story['state_pos']:
        data[story['state_pos']:story['state_pos']+4] = struct.pack('<I', state_value)
    
    # Écrire ConfirmedFlag à True
    if story['confirmed_pos']:
        data[story['confirmed_pos']] = 1
    
    # Sauvegarder
    with open(SAVE_FILE, 'wb') as f:
        f.write(data)
    
    print(f"\n✅ Sauvegarde modifiée avec succès!")
    return True

def interactive_menu():
    """Menu interactif"""
    
    while True:
        print("\n" + "=" * 80)
        print("ÉDITEUR DE CHAPITRES - MainStoryData")
        print("=" * 80)
        print("1. Afficher toutes les histoires")
        print("2. Marquer un chapitre comme complété")
        print("3. Tester: Hikari Chapitre 1 (ID supposé: 1)")
        print("4. Tester: Agnea Chapitre 1 (ID supposé: 6)")
        print("5. Tester: Partitio Chapitre 1 (ID supposé: 11)")
        print("0. Quitter")
        
        choice = input("\n>> Choix: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            stories = find_all_stories()
            display_stories(stories)
        elif choice == '2':
            index = int(input("Index de la structure (0-26): "))
            story_id = int(input("StoryID à définir: "))
            state = int(input("State (5 = complété): "))
            set_story_complete(index, story_id, state)
        elif choice == '3':
            print("\n🧪 Test: Hikari Chapitre 1 (ID hypothétique: 1)")
            set_story_complete(0, 1, 5)
        elif choice == '4':
            print("\n🧪 Test: Agnea Chapitre 1 (ID hypothétique: 6)")
            set_story_complete(1, 6, 5)
        elif choice == '5':
            print("\n🧪 Test: Partitio Chapitre 1 (ID hypothétique: 11)")
            set_story_complete(2, 11, 5)

if __name__ == "__main__":
    print("=" * 80)
    print("ANALYSE PRÉLIMINAIRE")
    print("=" * 80)
    stories = find_all_stories()
    display_stories(stories)
    
    print("\n" + "=" * 80)
    print("OBSERVATION:")
    print("  - 27 structures MainStorySaveData disponibles")
    print("  - Toutes ont StoryID = 0 (vides)")
    print("  - State peut être utilisé pour marquer comme complété")
    print("=" * 80)
    
    interactive_menu()
