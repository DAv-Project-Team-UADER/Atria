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

"""Box — Menú BIM → 3D/BIM → Generic 3D tools → Box.

Crea un Part Box definiendo sus dimensiones gráficamente con 4 clics
(esquina, arista, cara y espesor), sin tener que editar propiedades después.
Sirve como base de cualquier otro objeto BIM.
Comando FreeCAD: BIM_Box.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Box"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_3d_view():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def box(length=None, width=None, height=None, placement=None):
    """Crea una caja.

    Parámetros
    ----------
    length, width, height : float, opcional
        Dimensiones en mm. Si se omite alguna, se abre la herramienta
        interactiva de 4 clics sobre el plano de trabajo.
    placement : FreeCAD.Placement, opcional
        Posición y orientación de la caja creada por script.

    Devuelve
    --------
    El objeto Part::Box creado, o None en modo interactivo.
    """
    doc = _require_document()
    _require_3d_view()

    if length is None or width is None or height is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    if length <= 0 or width <= 0 or height <= 0:
        raise RuntimeError("Las dimensiones de la caja deben ser mayores que cero.")

    doc.openTransaction("Box")
    try:
        result = doc.addObject("Part::Box", "Box")
        result.Length = length
        result.Width = width
        result.Height = height
        if placement is not None:
            result.Placement = placement
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
