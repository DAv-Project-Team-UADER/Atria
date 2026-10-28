@echo off
setlocal enabledelayedexpansion

title ATRIA - FreeCAD Launcher

echo ===================================================
echo           ATRIA - FreeCAD Voice Assistant
echo ===================================================
echo.

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

:: 1. Detect FreeCAD executable
set "FREECAD_EXE="
if exist "C:\Program Files\FreeCAD 1.1\bin\freecad.exe" set "FREECAD_EXE=C:\Program Files\FreeCAD 1.1\bin\freecad.exe"
if not defined FREECAD_EXE if exist "C:\Program Files\FreeCAD 1.0\bin\freecad.exe" set "FREECAD_EXE=C:\Program Files\FreeCAD 1.0\bin\freecad.exe"
if not defined FREECAD_EXE if exist "C:\Program Files\FreeCAD 0.21\bin\freecad.exe" set "FREECAD_EXE=C:\Program Files\FreeCAD 0.21\bin\freecad.exe"
if not defined FREECAD_EXE if exist "C:\Program Files\FreeCAD\bin\freecad.exe" set "FREECAD_EXE=C:\Program Files\FreeCAD\bin\freecad.exe"
if not defined FREECAD_EXE if exist "%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\freecad.exe" set "FREECAD_EXE=%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\freecad.exe"
if not defined FREECAD_EXE if exist "%LOCALAPPDATA%\Programs\FreeCAD 1.0\bin\freecad.exe" set "FREECAD_EXE=%LOCALAPPDATA%\Programs\FreeCAD 1.0\bin\freecad.exe"

if not defined FREECAD_EXE (
    for %%X in (freecad.exe) do (set "FREECAD_EXE=%%~$PATH:X")
)

if not defined FREECAD_EXE (
    echo [ERROR] No se encontro FreeCAD instalado en las rutas habituales.
    echo Por favor asegurese de tener instalado FreeCAD 1.0 o superior.
    pause
    exit /b 1
)

echo [OK] FreeCAD detectado en: "%FREECAD_EXE%"

:: 2. Ensure Workbench link in FreeCAD Mod directory
for %%V in ("%APPDATA%\FreeCAD\Mod" "%APPDATA%\FreeCAD\v1-1\Mod" "%APPDATA%\FreeCAD\v1-0\Mod") do (
    set "MOD_DIR=%%~V"
    if not exist "!MOD_DIR!" mkdir "!MOD_DIR!" 2>nul
    if not exist "!MOD_DIR!\Atria" (
        mklink /J "!MOD_DIR!\Atria" "%REPO_ROOT%" >nul 2>nul
        if exist "!MOD_DIR!\Atria" (
            echo [OK] Enlace creado en !MOD_DIR!\Atria
        )
    )
)

:: 3. Configure Environment Variables
set "ATRIA_MOD_ROOT=%REPO_ROOT%"
set "ATRIA_GUI_FREECAD_ROOT=%REPO_ROOT%\GUIFreeCad"
set "ATRIA_INTERFAZ_ROOT=%REPO_ROOT%\InterfazATRIA"
if exist "%REPO_ROOT%\InterfazATRIA\Icons" (
    set "ATRIA_ICONS_ROOT=%REPO_ROOT%\InterfazATRIA\Icons"
) else (
    set "ATRIA_ICONS_ROOT=%REPO_ROOT%\GUIFreeCad\ui\Icons"
)
set "ATRIA_DICTIONARY_ROOT=%REPO_ROOT%\dictionary"
set "ATRIA_MODELS_DIR=%REPO_ROOT%\models"
set "ATRIA_AUTOLOAD_WORKBENCH=1"
set "ATRIA_AUTO_START_VOICE=1"
set "ATRIA_AUTO_PANEL=1"

echo.
echo Iniciando FreeCAD con el Workbench ATRIA...
echo.

start "" "%FREECAD_EXE%"
