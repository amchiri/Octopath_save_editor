#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script qui trouve et affiche TOUTES les donnees d'histoire
"""

import struct

def main():
    save_file = "SaveData/SaveData0.sav"

    print("=" * 80)
    print("ANALYSE COMPLETE DE MAINSTORYDATA")
    print("=" * 80)

    with open(save_file, 'rb') as f:
        data = f.read()

    print(f"\nFichier: {save_file} ({len(data)} bytes)")

    # PARTIE 1: Endroll_ClearedMS (chapitres completes)
    print("\n" + "=" * 80)
    print("1. ENDROLL_CLEAREDMS - CHAPITRES COMPLETES")
    print("=" * 80)

    endroll_pos = data.find(b'Endroll_ClearedMS')
    if endroll_pos == -1:
        print("NON TROUVE!")
    else:
        print(f"\nPosition: 0x{endroll_pos:08X}")

        # Afficher le dump hex autour pour comprendre la structure
        start = endroll_pos
        end = endroll_pos + 150

        print("\nStructure hex:")
        for i in range(start, end, 16):
            hex_bytes = data[i:i+16]
            hex_str = ' '.join(f'{b:02X}' for b in hex_bytes)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in hex_bytes)
            print(f"  0x{i:08X}: {hex_str:<48} | {ascii_str}")

        # Trouver ArrayProperty
        array_pos = data.find(b'ArrayProperty', endroll_pos)
        print(f"\nArrayProperty a: 0x{array_pos:08X}")

        # Chercher "IntProperty" apres ArrayProperty
        intprop_pos = data.find(b'IntProperty', array_pos)
        print(f"IntProperty (type des elements) a: 0x{intprop_pos:08X}")

        # Le count est juste apres IntProperty\x00 + padding
        count_pos = intprop_pos + len(b'IntProperty\x00') + 1
        count = struct.unpack_from('<I', data, count_pos)[0]

        print(f"\nNombre d'elements: {count}")

        # Les donnees commencent juste apres
        data_pos = count_pos + 4

        print(f"\nCHAPITRES COMPLETES:")
        print("-" * 80)

        chapter_ids = []
        for i in range(min(count, 50)):
            chapter_id = struct.unpack_from('<i', data, data_pos)[0]
            if chapter_id > 0 and chapter_id < 100:
                chapter_ids.append(chapter_id)
                print(f"  [{i:2d}] ID = {chapter_id:2d} (0x{chapter_id:02X}) @ 0x{data_pos:08X}")
            data_pos += 4

        print("-" * 80)
        print(f"\nRESUME: {len(chapter_ids)} chapitres valides")
        print(f"IDs: {chapter_ids}")

if __name__ == "__main__":
    main()
