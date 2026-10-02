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

"""External Reference — Menú BIM → 3D/BIM → Generic 3D tools → External reference.

Inserta un enlace que copia la forma y los colores de un objeto que vive en
otro archivo de FreeCAD. Si el archivo de origen cambia, el objeto queda
marcado para recargarse desde su menú contextual.
Comando FreeCAD: Arch_Reference.
"""

import os

import FreeCAD
import FreeCADGui

COMMAND = "Arch_Reference"


def _require_document():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def external_reference(file_path=None, part=None):
    """Inserta una referencia a un objeto de otro archivo de FreeCAD.

    Parámetros
    ----------
    file_path : str, opcional
        Ruta al archivo .FCStd de origen. Si se omite, se abre el panel
        interactivo con el botón "Choose file...".
    part : str, opcional
        Nombre del objeto a enlazar dentro de ese archivo. Si el archivo tiene
        varios objetos, conviene agruparlos antes en un Arch BuildingPart.

    Devuelve
    --------
    El objeto reference creado, o None en modo interactivo.
    """
    doc = _require_document()

    if file_path is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    if not os.path.isfile(file_path):
        raise RuntimeError("No existe el archivo: " + file_path)

    import Arch

    doc.openTransaction("External reference")
    try:
        result = Arch.makeReference(file_path, part)
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return result
