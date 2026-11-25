# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""
Prueba guiada para Alex — se ejecuta desde consola FreeCAD sin configurar rutas.

    from scr.gui.atria_commands import RunAlexSelectionPrueba
    RunAlexSelectionPrueba()
"""

from __future__ import annotations

import sys
from pathlib import Path


def _EnsurePath() -> None:
    """Idempotent: selection/ must already be on sys.path via ATRIA bootstrap."""
    selection_dir = Path(__file__).resolve().parent
    text = str(selection_dir)
    if text not in sys.path:
        sys.path.insert(0, text)


def _FindSketchName(preferred: str | None) -> str | None:
    import FreeCAD as App

    doc = App.ActiveDocument
    if doc is None:
        print("[ATRIA] Error: no hay documento activo. Creá uno nuevo (Archivo > Nuevo).")
        return None

    if preferred:
        if doc.getObject(preferred):
            return preferred
        print(f"[ATRIA] No existe '{preferred}'. Buscando Sketch automáticamente...")

    for obj in doc.Objects:
        type_id = getattr(obj, "TypeId", "")
        if "Sketcher" in type_id or obj.Name.lower().startswith("sketch"):
            print(f"[ATRIA] Sketch detectado: '{obj.Name}'")
            return obj.Name

    if doc.Objects:
        fallback = doc.Objects[0].Name
        print(f"[ATRIA] No hay Sketch; uso el primer objeto: '{fallback}'")
        return fallback

    print("[ATRIA] Documento vacío. Creá un Sketch con al menos 5 herramientas Sketcher.")
    return None


def RunFullDemo(sketch_name: str | None = None):
    """CreateObjects (es/en/pt) + ObjectSelection demo. Returns selector."""
    _EnsurePath()
    import FreeCAD as App

    if App.ActiveDocument is None:
        App.newDocument("SelectionTest")
        print("[ATRIA] Documento creado: 'SelectionTest'")

    from console_helpers import PrintObjectTree, RunCreateObjects, RunSelectionDemo

    target = _FindSketchName(sketch_name)
    if target is None:
        return None

    print("\n========== ATRIA selection — prueba automática ==========\n")

    for language in ("es", "en", "pt"):
        print(f"--- CreateObjects idioma={language} ---")
        RunCreateObjects(target, Is3D=False, Language=language)
        PrintObjectTree()

    print("--- ObjectSelection (primer objeto) ---")
    selector = RunSelectionDemo()
    if selector is not None:
        print("Para ciclar objetos:")
        print("  selector.SelectOther = True")
        print("(repetí esa línea para avanzar)\n")

    return selector
