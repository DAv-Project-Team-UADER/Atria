"""Copy — Menú BIM → Modify → Copy.

Copia los objetos seleccionados a una nueva ubicación (Move en modo copia).
Comando FreeCAD: BIM_Copy (atajo C, P).
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Copy"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def copy(vector=None):
    """Copia la selección actual desplazándola según un vector.

    Parámetros
    ----------
    vector : FreeCAD.Vector | tuple, opcional
        Desplazamiento (X, Y, Z) en mm desde el original hasta la copia.
        Si se omite, se abre la herramienta interactiva para marcar punto
        base y punto destino en la vista 3D.

    Devuelve
    --------
    Las copias creadas, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if vector is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para copiar.")

    import Draft

    doc.openTransaction("Copy")
    try:
        result = Draft.move(selection, FreeCAD.Vector(vector), copy=True)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
