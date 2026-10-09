# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad AutÃ³noma de Entre RÃ­os (UADER FCYT, sede ConcepciÃ³n del Uruguay)
# Bajo la direcciÃ³n de Ernesto Ledesma
# Encargados: Micaela SaÃ¼l, Tadeo Rochas y Camila ViÃ±eg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los tÃ©rminos de la Licencia PÃºblica General GNU tal como fue publicada
# por la FundaciÃ³n para el Software Libre, en la versiÃ³n 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea Ãºtil,
# pero SIN NINGUNA GARANTÃA; incluso sin la garantÃ­a implÃ­cita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÃ“SITO PARTICULAR. Consulte la
# Licencia PÃºblica General GNU para mÃ¡s detalles.
#
# DeberÃ­as haber recibido una copia de la Licencia PÃºblica General GNU
# junto con este programa. Si no es asÃ­, consulte <http://www.gnu.org/licenses/>.

"""
Prueba guiada para Alex â€” se ejecuta desde consola FreeCAD sin configurar rutas.

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
        print("[ATRIA] Error: no hay documento activo. CreÃ¡ uno nuevo (Archivo > Nuevo).")
        return None

    if preferred:
        if doc.getObject(preferred):
            return preferred
        print(f"[ATRIA] No existe '{preferred}'. Buscando Sketch automÃ¡ticamente...")

    for obj in doc.Objects:
        type_id = getattr(obj, "TypeId", "")
        if "Sketcher" in type_id or obj.Name.lower().startswith("sketch"):
            print(f"[ATRIA] Sketch detectado: '{obj.Name}'")
            return obj.Name

    if doc.Objects:
        fallback = doc.Objects[0].Name
        print(f"[ATRIA] No hay Sketch; uso el primer objeto: '{fallback}'")
        return fallback

    print("[ATRIA] Documento vacÃ­o. CreÃ¡ un Sketch con al menos 5 herramientas Sketcher.")
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

    print("\n========== ATRIA selection â€” prueba automÃ¡tica ==========\n")

    for language in ("es", "en", "pt"):
        print(f"--- CreateObjects idioma={language} ---")
        RunCreateObjects(target, Is3D=False, Language=language)
        PrintObjectTree()

    print("--- ObjectSelection (primer objeto) ---")
    selector = RunSelectionDemo()
    if selector is not None:
        print("Para ciclar objetos:")
        print("  selector.SelectOther = True")
        print("(repetÃ­ esa lÃ­nea para avanzar)\n")

    return selector
