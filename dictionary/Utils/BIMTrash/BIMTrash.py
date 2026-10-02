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

"""BIM Trash — Menú BIM → Utils → Move to Trash.

Mueve los objetos seleccionados a un grupo especial llamado "Trash". Si el grupo
no existe en el documento, lo crea. Los objetos quedan ocultos y fuera de su
grupo original, pero no se eliminan: siguen siendo recuperables desde la papelera.
Comando FreeCAD: BIM_Trash.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Trash"

TRASH_NAME = "Trash"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def GetTrash(create=False):
    """Devuelve el grupo Trash del documento, o None si no está y create es False.

    Parámetros
    ----------
    create : bool
        Si es True, crea el grupo Trash cuando todavía no existe.
    """
    doc = _RequireDocument()
    trash = doc.getObject(TRASH_NAME)
    if trash and trash.isDerivedFrom("App::DocumentObjectGroup"):
        return trash
    if not create:
        return None
    trash = doc.addObject("App::DocumentObjectGroup", TRASH_NAME)
    trash.Label = "Trash"
    return trash


def _RemoveFromParents(obj, trash):
    """Saca el objeto de los grupos o contenedores que lo referencian."""
    for parent in obj.InList:
        if parent == trash or not hasattr(parent, "Group"):
            continue
        if obj not in parent.Group:
            continue
        if hasattr(parent, "removeObject"):
            parent.removeObject(obj)
        else:
            group = parent.Group
            group.remove(obj)
            parent.Group = group


def BIMTrash(objects=None):
    """Mueve los objetos indicados a la papelera.

    Parámetros
    ----------
    objects : list, opcional
        Objetos a mover. Si se omite, se usa la selección actual.

    Devuelve
    --------
    El grupo Trash, o None si no había nada seleccionado.
    """
    doc = _RequireDocument()

    if objects is None:
        objects = FreeCADGui.Selection.getSelection()
    objects = list(objects)
    if not objects:
        return None

    doc.openTransaction("Move to Trash")
    try:
        bin_ = GetTrash(create=True)
        for obj in objects:
            bin_.addObject(obj)
            _RemoveFromParents(obj, bin_)
            if getattr(obj, "ViewObject", None):
                obj.ViewObject.hide()
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return bin_
