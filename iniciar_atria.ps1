# ATRIA - FreeCAD Launcher (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "          ATRIA - FreeCAD Voice Assistant          " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = $PSScriptRoot

# 1. Detect FreeCAD executable
$candidates = @(
    "C:\Program Files\FreeCAD 1.1\bin\freecad.exe",
    "C:\Program Files\FreeCAD 1.0\bin\freecad.exe",
    "C:\Program Files\FreeCAD 0.21\bin\freecad.exe",
    "C:\Program Files\FreeCAD\bin\freecad.exe",
    "$env:LOCALAPPDATA\Programs\FreeCAD 1.1\bin\freecad.exe",
    "$env:LOCALAPPDATA\Programs\FreeCAD 1.0\bin\freecad.exe"
)

$freecadExe = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $freecadExe) {
    $cmd = Get-Command "freecad.exe" -ErrorAction SilentlyContinue
    if ($cmd) {
        $freecadExe = $cmd.Source
    }
}

if (-not $freecadExe) {
    Write-Host "[ERROR] No se encontró FreeCAD instalado en las rutas habituales." -ForegroundColor Red
    Write-Host "Por favor instala FreeCAD 1.0 o superior." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] FreeCAD detectado en: $freecadExe" -ForegroundColor Green

# 2. Ensure Mod directory link
$modDirs = @(
    "$env:APPDATA\FreeCAD\Mod",
    "$env:APPDATA\FreeCAD\v1-1\Mod",
    "$env:APPDATA\FreeCAD\v1-0\Mod"
)

foreach ($modDir in $modDirs) {
    if (-not (Test-Path $modDir)) {
        New-Item -ItemType Directory -Path $modDir -Force | Out-Null
    }
    $targetLink = Join-Path $modDir "Atria"
    if (-not (Test-Path $targetLink)) {
        try {
            New-Item -ItemType Junction -Path $targetLink -Target $repoRoot | Out-Null
            Write-Host "[OK] Enlace creado en: $targetLink" -ForegroundColor Green
        } catch {
            Write-Host "[WARN] No se pudo crear junction en $($targetLink): $_" -ForegroundColor Yellow
        }
    }
}

# 3. Environment variables
$env:ATRIA_MOD_ROOT = $repoRoot
$env:ATRIA_GUI_FREECAD_ROOT = Join-Path $repoRoot "GUIFreeCad"
$env:ATRIA_DICTIONARY_ROOT = Join-Path $repoRoot "dictionary"
$env:ATRIA_AUTOLOAD_WORKBENCH = "1"

Write-Host ""
Write-Host "Iniciando FreeCAD con el Workbench ATRIA..." -ForegroundColor Cyan
Write-Host ""

Start-Process -FilePath $freecadExe
