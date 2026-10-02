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

"""Shape Builder — Menú BIM → 3D/BIM → Generic 3D tools → Shape builder...

Abre el constructor de formas de Part, que arma geometría más compleja a
partir de primitivas: arista desde 2 vértices, alambre desde aristas, cara
desde vértices o aristas, cascarón desde caras y sólido desde un cascarón.
Comando FreeCAD: Part_Builder.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Part_Builder"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def shape_builder():
    """Abre el panel del constructor de formas.

    Cada operación pide sus propios subelementos (vértices, aristas o caras),
    que se seleccionan dentro del panel antes de pulsar "Create"; "Solid from
    shell" no necesita selección previa.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND)
