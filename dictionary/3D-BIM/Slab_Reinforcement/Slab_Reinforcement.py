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

"""Slab Reinforcement — Menú BIM → 3D/BIM → Reinforcement tools → Slab Reinforcement.

Crea un mallado de refuerzo dentro de una losa modelada como Arch Structure:
barras paralelas y transversales (rectas, L, U o curvas) con barras de
distribución opcionales.
Comando FreeCAD: Reinforcement_SlabRebars (addon Reinforcement).
"""

import FreeCAD
import FreeCADGui

COMMAND = "Reinforcement_SlabRebars"
ADDON_MODULE = "SlabReinforcement"

# Caras de la losa sobre las que se puede apoyar la malla.
MESH_COVER_ALONG = ("Top", "Bottom")


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _require_addon(module):
    """Verifica que el addon Reinforcement esté instalado."""
    try:
        __import__(module)
    except ImportError:
        raise RuntimeError(
            "Falta el addon Reinforcement. Instalalo desde el Addon Manager."
        )


def _require_selected_face(que):
    """Devuelve (objeto, nombre de cara) de la única cara seleccionada."""
    import Draft

    selection = FreeCADGui.Selection.getSelectionEx()
    if not selection:
        raise RuntimeError("Seleccioná " + que + ".")
    sel = selection[0]
    faces = [sub for sub in sel.SubElementNames if sub.startswith("Face")]
    if len(faces) != 1:
        raise RuntimeError("Seleccioná exactamente una cara: " + que + ".")
    if Draft.getType(sel.Object) != "Structure":
        raise RuntimeError("El objeto seleccionado no es un Arch Structure.")
    return sel.Object, faces[0]


def slab_reinforcement():
    """Abre el diálogo de refuerzo de losa sobre la cara seleccionada.

    Requiere una losa (Arch Structure) existente con una de sus caras
    seleccionada y el addon Reinforcement instalado.

    Devuelve
    --------
    None. El SlabReinforcementGroup lo crea el diálogo al confirmar.
    """
    _require_document()
    _require_addon(ADDON_MODULE)
    _require_selected_face("una cara de la losa")
    FreeCADGui.runCommand(COMMAND)
