import struct
import sys

def find_string_position(data, search_string):
    """Trouve la position d'une chaîne dans les données"""
    search_bytes = search_string.encode('utf-8')
    pos = data.find(search_bytes)
    return pos if pos != -1 else None

def parse_int_property(data, start_pos):
    """
    Parse un IntProperty
    Structure: [Nom]\x00 + \x0C\x00\x00\x00 + IntProperty\x00 + \x04\x00\x00\x00 + \x00\x00\x00\x00 + \x00 + VALEUR(4 bytes)
    La valeur Int32 est à +21 bytes après "IntProperty\x00"
    """
    # Chercher "IntProperty\x00" après la position
    int_prop = data.find(b"IntProperty\x00", start_pos, start_pos + 50)
    if int_prop == -1:
        return None, None
    
    # D'après votre exemple:
    # IntProperty\x00 (12 bytes) + \x04\x00\x00\x00 (4 bytes) + \x00\x00\x00\x00 (4 bytes) + \x00 (1 byte) + VALEUR (4 bytes)
    # = 12 + 4 + 4 + 1 = 21 bytes
    value_pos = int_prop + 21
    value = struct.unpack_from('<i', data, value_pos)[0]
    
    return value, value_pos

def parse_bool_property(data, start_pos):
    """
    Parse un BoolProperty
    Structure: ConfirmedFlag\x00 + \x0D\x00\x00\x00 + BoolProperty\x00 + \x00\x00\x00\x00 + \x00\x00\x00\x00 + \x00
    Suivi de: \x00\x00\x00\x05\x00\x00\x00None\x00...
    """
    # Chercher "BoolProperty\x00" après la position
    bool_prop = data.find(b"BoolProperty\x00", start_pos, start_pos + 50)
    if bool_prop == -1:
        return None, None
    
    # La valeur bool est juste après BoolProperty\x00 + padding
    # BoolProperty\x00 (13 bytes) + \x00\x00\x00\x00 (4) + \x00\x00\x00\x00 (4) + BOOL (1 byte)
    value_pos = bool_prop + len("BoolProperty\x00") + 8
    value = data[value_pos] != 0
    
    return value, value_pos

def scan_all_mainstorydata(data):
    """Scanne toutes les entrées MainStoryData avec la structure correcte"""
    
    # Trouver MainStoryData
    pos = find_string_position(data, "MainStoryData")
    if not pos:
        print("[ERREUR] MainStoryData non trouve!")
        return []
    
    print(f"[OK] MainStoryData trouve a l'adresse: 0x{pos:08X}\n")
    
    # Chercher toutes les occurrences de "StoryID\x00" dans une plage
    search_range = 50000
    end_pos = min(pos + search_range, len(data))
    
    entries = []
    entry_num = 0
    search_pos = pos
    max_entries = 250
    
    while entry_num < max_entries:
        # Chercher "StoryID\x00"
        story_id_pos = data.find(b"StoryID\x00", search_pos, end_pos)
        if story_id_pos == -1:
            break
        
        search_pos = story_id_pos + len(b"StoryID\x00")
        entry_num += 1
        
        try:
            # Parser StoryID (IntProperty)
            story_id, story_id_addr = parse_int_property(data, story_id_pos)
            if story_id is None:
                continue
            
            # Chercher CurrentTaskID
            task_pos = data.find(b"CurrentTaskID\x00", story_id_pos, story_id_pos + 200)
            current_task = 0
            task_addr = None
            if task_pos != -1:
                current_task, task_addr = parse_int_property(data, task_pos)
            
            # Chercher State
            state_pos = data.find(b"State\x00", story_id_pos, story_id_pos + 300)
            state = -1
            state_addr = None
            if state_pos != -1:
                state, state_addr = parse_int_property(data, state_pos)
            
            # Chercher ConfirmedFlag
            conf_pos = data.find(b"ConfirmedFlag\x00", story_id_pos, story_id_pos + 400)
            confirmed = False
            conf_addr = None
            if conf_pos != -1:
                confirmed, conf_addr = parse_bool_property(data, conf_pos)
            
            entries.append({
                'entry': entry_num,
                'story_id': story_id,
                'story_id_addr': story_id_addr,
                'task_id': current_task if current_task else 0,
                'task_addr': task_addr,
                'state': state if state is not None else -1,
                'state_addr': state_addr,
                'confirmed': confirmed if confirmed is not None else False,
                'confirmed_addr': conf_addr
            })
            
        except Exception as e:
            continue
    
    return entries

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_mainstorydata_fixed.py <SaveData.sav>")
        return
    
    save_file = sys.argv[1]
    
    print("\n" + "=" * 80)
    print(f"ANALYSE MAINSTORYDATA AVEC STRUCTURE CORRECTE: {save_file}")
    print("=" * 80 + "\n")
    
    try:
        with open(save_file, 'rb') as f:
            data = f.read()
        
        print(f"[OK] Fichier charge: {len(data)} bytes\n")
        
        entries = scan_all_mainstorydata(data)
        
        print(f"\n✓ Total d'entrées trouvées: {len(entries)}\n")
        
        # Filtrer les entrées actives
        active = [e for e in entries if e['story_id'] != 0]
        print(f"✓ Entrées actives (StoryID != 0): {len(active)}\n")
        
        if active:
            print("=" * 80)
            print("ENTRÉES ACTIVES:")
            print("=" * 80)
            for e in active[:50]:  # Limiter l'affichage aux 50 premières
                state_label = {-1: "???", 0: "Non démarré", 1: "Actif", 2: "En cours", 5: "Complété"}.get(e['state'], f"State {e['state']}")
                state_addr_str = f"0x{e['state_addr']:08X}" if e['state_addr'] else "N/A"
                print(f"Entrée #{e['entry']:3d} | StoryID: {e['story_id']:4d} @ 0x{e['story_id_addr']:08X} | "
                      f"Task: {e['task_id']:4d} | State: {e['state']:2d} ({state_label}) @ {state_addr_str} | "
                      f"Confirmed: {e['confirmed']}")
            
            if len(active) > 50:
                print(f"\n... et {len(active) - 50} entrées supplémentaires")
        
        # Statistiques par State
        print("\n" + "=" * 80)
        print("STATISTIQUES PAR STATE:")
        print("=" * 80)
        states = {}
        for e in active:
            s = e['state']
            if s not in states:
                states[s] = 0
            states[s] += 1
        
        for state in sorted(states.keys()):
            state_label = {-1: "???", 0: "Non démarré", 1: "Actif", 2: "En cours", 5: "Complété"}.get(state, f"State {state}")
            print(f"  State {state:2d} ({state_label:15s}): {states[state]:3d} entrées")
        
    except FileNotFoundError:
        print(f"[ERREUR] Fichier non trouve: {save_file}")
    except Exception as e:
        print(f"[ERREUR] Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
