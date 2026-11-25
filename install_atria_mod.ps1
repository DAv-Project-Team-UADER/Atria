# Instala Atria en la carpeta Mod de FreeCAD (usuario) creando un enlace simbolico.
# Soporta tanto versiones viejas (0.x) como nuevas (1.x y superior).

$ErrorActionPreference = "Stop"

# Obtener la carpeta de origen
$SourcePath = $PSScriptRoot

# Obtener la carpeta de AppData
$AppdataPath = [Environment]::GetFolderPath("ApplicationData")
$FreeCadUserDir = Join-Path $AppdataPath "FreeCAD"

# Determinar si existe la estructura nueva (v1-1, v1-2, etc.) o si usamos la clasica
# Buscamos directorios que empiecen con 'v' dentro de AppData\Roaming\FreeCAD
$VersionDirs = Get-ChildItem -Path $FreeCadUserDir -Directory -Filter "v*" -ErrorAction SilentlyContinue

if ($VersionDirs.Count -gt 0) {
    # Si hay directorios de versión (ej. v1-1), agarramos el más reciente
    $LatestVersionDir = $VersionDirs | Sort-Object Name -Descending | Select-Object -First 1
    $DestFolder = Join-Path $LatestVersionDir.FullName "Mod"
    Write-Host "Detectada estructura moderna de FreeCAD en: $DestFolder"
} else {
    # Estructura clásica (0.21 y anteriores)
    $DestFolder = Join-Path $FreeCadUserDir "Mod"
    Write-Host "Detectada estructura clasica de FreeCAD en: $DestFolder"
}

$DestLink = Join-Path $DestFolder "Atria"

# Asegurar que la carpeta Mod exista
if (-not (Test-Path -LiteralPath $DestFolder)) {
    New-Item -ItemType Directory -Path $DestFolder -Force | Out-Null
    Write-Host "Se creo el directorio de mods: $DestFolder"
}

# Si ya existe una instalacion previa de Atria, removerla
if (Test-Path -LiteralPath $DestLink) {
    Remove-Item -Path $DestLink -Recurse -Force
    Write-Host "Se elimino la version anterior de Atria en: $DestLink"
}

# Crear el Junction (enlace simbolico)
New-Item -ItemType Junction -Path $DestLink -Target $SourcePath -Force | Out-Null

Write-Host "-------------------------------------------"
Write-Host " Atria instalado con exito! "
Write-Host " Enlace creado: $DestLink -> $SourcePath"
Write-Host "-------------------------------------------"