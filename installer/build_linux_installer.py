import os
import tarfile
import hashlib
import time

SHELL_HEADER = """#!/usr/bin/env bash
# =====================================================================
# ATRIA - Asistente de Voz para FreeCAD
# Instalador autoextraible para distribuciones Linux
# Universidad Autónoma de Entre Ríos (UADER FCyT)
# =====================================================================

set -e

echo ""
echo "================================================================="
echo "       ATRIA — Asistente de Voz para FreeCAD (Instalador Linux)  "
echo "       Universidad Autónoma de Entre Ríos • FCyT • UADER         "
echo "================================================================="
echo ""

XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DEFAULT_TARGET="$XDG_DATA_HOME/FreeCAD/v1-1/Mod/Atria"
TARGET_DIR="${1:-$DEFAULT_TARGET}"

echo ">> Instalando ATRIA en: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Extraer el archivo embebido a partir del marcador
ARCHIVE_LINE=$(grep -a -n '^__PAYLOAD_BELOW__$' "$0" | head -n 1 | cut -d: -f1)
if [[ -z "$ARCHIVE_LINE" ]]; then
    echo "[ERROR] No se encontro el paquete embebido en el instalador." >&2
    exit 1
fi

echo ">> Extrayendo componentes de ATRIA..."
tail -n +$((ARCHIVE_LINE + 1)) "$0" | tar -xz -C "$TARGET_DIR"

echo "[OK] Archivos de ATRIA extraidos correctamente."

# Permisos de ejecucion
chmod +x "$TARGET_DIR/iniciar_atria.sh" "$TARGET_DIR/install_atria_mod.sh" 2>/dev/null || true

# Ejecutar enlaces a otros directorios de FreeCAD (0.20, 1.0, Flatpak, Snap)
if [[ -f "$TARGET_DIR/install_atria_mod.sh" ]]; then
    echo ">> Configurando integracion con versiones de FreeCAD..."
    (cd "$TARGET_DIR" && bash install_atria_mod.sh) || true
fi

# Instalar iconos del sistema
ICON_SRC="$TARGET_DIR/GUIFreeCad/Logos/atria_logo.png"
if [[ ! -f "$ICON_SRC" ]]; then
    ICON_SRC="$TARGET_DIR/GUIFreeCad/ui/Icons/atria_logo.png"
fi

if [[ -f "$ICON_SRC" ]]; then
    mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps" "$HOME/.local/share/pixmaps"
    cp "$ICON_SRC" "$HOME/.local/share/icons/hicolor/256x256/apps/atria.png" 2>/dev/null || true
    cp "$ICON_SRC" "$HOME/.local/share/pixmaps/atria.png" 2>/dev/null || true
fi

# Crear acceso directo en el Menu de Aplicaciones (.desktop)
DESKTOP_ENTRY_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_ENTRY_DIR"
cat << 'EOF' > "$DESKTOP_ENTRY_DIR/atria.desktop"
[Desktop Entry]
Type=Application
Name=ATRIA (FreeCAD)
GenericName=Asistente de Voz para FreeCAD
Comment=Diseño paramétrico y modelado 3D por comandos de voz
Exec=TARGET_DIR_PLACEHOLDER/iniciar_atria.sh
Icon=atria
Terminal=false
Categories=Graphics;Engineering;3DGraphics;Science;
StartupNotify=true
EOF

sed -i "s|TARGET_DIR_PLACEHOLDER|$TARGET_DIR|g" "$DESKTOP_ENTRY_DIR/atria.desktop"
chmod +x "$DESKTOP_ENTRY_DIR/atria.desktop"
echo "[OK] Acceso creado en el menu de aplicaciones: $DESKTOP_ENTRY_DIR/atria.desktop"

# Crear acceso directo en el Escritorio si existe la carpeta Desktop o Escritorio
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
echo " ¡Instalacion de ATRIA completada con exito!                     "
echo " Puedes abrir FreeCAD con ATRIA desde:                           "
echo "  1. El icono 'ATRIA (FreeCAD)' en tu Escritorio o Menu          "
echo "  2. O ejecutando: $TARGET_DIR/iniciar_atria.sh                  "
echo "================================================================="
echo ""

exit 0
__PAYLOAD_BELOW__
"""

def should_exclude(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p.startswith(".") and p not in [".libs"]:
            return True
        if p in ["scratch", "dist", "ticket", "tickets", "3D-BIM+Annotation", "__pycache__", ".venv", "venv", "vosk-model-small-pt-0.3"]:
            return True
    if "vosk-model-small-es-0.42" in parts and "vosk-model-small-en-us-0.15" in parts:
        return True
    if rel_path.endswith((".pyc", ".pyo", ".log", ".FCBak", ".FCStd1", ".FCStd.bak")):
        return True
    if "models" in parts and rel_path.endswith(".zip"):
        return True
    return False

def build_linux_installer(repo_root, dist_dir, scratch_dir):
    print("[ATRIA-LINUX] Creando archivo tar.gz de ATRIA para Linux...")
    start = time.time()
    tar_path = os.path.join(scratch_dir, "atria_linux_payload.tar.gz")
    
    count = 0
    with tarfile.open(tar_path, "w:gz") as tar:
        for root, dirs, files in os.walk(repo_root):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, repo_root)
                if not should_exclude(rel):
                    # Guardar con rutas relativas limpias (POSIX)
                    tar.add(full, arcname=rel.replace("\\", "/"))
                    count += 1

    tar_size_mb = os.path.getsize(tar_path) / (1024 * 1024)
    print(f"[ATRIA-LINUX] Comprimidos {count} archivos en tar.gz ({tar_size_mb:.2f} MB)")

    # Copiar tar.gz también a dist como paquete independiente
    dist_tar = os.path.join(dist_dir, "atria_linux.tar.gz")
    with open(tar_path, "rb") as f_src, open(dist_tar, "wb") as f_dst:
        f_dst.write(f_src.read())

    # Construir instalador autoextraible .sh
    sh_installer = os.path.join(dist_dir, "Instalador_ATRIA_Linux.sh")
    with open(sh_installer, "wb") as out_f:
        out_f.write(SHELL_HEADER.encode("utf-8"))
        with open(tar_path, "rb") as in_tar:
            out_f.write(in_tar.read())

    sh_size_mb = os.path.getsize(sh_installer) / (1024 * 1024)
    elapsed = time.time() - start
    print(f"[ATRIA-LINUX] Instalador autoextraible listo: {sh_installer} ({sh_size_mb:.2f} MB, {elapsed:.2f}s)")
    return sh_installer, dist_tar
