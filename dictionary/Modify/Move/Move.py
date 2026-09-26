"""Move — Menú BIM → Modify → Move.

Mueve los objetos seleccionados según un vector de desplazamiento.
Comando FreeCAD: Draft_Move (atajo M, V).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Move"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def move(vector=None, copy=False):
    """Mueve la selección actual.

    Parámetros
    ----------
    vector : FreeCAD.Vector | tuple, opcional
        Desplazamiento (X, Y, Z) en mm. Si se omite, se abre la herramienta
        interactiva para marcar punto base y punto destino en la vista 3D.
    copy : bool
        Si es True, crea copias desplazadas en lugar de mover los originales.

    Devuelve
    --------
    Los objetos movidos (o las copias creadas), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if vector is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para mover.")

    import Draft

    doc.openTransaction("Move")
    try:
        result = Draft.move(selection, FreeCAD.Vector(vector), copy=copy)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
