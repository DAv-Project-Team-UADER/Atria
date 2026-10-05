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

"""Working Plane Front — Menú BIM → Snapping → Working Plane Front.

Sitúa el plano de trabajo (Working Plane) en el plano XZ global, es decir la
vista frontal. Es una de las tres orientaciones canónicas de plano de trabajo
(Frontal, Planta, Lateral) accesibles desde el menú Snapping. Los nuevos objetos
y los snaps se proyectan sobre este plano.
Comando FreeCAD: BIM_SetWPFront.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_SetWPFront"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def SetWorkingPlaneFront():
    """Alinea el plano de trabajo con el plano XZ global (vista frontal).

    Parámetros
    ----------
    Ninguno: es una acción directa, sin argumentos.

    Devuelve
    --------
    None: el plano de trabajo queda alineado con la vista frontal.
    """
    _RequireDocument()
    _Require3dView()

    FreeCADGui.runCommand(COMMAND)


WorkingPlaneFront = {
    "working plane front": SetWorkingPlaneFront,
}
