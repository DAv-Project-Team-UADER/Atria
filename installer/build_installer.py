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

def compile_installer(csc_exe, cs_file, zip_file, ico_file, output_exe):
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
        f"/out:{output_exe}",
        cs_file,
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        log("ERROR al compilar con csc:")
        print(res.stdout)
        print(res.stderr)
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

def generate_release_notes(dist_dir, exe_name, size_mb, sha256_hash):
    notes_path = os.path.join(dist_dir, "RELEASE_NOTES.md")
    content = f"""# ATRIA — Asistente de Voz para FreeCAD
**Universidad Autónoma de Entre Ríos (UADER FCYT)**

## Novedades del Release
- **Instalador ejecutable de un clic (`{exe_name}`)**:
  - Detección automática de instalaciones de FreeCAD (1.1, 1.0, 0.21).
  - Descompresión automática e instalación en el directorio de Workbenchs (`Mod\\Atria`).
  - Creación de accesos directos en el Escritorio y Menú Inicio.
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
| Archivo | Tamaño | SHA-256 |
| :--- | :--- | :--- |
| **`{exe_name}`** | ~{size_mb:.1f} MB | `{sha256_hash}` |

### Instrucciones de Instalación:
1. Descarga el archivo `{exe_name}`.
2. Ejecuta el archivo haciendo doble clic.
3. Presiona **Instalar ATRIA**.
4. ¡Listo! Puedes abrir FreeCAD desde el acceso directo del Escritorio o seleccionando el Workbench ATRIA en FreeCAD.
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
    if not os.path.exists(ico_file):
        log("Generando icono atria.ico...")
        ico_script = os.path.join(installer_dir, "create_icon.py")
        if os.path.exists(ico_script):
            subprocess.run(["python", ico_script], cwd=installer_dir)

    cs_file = os.path.join(installer_dir, "InstallerSource.cs")
    if not os.path.exists(cs_file):
        log(f"ERROR: No se encontró {cs_file}")
        sys.exit(1)

    zip_file = os.path.join(scratch_dir, "atria_payload.zip")
    create_payload_zip(repo_root, zip_file)

    exe_name = "Instalador_ATRIA.exe"
    output_exe = os.path.join(dist_dir, exe_name)
    compile_installer(csc_exe, cs_file, zip_file, ico_file, output_exe)

    sha256_hash = generate_sha256(output_exe)
    size_mb = os.path.getsize(output_exe) / (1024 * 1024)
    generate_release_notes(dist_dir, exe_name, size_mb, sha256_hash)

    log("=" * 60)
    log(f"¡PROCESO COMPLETADO EXITOSAMENTE!")
    log(f"Instalador listo para publicar como Release en GitHub:")
    log(f"  -> {output_exe}")
    log(f"  -> Tamaño: {size_mb:.2f} MB")
    log("=" * 60)

if __name__ == "__main__":
    main()
