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

"""Aligned dimension — Menú BIM → Annotation → Aligned dimension.

Crea una cota alineada (objeto Dimension) entre dos puntos o a lo largo de una
arista seleccionada. El formato lo controlan los estilos de anotación del
documento.
Comando FreeCAD: BIM_DimensionAligned (atajo D, I).
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_DimensionAligned"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


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
    FreeCADGui.runCommand(COMMAND)
