# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

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
