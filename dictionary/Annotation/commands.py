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

"""Comandos FreeCAD de la seccion Annotation (consolidado).

Cada funcion conserva su comportamiento original; este modulo
reune lo que antes vivia en una carpeta por funcion.
"""
import FreeCAD
import FreeCADGui
import FreeCADGui as Gui


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc

def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


# --- Aligned_Dimension ---
"""Aligned dimension — Menú BIM → Annotation → Aligned dimension.

Crea una cota alineada (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionAligned (atajo D, I).
"""

COMMAND_ALIGNED_DIMENSION = "BIM_DimensionAligned"

def aligned_dimension():
    """Abre la herramienta de cota alineada.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    La medida queda alineada a la geometría de referencia.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_ALIGNED_DIMENSION)

# --- Horizontal_Dimension ---
"""Horizontal dimension — Menú BIM → Annotation → Horizontal dimension.

Crea una cota horizontal (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionHorizontal (atajo D, H).
"""

COMMAND_HORIZONTAL_DIMENSION = "BIM_DimensionHorizontal"

def horizontal_dimension():
    """Abre la herramienta de cota horizontal.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    Requiere un plano de trabajo horizontal adecuado.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_HORIZONTAL_DIMENSION)

# --- Vertical_Dimension ---
"""Vertical dimension — Menú BIM → Annotation → Vertical dimension.

Crea una cota vertical (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionVertical (atajo D, V).
"""

COMMAND_VERTICAL_DIMENSION = "BIM_DimensionVertical"

def vertical_dimension():
    """Abre la herramienta de cota vertical.

    Los dos puntos, o la arista de referencia, se marcan en la vista 3D.
    Requiere un plano de trabajo vertical adecuado.

    Devuelve
    --------
    None. El objeto Dimension lo crea el comando al cerrar.
    """
    _require_document()
    _require_3d_view()
    FreeCADGui.runCommand(COMMAND_VERTICAL_DIMENSION)
