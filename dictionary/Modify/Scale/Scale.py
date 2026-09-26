"""Scale — Menú BIM → Modify → Scale.

Escala los objetos seleccionados desde un punto base, con factores
independientes en X, Y y Z.
Comando FreeCAD: Draft_Scale (atajo S, C).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Scale"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def scale(factor=None, center=(0, 0, 0), copy=False, clone=False):
    """Escala la selección actual.

    Parámetros
    ----------
    factor : float | FreeCAD.Vector | tuple, opcional
        Un número escala igual en los tres ejes; un vector (X, Y, Z) escala
        cada eje por separado. Si se omite, se abre la herramienta
        interactiva.
    center : FreeCAD.Vector | tuple
        Punto base de la escala. Por defecto el origen.
    copy : bool
        Si es True, crea una copia escalada y deja el original.
    clone : bool
        Si es True, crea un clon escalado y deja el original.

    Devuelve
    --------
    Los objetos escalados (o las copias/clones), o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if factor is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    if copy and clone:
        raise ValueError("Elegí copy o clone, no ambos.")

    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná al menos un objeto para escalar.")

    if isinstance(factor, (int, float)):
        factor = (factor, factor, factor)
    factor = FreeCAD.Vector(factor)
    if 0 in (factor.x, factor.y, factor.z):
        raise ValueError("El factor de escala no puede ser 0 en ningún eje.")

    import Draft

    doc.openTransaction("Scale")
    try:
        result = Draft.scale(
            selection,
            factor,
            center=FreeCAD.Vector(center),
            copy=copy,
            clone=clone,
        )
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
