#!/usr/bin/env bash
# =====================================================================
# ATRIA — Asistente de Voz para FreeCAD
# Script universal de instalación para Linux
# Universidad Autónoma de Entre Ríos (UADER FCyT)
# =====================================================================
set -euo pipefail

REPO_URL="https://github.com/DAv-Project-Team-UADER/Atria.git"
BRANCH="Codigo"
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DEFAULT_TARGET="$XDG_DATA_HOME/FreeCAD/v1-1/Mod/Atria"
TARGET_DIR="${1:-$DEFAULT_TARGET}"

echo ""
echo "================================================================="
echo "       ATRIA — Asistente de Voz para FreeCAD (Instalador Linux)  "
echo "       Universidad Autónoma de Entre Ríos • FCyT • UADER         "
echo "================================================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"

if [[ -f "$SCRIPT_DIR/iniciar_atria.sh" && -f "$SCRIPT_DIR/InitGui.py" ]]; then
    echo ">> Detectado repositorio local en: $SCRIPT_DIR"
    if [[ "$SCRIPT_DIR" != "$TARGET_DIR" ]]; then
        echo ">> Configurando en: $TARGET_DIR"
        mkdir -p "$TARGET_DIR"
        if [[ -f "$SCRIPT_DIR/install_atria_mod.sh" ]]; then
            (cd "$SCRIPT_DIR" && bash install_atria_mod.sh)
        fi
    fi
    INSTALL_DIR="$SCRIPT_DIR"
else
    echo ">> Descargando e instalando ATRIA en: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    
    if command -v git >/dev/null 2>&1; then
        echo ">> Clonando repositorio oficial (rama $BRANCH)..."
        if [[ -d "$TARGET_DIR/.git" ]]; then
            (cd "$TARGET_DIR" && git pull --rebase origin "$BRANCH")
        else
            git clone --depth 1 -b "$BRANCH" "$REPO_URL" "$TARGET_DIR"
        fi
    elif command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1; then
        TAR_URL="https://github.com/DAv-Project-Team-UADER/Atria/releases/latest/download/atria_linux.tar.gz"
        echo ">> Descargando archivo comprimido desde GitHub Releases..."
        TMP_TAR="$(mktemp /tmp/atria_linux_XXXXXX.tar.gz)"
        if command -v curl >/dev/null 2>&1; then
            curl -fSL "$TAR_URL" -o "$TMP_TAR" || curl -fSL "https://raw.githubusercontent.com/DAv-Project-Team-UADER/Atria/$BRANCH/dist/atria_linux.tar.gz" -o "$TMP_TAR"
        else
            wget -qO "$TMP_TAR" "$TAR_URL" || wget -qO "$TMP_TAR" "https://raw.githubusercontent.com/DAv-Project-Team-UADER/Atria/$BRANCH/dist/atria_linux.tar.gz"
        fi
        tar -xzf "$TMP_TAR" -C "$TARGET_DIR"
        rm -f "$TMP_TAR"
    else
        echo "[ERROR] Se requiere 'git', 'curl' o 'wget' para descargar ATRIA." >&2
        exit 1
    fi
    INSTALL_DIR="$TARGET_DIR"
fi

chmod +x "$INSTALL_DIR/iniciar_atria.sh" "$INSTALL_DIR/install_atria_mod.sh" 2>/dev/null || true

if [[ -f "$INSTALL_DIR/install_atria_mod.sh" ]]; then
    echo ">> Configurando integración con versiones de FreeCAD..."
    (cd "$INSTALL_DIR" && bash install_atria_mod.sh) || true
fi

ICON_SRC="$INSTALL_DIR/GUIFreeCad/Logos/atria_logo.png"
if [[ ! -f "$ICON_SRC" ]]; then
    ICON_SRC="$INSTALL_DIR/GUIFreeCad/ui/Icons/atria_logo.png"
fi

if [[ -f "$ICON_SRC" ]]; then
    mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps" "$HOME/.local/share/pixmaps"
    cp "$ICON_SRC" "$HOME/.local/share/icons/hicolor/256x256/apps/atria.png" 2>/dev/null || true
    cp "$ICON_SRC" "$HOME/.local/share/pixmaps/atria.png" 2>/dev/null || true
fi

DESKTOP_ENTRY_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_ENTRY_DIR"
cat << EOF > "$DESKTOP_ENTRY_DIR/atria.desktop"
[Desktop Entry]
Type=Application
Name=ATRIA (FreeCAD)
GenericName=Asistente de Voz para FreeCAD
Comment=Diseño paramétrico y modelado 3D por comandos de voz
Exec=$INSTALL_DIR/iniciar_atria.sh
Icon=atria
Terminal=false
Categories=Graphics;Engineering;3DGraphics;Science;
StartupNotify=true
EOF
chmod +x "$DESKTOP_ENTRY_DIR/atria.desktop"
echo "[OK] Acceso creado en el menú de aplicaciones: $DESKTOP_ENTRY_DIR/atria.desktop"

for dt_dir in "$HOME/Desktop" "$HOME/Escritorio"; do
    if [[ -d "$dt_dir" ]]; then
        cp "$DESKTOP_ENTRY_DIR/atria.desktop" "$dt_dir/"
        chmod +x "$dt_dir/atria.desktop" 2>/dev/null || true
        if command -v gio >/dev/null 2>&1; then
            gio set "$dt_dir/atria.desktop" metadata::trusted true 2>/dev/null || true
        fi
        echo "[OK] Acceso directo creado en el Escritorio: $dt_dir/atria.desktop"
    fi
done

echo ""
echo "================================================================="
echo " ¡Instalación de ATRIA completada con éxito!                     "
echo " Puedes abrir FreeCAD con ATRIA desde:                           "
echo "  1. El icono 'ATRIA (FreeCAD)' en tu Escritorio o Menú          "
echo "  2. O ejecutando: $INSTALL_DIR/iniciar_atria.sh                 "
echo "================================================================="
echo ""
