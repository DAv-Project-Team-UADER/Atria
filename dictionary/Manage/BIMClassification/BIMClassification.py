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

"""BIM Classification — Menú BIM → Manage → Classification.

Asigna clasificaciones estandarizadas (Uniclass, OmniClass, MasterFormat, etc.)
a los objetos BIM y a los materiales del modelo. La clasificación queda como
metadato en las propiedades del elemento, para poder filtrarlo y exportarlo a
IFC. Los sistemas de clasificación son archivos .xml que FreeCAD busca en el
directorio de configuración del usuario.
Comando FreeCAD: BIM_Classification.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Classification"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def BIMClassification(objects=None):
    """Abre el administrador de clasificaciones BIM.

    La asignación de la clasificación (sistema, código y categoría) se hace en
    el diálogo: esta función solo valida que haya documento y, si se pasan
    objetos, que la selección sea utilizable.

    Parámetros
    ----------
    objects : list, opcional
        Objetos que se van a clasificar. Si se omite, se usa la selección actual.

    Devuelve
    --------
    None: la herramienta es un diálogo y no devuelve resultado.
    """
    _RequireDocument()
    _Require3dView()

    if objects is not None and len(objects) == 0:
        raise ValueError("Pasá al menos un objeto para clasificar.")

    if objects:
        FreeCADGui.Selection.clearSelection()
        for obj in objects:
            FreeCADGui.Selection.addSelection(obj)

    FreeCADGui.runCommand(COMMAND)
