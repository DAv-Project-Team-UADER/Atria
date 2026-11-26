@echo off
setlocal
title Generador de Instalador ATRIA (.exe)

echo ==========================================================
echo        Generador del Instalador Oficial de ATRIA (.exe)
echo ==========================================================
echo.

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

:: Buscar Python de FreeCAD o del sistema
set "PYTHON_EXE="
if exist "C:\Program Files\FreeCAD 1.1\bin\python.exe" set "PYTHON_EXE=C:\Program Files\FreeCAD 1.1\bin\python.exe"
if not defined PYTHON_EXE if exist "C:\Program Files\FreeCAD 1.0\bin\python.exe" set "PYTHON_EXE=C:\Program Files\FreeCAD 1.0\bin\python.exe"
if not defined PYTHON_EXE (
    for %%X in (python.exe) do (set "PYTHON_EXE=%%~$PATH:X")
)

if not defined PYTHON_EXE (
    echo [ERROR] No se encontro Python en el sistema.
    echo Por favor instala FreeCAD o agrega Python al PATH.
    pause
    exit /b 1
)

echo Usando Python: "%PYTHON_EXE%"
echo Compilando instalador...
echo.

"%PYTHON_EXE%" "%REPO_ROOT%\installer\build_installer.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Ocurrio un fallo al compilar el instalador.
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo  Instalador generado con exito en la carpeta 'dist':
echo  -> dist\Instalador_ATRIA.exe
echo ==========================================================
echo.
pause
