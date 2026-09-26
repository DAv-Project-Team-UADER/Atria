"""Make Link — Menú BIM → Modify → Cloning Tools → Make Link.

Crea un App::Link por cada objeto seleccionado: una referencia liviana que
reutiliza la forma del original sin duplicar datos. Después entra en modo
Mover para reubicar los enlaces.
Comando FreeCAD: BIM_LinkMake (atajo L, K).
"""

import FreeCAD
import FreeCADGui

MOVE_COMMAND = "Draft_Move"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def make_link(start_move=True):
    """Crea un enlace (App::Link) a cada objeto seleccionado.

    Parámetros
    ----------
    start_move : bool
        Si es True (por defecto, igual que en BIM), deja seleccionados los
        enlaces creados y abre la herramienta Mover para reubicarlos.

    Devuelve
    --------
    Lista de enlaces creados.
    """
    doc = _require_document()

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para enlazar.")

    doc.openTransaction("Make Link")
    try:
        links = []
        for obj in selection:
            link = doc.addObject("App::Link", obj.Name + "_Link")
            link.LinkedObject = obj
            link.Label = obj.Label + "_Link"
            if hasattr(obj, "Placement"):
                link.Placement = obj.Placement
            links.append(link)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()

    if start_move:
        FreeCADGui.Selection.clearSelection()
        for link in links:
            FreeCADGui.Selection.addSelection(link)
        FreeCADGui.runCommand(MOVE_COMMAND)

    return links
