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

"""Draft SelectGroup — Menú BIM → Utils → Select group.

Selecciona de forma recursiva el contenido del grupo o contenedor seleccionado
(Std Group, Draft Block, Arch BuildingPart, etc.) en lugar del contenedor mismo:
la selección del grupo se anula y quedan seleccionados todos sus hijos, tanto
en la vista 3D como en la vista de árbol.

Si lo que está seleccionado no es un grupo, se selecciona el contenido del
grupo que lo contiene.
Comando FreeCAD: Draft_SelectGroup.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_SelectGroup"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _Children(container, recursive):
    """Hijos directos del contenedor, o todo su contenido si recursive."""
    if recursive:
        import Draft

        return Draft.get_group_contents(container)
    return list(getattr(container, "Group", []))


def _Collect(objects, recursive):
    """Arma la lista de hijos de cada objeto, o de su grupo contenedor."""
    from draftutils import groups

    contents = []
    for obj in objects:
        if groups.is_group(obj):
            contents.extend(_Children(obj, recursive))
            continue
        for parent in obj.InList:
            if groups.is_group(parent):
                contents.extend(_Children(parent, recursive))
    return contents


def DraftSelectGroup(objects=None, recursive=True):
    """Selecciona el contenido de los grupos indicados.

    Parámetros
    ----------
    objects : list, opcional
        Grupos o contenedores cuyo contenido hay que seleccionar. Si se omite,
        se usa la selección actual.
    recursive : bool
        Si es True, baja también por los subgrupos; si es False, se queda en
        los hijos directos del contenedor.

    Devuelve
    --------
    La lista de objetos que quedaron seleccionados.
    """
    _RequireDocument()
    _Require3dView()

    if objects is None:
        objects = FreeCADGui.Selection.getSelection()
    objects = list(objects)
    if not objects:
        raise ValueError("Seleccioná al menos un grupo o contenedor.")

    contents = _Collect(objects, recursive)
    if not contents:
        raise ValueError(
            "No se encontró contenido. Seleccioná grupos con objetos dentro, "
            "u objetos que pertenezcan a un grupo."
        )

    FreeCADGui.Selection.clearSelection()
    for obj in contents:
        FreeCADGui.Selection.addSelection(obj)
    return contents
