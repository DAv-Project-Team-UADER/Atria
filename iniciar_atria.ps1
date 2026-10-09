# Lanzador directo de Atria para FreeCAD
$ErrorActionPreference = "Stop"

$AtriaRoot = $PSScriptRoot

# Configurar variables de entorno para que el Workbench las lea en InitGui.py
[Environment]::SetEnvironmentVariable("ATRIA_MOD_ROOT", $AtriaRoot, "Process")
[Environment]::SetEnvironmentVariable("ATRIA_AUTOLOAD_WORKBENCH", "1", "Process")

# Buscar FreeCAD dinámicamente en las rutas comunes de instalación
$rutasComunes = @(
    "$env:ProgramFiles\FreeCAD*\bin\FreeCAD.exe",
    "$env:LOCALAPPDATA\Programs\FreeCAD*\bin\FreeCAD.exe"
)

# Obtiene la lista de ejecutables, los ordena por fecha y se queda con el más nuevo
$FreeCADExe = (Get-ChildItem -Path $rutasComunes -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -First 1).FullName

if (-not $FreeCADExe -or -not (Test-Path -LiteralPath $FreeCADExe)) {
    Write-Error "No se encontro FreeCAD.exe en las rutas estandar. Por favor, instala FreeCAD o especifica la ruta manualmente en iniciar_atria.ps1."
    pause
    exit 1
}

Write-Host "Iniciando FreeCAD con Atria cargado desde: $AtriaRoot"
Write-Host "Ejecutable de FreeCAD detectado: $FreeCADExe"

& $FreeCADExe @args
exit $LASTEXITCODE