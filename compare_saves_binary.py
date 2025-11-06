import sys

def compare_saves(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"SaveData8: {len(data1)} bytes")
    print(f"SaveData9: {len(data2)} bytes")
    print(f"Différence de taille: {len(data1) - len(data2)} bytes\n")
    
    # Comparer les 100 premiers bytes différents
    diff_count = 0
    diff_regions = []
    current_region_start = None
    
    min_len = min(len(data1), len(data2))
    
    for i in range(min_len):
        if data1[i] != data2[i]:
            if current_region_start is None:
                current_region_start = i
            diff_count += 1
        else:
            if current_region_start is not None:
                diff_regions.append((current_region_start, i-1, i - current_region_start))
                current_region_start = None
                if len(diff_regions) >= 20:  # Limiter à 20 régions
                    break
    
    print(f"Total de {diff_count} bytes différents sur les {min_len} premiers bytes\n")
    print("=" * 80)
    print("PREMIÈRES RÉGIONS DE DIFFÉRENCES:")
    print("=" * 80)
    
    for idx, (start, end, size) in enumerate(diff_regions[:20], 1):
        print(f"\nRégion #{idx}: 0x{start:08X} - 0x{end:08X} ({size} bytes)")
        
        # Afficher quelques bytes avant/après pour contexte
        context_start = max(0, start - 20)
        context_end = min(len(data1), end + 20)
        
        print(f"\nSaveData8:")
        print_hex(data1, start, min(start + 50, end + 1))
        
        print(f"\nSaveData9:")
        print_hex(data2, start, min(start + 50, end + 1))

def print_hex(data, start, end):
    """Affiche des données en hex"""
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02X}' for b in data[i:min(i+16, end)])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:min(i+16, end)])
        print(f"  0x{i:08X}: {hex_str:<48} | {ascii_str}")

if __name__ == "__main__":
    compare_saves("SaveData/SaveData8.sav", "SaveData/SaveData9.sav")
