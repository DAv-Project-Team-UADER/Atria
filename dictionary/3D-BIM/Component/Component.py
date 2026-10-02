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

"""Component — Menú BIM → 3D/BIM → Generic 3D tools → Component.

Convierte un objeto basado en Part en un componente Arch no paramétrico: le
agrega los atributos de componente (Additions, Subtractions, Material, Base,
Description, Tag) y permite definir su tipo de exportación IFC.
Comando FreeCAD: Arch_Component.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Arch_Component"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_part_selection():
    """Devuelve los objetos seleccionados que tienen una forma de Part."""
    selection = FreeCADGui.Selection.getSelection()
    if not selection:
        raise RuntimeError("Seleccioná un objeto basado en Part.")
    sin_forma = [obj.Label for obj in selection if not hasattr(obj, "Shape")]
    if sin_forma:
        raise RuntimeError(
            "Estos objetos no están basados en Part: " + ", ".join(sin_forma) + "."
        )
    return selection


def component():
    """Convierte la selección en componentes Arch no paramétricos.

    Requiere al menos un objeto sólido o con forma basada en Part, creado con
    cualquier workbench.

    Devuelve
    --------
    None. El componente lo crea el comando de FreeCAD.
    """
    _require_document()
    _require_part_selection()
    FreeCADGui.runCommand(COMMAND)
