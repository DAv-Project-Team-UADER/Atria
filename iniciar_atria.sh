#!/usr/bin/env bash
# ATRIA - FreeCAD Launcher (Linux)
# Compatible con cualquier distribucion Linux y formato de FreeCAD (nativo, AppImage, Flatpak, Snap)

set -euo pipefail

echo "==================================================="
echo "          ATRIA - FreeCAD Voice Assistant          "
echo "==================================================="
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Asegurar enlaces del Workbench y libreria PortAudio local
"$REPO_ROOT/install_atria_mod.sh" >/dev/null

# 2. Configurar variables de entorno
export ATRIA_MOD_ROOT="$REPO_ROOT"
export ATRIA_GUI_FREECAD_ROOT="$REPO_ROOT/GUIFreeCad"
export ATRIA_INTERFAZ_ROOT="$REPO_ROOT/InterfazATRIA"
if [[ -d "$REPO_ROOT/InterfazATRIA/Icons" ]]; then
    export ATRIA_ICONS_ROOT="$REPO_ROOT/InterfazATRIA/Icons"
else
    export ATRIA_ICONS_ROOT="$REPO_ROOT/GUIFreeCad/ui/Icons"
fi
export ATRIA_DICTIONARY_ROOT="$REPO_ROOT/dictionary"
export ATRIA_MODELS_DIR="$REPO_ROOT/models"
export ATRIA_AUTOLOAD_WORKBENCH="1"
export ATRIA_AUTO_START_VOICE="1"
export ATRIA_AUTO_PANEL="1"

if [[ -f "$REPO_ROOT/.libs/libportaudio.so.2" ]]; then
    export ATRIA_PORTAUDIO_LIB="$REPO_ROOT/.libs/libportaudio.so.2"
    export LD_LIBRARY_PATH="$REPO_ROOT/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

# 3. Detectar ejecutable de FreeCAD
FREECAD_CMD=()

if [[ -n "${FREECAD_BIN:-}" && -x "${FREECAD_BIN}" ]]; then
    FREECAD_CMD=("$FREECAD_BIN")
else
    for bin_name in freecad FreeCAD freecad-daily freecad-weekly; do
        if command -v "$bin_name" >/dev/null 2>&1; then
            FREECAD_CMD=("$(command -v "$bin_name")")
            break
        fi
    done
fi

if [[ ${#FREECAD_CMD[@]} -eq 0 ]]; then
    if [[ -x "/snap/bin/freecad" ]]; then
        FREECAD_CMD=("/snap/bin/freecad")
    elif command -v flatpak >/dev/null 2>&1 && flatpak info org.freecad.FreeCAD >/dev/null 2>&1; then
        FREECAD_CMD=(
            "flatpak" "run"
            "--socket=pulseaudio"
            "--filesystem=$REPO_ROOT"
            "--env=ATRIA_MOD_ROOT=$ATRIA_MOD_ROOT"
            "--env=ATRIA_GUI_FREECAD_ROOT=$ATRIA_GUI_FREECAD_ROOT"
            "--env=ATRIA_INTERFAZ_ROOT=$ATRIA_INTERFAZ_ROOT"
            "--env=ATRIA_ICONS_ROOT=$ATRIA_ICONS_ROOT"
            "--env=ATRIA_DICTIONARY_ROOT=$ATRIA_DICTIONARY_ROOT"
            "--env=ATRIA_MODELS_DIR=$ATRIA_MODELS_DIR"
            "--env=ATRIA_AUTOLOAD_WORKBENCH=$ATRIA_AUTOLOAD_WORKBENCH"
            "--env=ATRIA_AUTO_START_VOICE=$ATRIA_AUTO_START_VOICE"
            "--env=ATRIA_AUTO_PANEL=$ATRIA_AUTO_PANEL"
            "--env=ATRIA_PORTAUDIO_LIB=${ATRIA_PORTAUDIO_LIB:-}"
            "org.freecad.FreeCAD"
        )
    elif command -v flatpak >/dev/null 2>&1 && flatpak info org.freecadweb.FreeCAD >/dev/null 2>&1; then
        FREECAD_CMD=(
            "flatpak" "run"
            "--socket=pulseaudio"
            "--filesystem=$REPO_ROOT"
            "--env=ATRIA_MOD_ROOT=$ATRIA_MOD_ROOT"
            "--env=ATRIA_GUI_FREECAD_ROOT=$ATRIA_GUI_FREECAD_ROOT"
            "--env=ATRIA_INTERFAZ_ROOT=$ATRIA_INTERFAZ_ROOT"
            "--env=ATRIA_ICONS_ROOT=$ATRIA_ICONS_ROOT"
            "--env=ATRIA_DICTIONARY_ROOT=$ATRIA_DICTIONARY_ROOT"
            "--env=ATRIA_MODELS_DIR=$ATRIA_MODELS_DIR"
            "--env=ATRIA_AUTOLOAD_WORKBENCH=$ATRIA_AUTOLOAD_WORKBENCH"
            "--env=ATRIA_AUTO_START_VOICE=$ATRIA_AUTO_START_VOICE"
            "--env=ATRIA_AUTO_PANEL=$ATRIA_AUTO_PANEL"
            "--env=ATRIA_PORTAUDIO_LIB=${ATRIA_PORTAUDIO_LIB:-}"
            "org.freecadweb.FreeCAD"
        )
    else
        # Buscar AppImage en rutas habituales del usuario
        for search_dir in "$REPO_ROOT" "$HOME/Applications" "$HOME/.local/bin" "$HOME/Descargas" "$HOME/Downloads" "$HOME" "/opt"; do
            if [[ -d "$search_dir" ]]; then
                while IFS= read -r -d '' appimage; do
                    if [[ -f "$appimage" && -x "$appimage" ]]; then
                        FREECAD_CMD=("$appimage")
                        break 2
                    fi
                done < <(find "$search_dir" -maxdepth 2 -iname "freecad*.AppImage" -print0 2>/dev/null || true)
            fi
        done
    fi
fi

if [[ ${#FREECAD_CMD[@]} -eq 0 ]]; then
    echo "[ERROR] No se encontro FreeCAD instalado en las rutas habituales." >&2
    echo "Por favor instala FreeCAD 1.0 o superior (paquete de tu distro, Flatpak, Snap o AppImage)" >&2
    echo "o indica la ruta manualmente: FREECAD_BIN=/ruta/a/FreeCAD ./iniciar_atria.sh" >&2
    exit 1
fi

echo "[OK] FreeCAD detectado: ${FREECAD_CMD[*]}"
echo ""
echo "Iniciando FreeCAD con el Workbench ATRIA..."
echo ""

exec "${FREECAD_CMD[@]}" "$@"
