#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recherche et analyse de la structure MainStoryData
"""

import struct

SAVE_FILE = r"SaveData\SaveData9.sav"

def find_mainstorydata():
    """Trouve toutes les occurrences de MainStoryData"""
    
    with open(SAVE_FILE, 'rb') as f:
        data = f.read()
    
    search_term = b'MainStoryData'
    positions = []
    
    pos = 0
    while True:
        pos = data.find(search_term, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1
    
    print("=" * 70)
    print(f"RECHERCHE: MainStoryData")
    print("=" * 70)
    print(f"\n✅ Trouvé {len(positions)} occurrence(s)\n")
    
    for i, pos in enumerate(positions, 1):
        print(f"\n{'='*70}")
        print(f"Occurrence #{i} à position 0x{pos:08X}")
        print(f"{'='*70}")
        
        # Afficher le contexte autour
        start = max(0, pos - 100)
        end = min(len(data), pos + 500)
        
        context = data[start:end]
        
        # Chercher les structures
        print("\n📄 Contexte (texte ASCII):")
        for j in range(0, len(context), 80):
            chunk = context[j:j+80]
            ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"  {ascii_repr}")
        
        print("\n🔍 Hex dump (position relative à MainStoryData):")
        relative_start = pos - start
        for offset in range(0, min(400, len(context) - relative_start), 16):
            abs_pos = pos + offset
            hex_bytes = ' '.join(f'{b:02X}' for b in context[relative_start + offset:relative_start + offset + 16])
            ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in context[relative_start + offset:relative_start + offset + 16])
            print(f"  +0x{offset:04X} (0x{abs_pos:08X}): {hex_bytes:<48} | {ascii_repr}")

def analyze_story_structure():
    """Analyse la structure détaillée de MainStoryData"""
    
    with open(SAVE_FILE, 'rb') as f:
        data = f.read()
    
    # Chercher "MainStoryData" suivi de "StructProperty"
    search_pattern = b'MainStoryData\x00'
    
    pos = data.find(search_pattern)
    if pos == -1:
        print("❌ MainStoryData non trouvé")
        return
    
    print("\n" + "=" * 70)
    print("ANALYSE DE LA STRUCTURE MainStoryData")
    print("=" * 70)
    
    # Chercher les champs
    fields = [
        b'StoryID\x00',
        b'CurrentTaskID\x00', 
        b'State\x00',
        b'ConfirmedFlag\x00'
    ]
    
    print("\n🔍 Recherche des champs dans MainStoryData:")
    
    # Chercher dans une fenêtre après MainStoryData
    search_window = data[pos:pos+5000]
    
    field_positions = {}
    for field in fields:
        field_pos = search_window.find(field)
        if field_pos != -1:
            abs_pos = pos + field_pos
            field_name = field.decode('utf-8').rstrip('\x00')
            field_positions[field_name] = abs_pos
            print(f"  ✅ {field_name:20} trouvé à 0x{abs_pos:08X} (relatif: +0x{field_pos:04X})")
    
    print("\n" + "=" * 70)
    print("EXTRACTION DES VALEURS")
    print("=" * 70)
    
    # Pour chaque StoryID trouvé, extraire les valeurs
    storyid_positions = []
    search_pos = pos
    for _ in range(50):  # Chercher max 50 stories
        search_pos = data.find(b'StoryID\x00', search_pos + 1)
        if search_pos == -1 or search_pos > pos + 5000:
            break
        storyid_positions.append(search_pos)
    
    print(f"\n📊 Trouvé {len(storyid_positions)} structures StoryID\n")
    
    for idx, story_pos in enumerate(storyid_positions[:10], 1):  # Afficher les 10 premières
        print(f"\n--- Story #{idx} à 0x{story_pos:08X} ---")
        
        # Chercher IntProperty après StoryID pour trouver la valeur
        # Format: "StoryID\x00" suivi de "IntProperty\x00" puis la valeur
        after_storyid = data[story_pos:story_pos+100]
        
        intprop_pos = after_storyid.find(b'IntProperty\x00')
        if intprop_pos != -1:
            # La valeur Int32 est généralement 4 ou 8 bytes après "IntProperty\x00"
            value_offset = intprop_pos + len(b'IntProperty\x00') + 4  # Sauter le \x00 et 4 bytes
            if value_offset + 4 <= len(after_storyid):
                story_id = struct.unpack('<I', after_storyid[value_offset:value_offset+4])[0]
                print(f"  StoryID: {story_id}")
        
        # Chercher CurrentTaskID
        tasid_search = data[story_pos:story_pos+200]
        taskid_pos = tasid_search.find(b'CurrentTaskID\x00')
        if taskid_pos != -1:
            after_task = tasid_search[taskid_pos:]
            intprop_pos = after_task.find(b'IntProperty\x00')
            if intprop_pos != -1:
                value_offset = intprop_pos + len(b'IntProperty\x00') + 4
                if value_offset + 4 <= len(after_task):
                    task_id = struct.unpack('<I', after_task[value_offset:value_offset+4])[0]
                    print(f"  CurrentTaskID: {task_id}")
        
        # Chercher State
        state_search = data[story_pos:story_pos+250]
        state_pos = state_search.find(b'State\x00')
        if state_pos != -1:
            after_state = state_search[state_pos:]
            intprop_pos = after_state.find(b'IntProperty\x00')
            if intprop_pos != -1:
                value_offset = intprop_pos + len(b'IntProperty\x00') + 4
                if value_offset + 4 <= len(after_state):
                    state = struct.unpack('<I', after_state[value_offset:value_offset+4])[0]
                    print(f"  State: {state}")
        
        # Chercher ConfirmedFlag
        flag_search = data[story_pos:story_pos+300]
        flag_pos = flag_search.find(b'ConfirmedFlag\x00')
        if flag_pos != -1:
            after_flag = flag_search[flag_pos:]
            boolprop_pos = after_flag.find(b'BoolProperty\x00')
            if boolprop_pos != -1:
                value_offset = boolprop_pos + len(b'BoolProperty\x00') + 4
                if value_offset + 1 <= len(after_flag):
                    confirmed = after_flag[value_offset]
                    print(f"  ConfirmedFlag: {bool(confirmed)}")

if __name__ == "__main__":
    find_mainstorydata()
    analyze_story_structure()
