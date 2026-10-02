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

"""BIM WPView — Menú BIM → Utils → Working Plane View.

Alinea la cámara de la vista 3D de forma perpendicular al plano de trabajo
activo, poniendo la cuadrícula de frente. Facilita dibujar, medir y editar
sobre planos inclinados, fachadas o caras concretas del modelo.

Si el panel BIM Views está abierto y tiene un elemento seleccionado, alinea a
ese elemento; si no, alinea al plano de trabajo activo.
Comando FreeCAD: BIM_WPView.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_WPView"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def BIMWPView():
    """Alinea la vista 3D al plano de trabajo activo.

    Devuelve
    --------
    None: la vista 3D queda orientada de frente al plano de trabajo.
    """
    _RequireDocument()
    _Require3dView()
    FreeCADGui.runCommand(COMMAND)
