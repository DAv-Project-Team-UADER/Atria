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

"""BIM IFC Properties — Menú BIM → Manage → IFC Management → Manage IFC Properties.

Gestiona los conjuntos de propiedades IFC (Property Sets o Psets) de los objetos
BIM: asigna los psets predefinidos del estándar y permite crear propiedades
personalizadas. Los psets quedan incrustados en el elemento para exportarlo
correctamente a IFC. Los psets propios se declaran en un `CustomPsets.csv` en
el directorio de datos del usuario.
Comando FreeCAD: BIM_IfcProperties.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_IfcProperties"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def BIMIfcProperties(objects=None):
    """Abre el administrador de propiedades IFC.

    La edición de los psets (nombre, tipo y valor de cada propiedad) se hace en
    el diálogo: esta función solo valida que haya documento y, si se pasan
    objetos, que la selección sea utilizable.

    Parámetros
    ----------
    objects : list, opcional
        Objetos cuyas propiedades IFC se van a gestionar. Si se omite, se usa
        la selección actual.

    Devuelve
    --------
    None: la herramienta es un diálogo y no devuelve resultado.
    """
    _RequireDocument()
    _Require3dView()

    if objects is not None and len(objects) == 0:
        raise ValueError("Pasá al menos un objeto para gestionar sus propiedades IFC.")

    if objects:
        FreeCADGui.Selection.clearSelection()
        for obj in objects:
            FreeCADGui.Selection.addSelection(obj)

    FreeCADGui.runCommand(COMMAND)
