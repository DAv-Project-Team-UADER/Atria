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

"""Objects Library — Menú BIM → 3D/BIM → Generic 3D tools → Objects library.

Inserta en el modelo un objeto de equipamiento o mobiliario desde la Parts
Library, con un navegador integrado de archivos FCStd, STEP y BREP, local o
en línea desde el repositorio Git.
Comando FreeCAD: BIM_Library (addon Parts Library para el modo offline).
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Library"

# Puntos de inserción que ofrece el panel para los archivos STEP y BREP.
INSERTION_POINTS = (
    "Original",
    "Top left",
    "Top center",
    "Top right",
    "Middle left",
    "Middle center",
    "Middle right",
    "Bottom left",
    "Bottom center",
    "Bottom right",
)


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def objects_library():
    """Abre el navegador de la biblioteca de objetos.

    El archivo a insertar se elige en el panel. Los FCStd entran con su
    posición interna; los STEP y BREP piden además un punto de inserción y
    entran como Arch Equipment. El modo offline necesita el addon Parts
    Library instalado; el modo en línea usa el repositorio Git.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND)
