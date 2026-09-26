"""Clone — Menú BIM → Modify → Cloning Tools → Clone.

Crea un clon (copia enlazada) de cada objeto seleccionado: si el original
cambia, el clon también se actualiza.
Comando FreeCAD: BIM_Clone (atajo C, L).
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Clone"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def clone(delta=None):
    """Clona la selección actual.

    Parámetros
    ----------
    delta : FreeCAD.Vector | tuple, opcional
        Desplazamiento de cada clon respecto de su original. Si se omite, se
        ejecuta la herramienta de BIM, que crea los clones y entra en modo
        Mover para ubicarlos con el mouse.

    Devuelve
    --------
    Lista de clones creados, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para clonar.")

    if delta is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    import Draft

    delta = FreeCAD.Vector(delta)
    doc.openTransaction("Clone")
    try:
        clones = [Draft.make_clone(obj, delta=delta) for obj in selection]
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return clones
