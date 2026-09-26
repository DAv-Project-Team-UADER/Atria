"""Working Plane Top — Menú BIM → Snapping → Working Plane Top.

Fija el plano de trabajo en posición Top (plano XY, normal +Z).
Comando FreeCAD: BIM_SetWPTop (atajo W, P, 2).
"""

import FreeCAD
import FreeCADGui


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def working_plane_top(offset=0):
    """Orienta el plano de trabajo en Top.

    Parámetros
    ----------
    offset : float
        Distancia en mm del plano respecto del origen, sobre +Z. Por defecto 0.

    Devuelve
    --------
    El plano de trabajo activo.
    """
    _require_document()
    _require_3d_view()

    import WorkingPlane

    plane = WorkingPlane.get_working_plane(update=False)
    plane.set_to_top(offset)
    return plane
