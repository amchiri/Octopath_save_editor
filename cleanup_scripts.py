import os
import glob

# Scripts à GARDER (utiles et corrects)
keep = [
    "fixed_editor.py",                    # Éditeur personnages (HP/SP/Level)
    "inventory_editor_dynamic.py",        # Éditeur inventaire
    "hp_bonus_editor_final.py",          # Éditeur bonus HP (noix)
    "show_all_mainstorydata.py",         # Affichage MainStoryData (NOUVEAU)
    "parse_mainstorydata_fixed.py",      # Parser MainStoryData (offset +21)
    "compare_saves_binary.py",           # Comparaison binaire
    "analyze_all_mainstorydata.py",      # Analyse complète (référence)
    "cleanup_scripts.py",                # Ce script de nettoyage
    "cleanup_scripts.ps1"                # Script PowerShell
]

print("=" * 80)
print("NETTOYAGE DES SCRIPTS")
print("=" * 80)
print("\nScripts à GARDER:")
for f in keep:
    if f.endswith('.py'):
        print(f"  [OK] {f}")

# Lister tous les .py
all_files = glob.glob("*.py")

# Trouver ceux à supprimer
to_delete = [f for f in all_files if f not in keep]

print(f"\nScripts à SUPPRIMER: {len(to_delete)}")
if len(to_delete) <= 20:
    for f in to_delete:
        print(f"  [-] {f}")
else:
    for f in to_delete[:10]:
        print(f"  [-] {f}")
    print(f"  ... et {len(to_delete) - 10} autres")

# Demander confirmation
print("\n" + "=" * 80)
confirm = input(f"Voulez-vous supprimer ces {len(to_delete)} fichiers? (oui/non): ")

if confirm.lower() == "oui":
    count = 0
    for file in to_delete:
        try:
            os.remove(file)
            count += 1
        except Exception as e:
            print(f"Erreur en supprimant {file}: {e}")
    
    print(f"\n[OK] {count} fichiers supprimés!")
    print("\nFichiers restants:")
    remaining = glob.glob("*.py")
    for f in sorted(remaining):
        size = os.path.getsize(f)
        print(f"  {f:<40} {size:>8} bytes")
else:
    print("\nAnnulé.")
