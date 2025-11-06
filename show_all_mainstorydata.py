import struct
import sys

def find_mainstorydata(data):
    pos = data.find(b"MainStoryData")
    return pos if pos != -1 else None

def parse_int_property(data, start_pos):
    int_prop = data.find(b"IntProperty\x00", start_pos, start_pos + 50)
    if int_prop == -1:
        return None, None
    value_pos = int_prop + 21
    value = struct.unpack_from('<i', data, value_pos)[0]
    return value, value_pos

def scan_all_entries(data, show_all=False):
    pos = find_mainstorydata(data)
    if not pos:
        print("MainStoryData non trouve!")
        return []
    
    print(f"MainStoryData trouve a: 0x{pos:08X}\n")
    
    entries = []
    search_pos = pos
    end_pos = min(pos + 60000, len(data))
    max_entries = 250
    
    while len(entries) < max_entries:
        story_id_pos = data.find(b"StoryID\x00", search_pos, end_pos)
        if story_id_pos == -1:
            break
        
        search_pos = story_id_pos + len(b"StoryID\x00")
        
        try:
            story_id, _ = parse_int_property(data, story_id_pos)
            if story_id is None:
                continue
            
            task_pos = data.find(b"CurrentTaskID\x00", story_id_pos, story_id_pos + 200)
            current_task = 0
            if task_pos != -1:
                current_task, _ = parse_int_property(data, task_pos)
            
            state_pos = data.find(b"State\x00", story_id_pos, story_id_pos + 300)
            state = 0
            if state_pos != -1:
                state, _ = parse_int_property(data, state_pos)
            
            conf_pos = data.find(b"ConfirmedFlag\x00", story_id_pos, story_id_pos + 400)
            confirmed = False
            if conf_pos != -1:
                bool_prop = data.find(b"BoolProperty\x00", conf_pos, conf_pos + 50)
                if bool_prop != -1:
                    confirmed = data[bool_prop + 25] != 0
            
            entries.append({
                'num': len(entries) + 1,
                'story_id': story_id,
                'task_id': current_task if current_task else 0,
                'state': state if state else 0,
                'confirmed': confirmed
            })
            
        except Exception as e:
            continue
    
    return entries

def main():
    if len(sys.argv) < 2:
        print("Usage: python show_all_mainstorydata.py <SaveData.sav> [--all]")
        print("  --all : Afficher TOUTES les entrees, meme vides (StoryID=0)")
        return
    
    save_file = sys.argv[1]
    show_all = "--all" in sys.argv
    
    with open(save_file, 'rb') as f:
        data = f.read()
    
    print(f"Analyse: {save_file} ({len(data)} bytes)")
    print("=" * 80)
    
    entries = scan_all_entries(data, show_all)
    
    # Filtrer ou non selon l'option
    if not show_all:
        entries = [e for e in entries if e['story_id'] != 0]
    
    print(f"\nTotal entrees scannees: {len(entries)}")
    
    if show_all:
        print("\nAFFICHAGE DE TOUTES LES ENTREES (y compris vides):")
    else:
        print("\nAFFICHAGE DES ENTREES ACTIVES (StoryID != 0):")
    
    print("=" * 80)
    print(f"{'#':>4} | {'StoryID':>7} | {'TaskID':>7} | {'State':>5} | Confirmed")
    print("-" * 80)
    
    for e in entries:
        state_label = {0: "Vide", 1: "Actif", 2: "Cours", 5: "Fin"}.get(e['state'], f"S{e['state']}")
        print(f"{e['num']:>4} | {e['story_id']:>7} | {e['task_id']:>7} | {e['state']:>5} | {str(e['confirmed']):<5}")
    
    print("-" * 80)
    
    # Stats par State
    state_counts = {}
    for e in entries:
        state = e['state']
        state_counts[state] = state_counts.get(state, 0) + 1
    
    print("\nSTATISTIQUES PAR STATE:")
    for state in sorted(state_counts.keys()):
        label = {0: "Vide/Non demarre", 1: "Actif", 2: "En cours", 5: "Complete"}.get(state, f"State {state}")
        print(f"  State {state:2d} ({label:20s}): {state_counts[state]:3d} entrees")

if __name__ == "__main__":
    main()
