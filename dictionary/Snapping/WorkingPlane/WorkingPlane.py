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

"""Working Plane — Menú BIM → Snapping → Working Plane.

Abre el panel "Select Plane" para definir el plano de trabajo a partir de
3 vértices, una cara, un objeto o los botones rápidos (Top, Front, Side,
Align, Auto), y configurar offset, cuadrícula y radio de snap.
Comando FreeCAD: Draft_SelectPlane (atajo W, P).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_SelectPlane"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def working_plane():
    """Abre el panel de selección del plano de trabajo.

    Si hay 3 vértices, una cara o un objeto seleccionados, FreeCAD define el
    plano a partir de esa geometría; si no, el panel queda abierto para
    elegir con los botones rápidos.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND)
