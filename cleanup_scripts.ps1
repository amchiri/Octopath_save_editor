# Scripts à GARDER (utiles et corrects)
$keep = @(
    "fixed_editor.py",                    # Éditeur personnages (HP/SP/Level)
    "inventory_editor_dynamic.py",        # Éditeur inventaire
    "hp_bonus_editor_final.py",          # Éditeur bonus HP (noix)
    "show_all_mainstorydata.py",         # Affichage MainStoryData (NOUVEAU)
    "parse_mainstorydata_fixed.py",      # Parser MainStoryData (offset +21)
    "compare_saves_binary.py",           # Comparaison binaire
    "analyze_all_mainstorydata.py"       # Analyse complète (référence)
)

Write-Host "Scripts à GARDER:" -ForegroundColor Green
$keep | ForEach-Object { Write-Host "  - $_" -ForegroundColor Green }
Write-Host ""

# Lister tous les .py
$all = Get-ChildItem *.py | Select-Object -ExpandProperty Name

# Trouver ceux à supprimer
$to_delete = $all | Where-Object { $_ -notin $keep }

Write-Host "Scripts à SUPPRIMER: $($to_delete.Count)" -ForegroundColor Yellow
Write-Host ""

# Demander confirmation
$confirm = Read-Host "Voulez-vous supprimer ces $($to_delete.Count) fichiers? (oui/non)"

if ($confirm -eq "oui") {
    $count = 0
    foreach ($file in $to_delete) {
        Remove-Item $file -Force
        $count++
    }
    Write-Host ""
    Write-Host "✓ $count fichiers supprimés!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Fichiers restants:" -ForegroundColor Cyan
    Get-ChildItem *.py | Select-Object Name, Length | Format-Table -AutoSize
} else {
    Write-Host "Annulé." -ForegroundColor Red
}
