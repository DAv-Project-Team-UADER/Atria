"""Rotate — Menú BIM → Modify → Rotate.

Rota los objetos seleccionados un ángulo alrededor de un centro y un eje.
Comando FreeCAD: Draft_Rotate (atajo R, O).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Rotate"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def rotate(angle=None, center=(0, 0, 0), axis=(0, 0, 1), copy=False):
    """Rota la selección actual.

    Parámetros
    ----------
    angle : float, opcional
        Ángulo en grados. Si se omite, se abre la herramienta interactiva
        para marcar centro y ángulo en la vista 3D.
    center : FreeCAD.Vector | tuple
        Centro de rotación. Por defecto el origen.
    axis : FreeCAD.Vector | tuple
        Eje de rotación. Por defecto Z.
    copy : bool
        Si es True, crea copias rotadas en lugar de rotar los originales.

    Devuelve
    --------
    Los objetos rotados (o las copias creadas), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if angle is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para rotar.")

    import Draft

    doc.openTransaction("Rotate")
    try:
        result = Draft.rotate(
            selection,
            float(angle),
            center=FreeCAD.Vector(center),
            axis=FreeCAD.Vector(axis),
            copy=copy,
        )
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
