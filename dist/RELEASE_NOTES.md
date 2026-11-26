# ATRIA — Asistente de Voz para FreeCAD
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
| **Windows** | Instalador ejecutable (.exe) | **`Instalador_ATRIA.exe`** | ~80.1 MB | `57542bbd4fb9ad97a8974bd97aa3a769682e6989876e815c4e7914af43192655` |
| **Linux** | Instalador autoextraíble (.sh) | **`Instalador_ATRIA_Linux.sh`** | ~79.0 MB | `18e082e227068ad957cf92c90de34496a88b7fa5bf4d85a2f0b611738aefa5bc` |
| **Linux** | Tarball comprimido (.tar.gz) | **`atria_linux.tar.gz`** | ~78.9 MB | `dc1a08e2947c9d1baff8b2b0e69ed3ca178f9f1d4cd6f5ce4779e56b0a2f9619` |

---

### Instrucciones de Instalación en Windows:
1. Descarga **`Instalador_ATRIA.exe`**.
2. Haz doble clic sobre el archivo descargado.
3. Presiona **Instalar ATRIA**.
4. ¡Listo! Abre FreeCAD desde el acceso directo del Escritorio o seleccionando el Workbench ATRIA.

---

### Instrucciones de Instalación en Linux:

#### Opción 1: Instalador autoextraíble descargable (Recomendado)
1. Descarga el archivo **`Instalador_ATRIA_Linux.sh`**.
2. Dale permisos de ejecución y ejecútalo en una terminal:
   ```bash
   chmod +x Instalador_ATRIA_Linux.sh
   ./Instalador_ATRIA_Linux.sh
   ```
3. ¡Listo! Se creará el acceso directo `ATRIA (FreeCAD)` en tu Escritorio y en tu Menú de Aplicaciones.

#### Opción 2: Instalación directa por comando (un solo paso)
Abre tu terminal y ejecuta:
```bash
curl -fsSL https://raw.githubusercontent.com/DAv-Project-Team-UADER/Atria/Codigo/install.sh | bash
```
