# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT)
# Script de construcción del instalador autónomo de ATRIA (Instalador_ATRIA.exe)

import os
import sys
import zipfile
import subprocess
import hashlib
import shutil
import time

sys.path.insert(0, os.path.dirname(__file__))
from build_linux_installer import build_linux_installer

def log(msg):
    print(f"[ATRIA-BUILD] {msg}")

def find_csc():
    candidates = [
        r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
        r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return shutil.which("csc.exe")

def create_payload_zip(repo_root, zip_dest):
    log(f"Comprimiendo componentes de ATRIA en: {zip_dest}")
    start = time.time()

    exclude_dirs = {
        ".git", ".vscode", "__pycache__", "scratch", "installer", "dist",
        "vosk-model-small-pt-0.3"
    }

    count = 0
    with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            rel_root = os.path.relpath(root, repo_root)

            # Evitar duplicado anidado de es dentro de en-us
            if "vosk-model-small-es-0.42" in rel_root and "vosk-model-small-en-us-0.15" in rel_root:
                continue

            for f in files:
                if f.endswith((".pyc", ".pyo", ".gitkeep")):
                    continue
                fp = os.path.join(root, f)
                arcname = os.path.relpath(fp, repo_root)
                zf.write(fp, arcname)
                count += 1

    size_mb = os.path.getsize(zip_dest) / (1024 * 1024)
    elapsed = time.time() - start
    log(f"Comprimidos {count} archivos en {elapsed:.2f}s (Tamaño ZIP: {size_mb:.2f} MB)")
    return count, size_mb

def compile_installer(csc_exe, cs_file, zip_file, ico_file, logo_file, output_exe):
    log(f"Compilando ejecutable de instalación: {output_exe}")
    start = time.time()

    cmd = [
        csc_exe,
        "/nologo",
        "/target:winexe",
        "/platform:anycpu",
        "/optimize+",
        f"/win32icon:{ico_file}",
        "/r:System.dll",
        "/r:System.Drawing.dll",
        "/r:System.Windows.Forms.dll",
        "/r:System.IO.Compression.dll",
        "/r:System.IO.Compression.FileSystem.dll",
        f"/resource:{zip_file},Payload",
        f"/resource:{ico_file},Icon",
    ]
    if logo_file and os.path.exists(logo_file):
        cmd.append(f"/resource:{logo_file},Logo")

    cmd.append(f"/out:{output_exe}")
    cmd.append(cs_file)

    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        log("ERROR al compilar con csc:")
        print(res.stdout.decode("latin1", errors="replace"))
        print(res.stderr.decode("latin1", errors="replace"))
        sys.exit(1)

    elapsed = time.time() - start
    size_mb = os.path.getsize(output_exe) / (1024 * 1024)
    log(f"Compilación exitosa en {elapsed:.2f}s (Tamaño EXE: {size_mb:.2f} MB)")

def generate_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    digest = h.hexdigest()
    sha_file = file_path + ".sha256"
    with open(sha_file, "w", encoding="utf-8") as f:
        f.write(f"{digest} *{os.path.basename(file_path)}\n")
    log(f"SHA-256 ({os.path.basename(file_path)}): {digest}")
    return digest

def generate_release_notes(dist_dir, win_exe, win_size, win_hash, linux_sh, linux_sh_size, linux_sh_hash, linux_tar, linux_tar_size, linux_tar_hash):
    notes_path = os.path.join(dist_dir, "RELEASE_NOTES.md")
    content = f"""# ATRIA — Asistente de Voz para FreeCAD
**Universidad Autónoma de Entre Ríos (UADER FCYT)**

## Novedades del Release
- **Instalador ejecutable multiplataforma (Windows y Linux)**:
  - Detección automática de instalaciones de FreeCAD (1.1, 1.0, 0.21, Flatpak, Snap, AppImage).
  - Descompresión automática e instalación en el directorio de Workbenchs (`Mod/Atria`).
  - Creación de accesos directos en el Escritorio y Menú de Aplicaciones / Menú Inicio con el logo oficial.
  - Modelos de reconocimiento de voz sin conexión incluidos (Español e Inglés).
- **Modelado 3D paramétrico por voz con coordenadas (X, Y, Z)**:
  - Creación y posicionamiento preciso de paredes, vigas, columnas, losas, cajas, techos, puertas, ventanas, caños/tubos y escaleras.
- **Categoría de Selección y Edición de Objetos (`Select`)**:
  - Comandos de voz: `avanzar`, `retroceder`, `seleccionar`, `deseleccionar`, `seleccionar todos`, `deseleccionar todos`.
  - Edición visual interactiva: `editar` (modo edición Draft/FreeCAD).
  - Eliminación de objetos: `borrar` / `eliminar`.
- **Cámara y Vistas 3D**:
  - Vistas ortogonales, isométrica, dimétrica, trimétrica, centrado de vista y rotación por voz.
- **Soporte Bilingüe**:
  - Español e Inglés completo tanto en voz como en interfaz gráfica.

## Archivos de Descarga
| Plataforma | Tipo de Paquete | Archivo | Tamaño | SHA-256 |
| :--- | :--- | :--- | :--- | :--- |
| **Windows** | Instalador ejecutable (.exe) | **`{win_exe}`** | ~{win_size:.1f} MB | `{win_hash}` |
| **Linux** | Instalador autoextraíble (.sh) | **`{linux_sh}`** | ~{linux_sh_size:.1f} MB | `{linux_sh_hash}` |
| **Linux** | Tarball comprimido (.tar.gz) | **`{linux_tar}`** | ~{linux_tar_size:.1f} MB | `{linux_tar_hash}` |

---

### Instrucciones de Instalación en Windows:
1. Descarga **`{win_exe}`**.
2. Haz doble clic sobre el archivo descargado.
3. Presiona **Instalar ATRIA**.
4. ¡Listo! Abre FreeCAD desde el acceso directo del Escritorio o seleccionando el Workbench ATRIA.

---

### Instrucciones de Instalación en Linux:

#### Opción 1: Instalador autoextraíble descargable (Recomendado)
1. Descarga el archivo **`{linux_sh}`**.
2. Dale permisos de ejecución y ejecútalo en una terminal:
   ```bash
   chmod +x {linux_sh}
   ./{linux_sh}
   ```
3. ¡Listo! Se creará el acceso directo `ATRIA (FreeCAD)` en tu Escritorio y en tu Menú de Aplicaciones.

#### Opción 2: Instalación directa por comando (un solo paso)
Abre tu terminal y ejecuta:
```bash
curl -fsSL https://raw.githubusercontent.com/DAv-Project-Team-UADER/Atria/Codigo/install.sh | bash
```
"""
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"Notas de release generadas en: {notes_path}")

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(repo_root, "dist")
    scratch_dir = os.path.join(repo_root, "scratch")
    installer_dir = os.path.join(repo_root, "installer")

    os.makedirs(dist_dir, exist_ok=True)
    os.makedirs(scratch_dir, exist_ok=True)

    csc_exe = find_csc()
    if not csc_exe:
        log("ERROR: No se encontró csc.exe (.NET Framework C# Compiler).")
        sys.exit(1)
    log(f"Compilador C# encontrado: {csc_exe}")

    ico_file = os.path.join(installer_dir, "atria.ico")
    badge_file = os.path.join(installer_dir, "atria_badge.png")

    # Asegurar generación de iconos con create_icon.py
    ico_script = os.path.join(installer_dir, "create_icon.py")
    if os.path.exists(ico_script):
        log("Actualizando recursos de icono y logo...")
        subprocess.run([sys.executable, ico_script], cwd=installer_dir)

    cs_file = os.path.join(installer_dir, "InstallerSource.cs")
    if not os.path.exists(cs_file):
        log(f"ERROR: No se encontró {cs_file}")
        sys.exit(1)

    # 1. Compilar Iniciar_ATRIA.exe primero para que quede dentro del payload ZIP
    launcher_cs = os.path.join(installer_dir, "LauncherSource.cs")
    launcher_exe = os.path.join(repo_root, "Iniciar_ATRIA.exe")
    if os.path.exists(launcher_cs):
        log("Compilando lanzador nativo Iniciar_ATRIA.exe...")
        subprocess.run([
            csc_exe,
            "/nologo",
            "/target:winexe",
            "/platform:anycpu",
            "/optimize+",
            f"/win32icon:{ico_file}",
            f"/out:{launcher_exe}",
            launcher_cs
        ], check=True)
        log(f"Lanzador nativo listo: {launcher_exe} ({os.path.getsize(launcher_exe)} bytes)")

    zip_file = os.path.join(scratch_dir, "atria_payload.zip")
    create_payload_zip(repo_root, zip_file)

    exe_name = "Instalador_ATRIA.exe"
    output_exe = os.path.join(dist_dir, exe_name)
    compile_installer(csc_exe, cs_file, zip_file, ico_file, badge_file, output_exe)

    win_hash = generate_sha256(output_exe)
    win_size = os.path.getsize(output_exe) / (1024 * 1024)

    # 3. Compilar instalador y paquete de Linux
    log("Construyendo instalador autoextraíble y paquete para Linux...")
    sh_installer, dist_tar = build_linux_installer(repo_root, dist_dir, scratch_dir)
    linux_sh_hash = generate_sha256(sh_installer)
    linux_sh_size = os.path.getsize(sh_installer) / (1024 * 1024)
    linux_tar_hash = generate_sha256(dist_tar)
    linux_tar_size = os.path.getsize(dist_tar) / (1024 * 1024)

    generate_release_notes(
        dist_dir,
        exe_name,
        win_size,
        win_hash,
        os.path.basename(sh_installer),
        linux_sh_size,
        linux_sh_hash,
        os.path.basename(dist_tar),
        linux_tar_size,
        linux_tar_hash
    )

    log("=" * 60)
    log(f"¡PROCESO COMPLETADO EXITOSAMENTE!")
    log(f"Paquetes listos para publicar como Release en GitHub:")
    log(f"  [Windows] -> {output_exe} ({win_size:.2f} MB)")
    log(f"  [Linux]   -> {sh_installer} ({linux_sh_size:.2f} MB)")
    log(f"  [Linux]   -> {dist_tar} ({linux_tar_size:.2f} MB)")
    log("=" * 60)

if __name__ == "__main__":
    main()
