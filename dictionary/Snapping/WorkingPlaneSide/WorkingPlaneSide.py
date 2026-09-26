"""Working Plane Side — Menú BIM → Snapping → Working Plane Side.

Fija el plano de trabajo en posición Side (plano YZ, visto desde la derecha).
Comando FreeCAD: BIM_SetWPSide (atajo W, P, 3).
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


def working_plane_side(offset=0):
    """Orienta el plano de trabajo en Side.

    Parámetros
    ----------
    offset : float
        Distancia en mm del plano respecto del origen, sobre +X. Por defecto 0.

    Devuelve
    --------
    El plano de trabajo activo.
    """
    _require_document()
    _require_3d_view()

    import WorkingPlane

    plane = WorkingPlane.get_working_plane(update=False)
    plane.set_to_side(offset)
    return plane
