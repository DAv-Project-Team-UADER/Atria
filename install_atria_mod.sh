#!/usr/bin/env bash
# Instala Atria en la carpeta Mod de FreeCAD (usuario en Linux) creando enlaces simbolicos.
# Compatible con cualquier distribucion Linux y cualquier version de FreeCAD:
#   - Clásica (0.18 / 0.19): ~/.FreeCAD/Mod
#   - Estándar XDG (0.20 / 0.21 / 1.0): ~/.local/share/FreeCAD/Mod
#   - Moderna versionada (1.0 / 1.1+): ~/.local/share/FreeCAD/v1-0/Mod, v1-1/Mod, v*/Mod
#   - Empaquetados Flatpak (org.freecad.FreeCAD / org.freecadweb.FreeCAD) y Snap

set -euo pipefail

# Obtener la carpeta de origen (raiz del repositorio)
SOURCE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DEFAULT_FREECAD_DIR="$XDG_DATA_HOME/FreeCAD"

declare -a BASE_DIRS=("$DEFAULT_FREECAD_DIR")

# Legacy FreeCAD (< 0.20) si existe
if [[ -d "$HOME/.FreeCAD" ]]; then
    BASE_DIRS+=("$HOME/.FreeCAD")
fi

# Detectar instalaciones Flatpak (aunque no se hayan abierto por primera vez)
for fp_id in "org.freecad.FreeCAD" "org.freecadweb.FreeCAD"; do
    fp_dir="$HOME/.var/app/$fp_id/data/FreeCAD"
    if [[ -d "$HOME/.var/app/$fp_id" ]] || (command -v flatpak >/dev/null 2>&1 && flatpak info "$fp_id" >/dev/null 2>&1); then
        BASE_DIRS+=("$fp_dir")
        # Dar permiso al sandbox de Flatpak para leer la carpeta del repositorio Atria y usar audio/microfono (PulseAudio/PipeWire)
        if command -v flatpak >/dev/null 2>&1 && flatpak info "$fp_id" >/dev/null 2>&1; then
            flatpak override --user --socket=pulseaudio --filesystem="$SOURCE_PATH" "$fp_id" 2>/dev/null || true
        fi
    fi
done

# Detectar instalacion Snap
if [[ -d "$HOME/snap/freecad" ]] || [[ -x "/snap/bin/freecad" ]]; then
    if [[ -d "$HOME/snap/freecad/current" ]]; then
        BASE_DIRS+=("$HOME/snap/freecad/current/.local/share/FreeCAD")
    fi
fi

# Copiar libportaudio.so.2 del sistema a .libs/ para entornos aislados (Flatpak / AppImage)
stage_portaudio_lib() {
    local host_pa=""
    for search_dir in /usr/lib /usr/lib64 /lib /lib64 /usr/local/lib; do
        if [[ -d "$search_dir" ]]; then
            host_pa="$(find "$search_dir" -maxdepth 3 -name "libportaudio.so.2*" 2>/dev/null | head -n 1 || true)"
            if [[ -n "$host_pa" ]]; then
                break
            fi
        fi
    done

    if [[ -n "$host_pa" && -e "$host_pa" ]]; then
        mkdir -p "$SOURCE_PATH/.libs"
        cp -L "$host_pa" "$SOURCE_PATH/.libs/libportaudio.so.2"
        ln -sf "libportaudio.so.2" "$SOURCE_PATH/.libs/libportaudio.so"
        echo " [OK] PortAudio empaquetado para sandbox: $SOURCE_PATH/.libs/libportaudio.so.2"
    else
        echo " [WARN] No se encontro libportaudio.so.2 en el sistema host."
        echo "        Instala PortAudio con el gestor de paquetes de tu distro (ej. libportaudio2 / portaudio)."
    fi
}

link_mod_folder() {
    local dest_folder="$1"
    local dest_link="$dest_folder/Atria"

    if [[ ! -d "$dest_folder" ]]; then
        mkdir -p "$dest_folder"
        echo "Se creo el directorio de mods: $dest_folder"
    fi

    if [[ -e "$dest_link" || -L "$dest_link" ]]; then
        rm -rf "$dest_link"
        echo "Se actualizo la instalacion previa en: $dest_link"
    fi

    ln -s "$SOURCE_PATH" "$dest_link"
    echo " [OK] Enlace creado: $dest_link -> $SOURCE_PATH"
}

install_into_base_dir() {
    local freecad_user_dir="$1"

    # 1. Instalar siempre en Mod base (0.20, 0.21, 1.0) y en v1-0 / v1-1
    #    (para que funcione incluso si el usuario aun no abrio FreeCAD 1.x por primera vez)
    declare -a target_mod_dirs=(
        "$freecad_user_dir/Mod"
        "$freecad_user_dir/v1-0/Mod"
        "$freecad_user_dir/v1-1/Mod"
    )

    # 2. Si existen otros directorios de version (ej. v1-2, v2-0), incluirlos tambien
    if [[ -d "$freecad_user_dir" ]]; then
        for vdir in "$freecad_user_dir"/v*; do
            if [[ -d "$vdir" ]]; then
                local vmod="$vdir/Mod"
                local already=0
                for existing in "${target_mod_dirs[@]}"; do
                    if [[ "$existing" == "$vmod" ]]; then
                        already=1
                        break
                    fi
                done
                if [[ $already -eq 0 ]]; then
                    target_mod_dirs+=("$vmod")
                fi
            fi
        done
    fi

    for mod_dir in "${target_mod_dirs[@]}"; do
        link_mod_folder "$mod_dir"
    done
}

echo "-------------------------------------------"
echo " Instalando Atria para FreeCAD en Linux... "
echo "-------------------------------------------"

for base_dir in "${BASE_DIRS[@]}"; do
    install_into_base_dir "$base_dir"
done

stage_portaudio_lib

echo "-------------------------------------------"
echo " Atria instalado con exito! "
echo "-------------------------------------------"
