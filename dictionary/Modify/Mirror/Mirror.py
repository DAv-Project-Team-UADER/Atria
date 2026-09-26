"""Mirror — Menú BIM → Modify → Mirror.

Refleja los objetos seleccionados respecto de una línea definida por dos
puntos (sobre el plano de trabajo actual).
Comando FreeCAD: Draft_Mirror (atajo M, I).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Mirror"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def mirror(p1=None, p2=None):
    """Crea la imagen especular de la selección actual.

    Parámetros
    ----------
    p1, p2 : FreeCAD.Vector | tuple, opcionales
        Puntos que definen la línea de espejo. El plano de reflexión contiene
        esa línea y la normal del plano de trabajo. Si falta alguno, se abre
        la herramienta interactiva para marcarlos en la vista 3D.

    Devuelve
    --------
    Los objetos Part::Mirroring creados, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if p1 is None or p2 is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    p1 = FreeCAD.Vector(p1)
    p2 = FreeCAD.Vector(p2)
    if p1.isEqual(p2, 1e-7):
        raise ValueError("Los dos puntos de la línea de espejo deben ser distintos.")

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para espejar.")

    import Draft

    doc.openTransaction("Mirror")
    try:
        result = Draft.mirror(selection, p1, p2)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
