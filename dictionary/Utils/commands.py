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

"""Comandos FreeCAD de la seccion Utils (consolidado).

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

def _replace_references(old, new):
    """Hace que los objetos que apuntaban a `old` apunten a `new`."""
    for parent in old.InList:
        for prop in parent.PropertiesList:
            value = getattr(parent, prop)
            if value == old:
                setattr(parent, prop, new)
            elif isinstance(value, list) and old in value:
                if prop == "Group" and hasattr(parent, "addObject"):
                    parent.addObject(new)
                else:
                    setattr(parent, prop, value + [new])
            else:
                continue
            FreeCAD.Console.PrintMessage(
                "Se actualizó la referencia de {} a este objeto.\n".format(parent.Label)
            )


# --- Unclone ---
"""Unclone — Menú BIM → Utils → Unclone.

Convierte un clon de tipo Arch en un objeto independiente del original:
conserva su forma y propiedades actuales pero deja de actualizarse cuando el
original cambia. Las referencias de otros objetos al clon se actualizan.
Comando FreeCAD: BIM_Unclone.
"""

COMMAND_UNCLONE = "BIM_Unclone"

# Propiedades del original que no se copian al objeto independizado.
SKIPPED_PROPERTIES = (
    "Objects",
    "CloneOf",
    "ExpressionEngine",
    "HorizontalArea",
    "Area",
    "VerticalArea",
    "PerimeterLength",
    "Proxy",
    "Shape",
)

def unclone(interactive=False):
    """Independiza el clon seleccionado de su original.

    Requiere exactamente un objeto seleccionado que sea un clon de tipo Arch
    (con la propiedad CloneOf). Los clones de Draft no están soportados.

    Parámetros
    ----------
    interactive : bool
        Si es True, abre la herramienta interactiva de FreeCAD en lugar de
        ejecutar la lógica por script.

    Devuelve
    --------
    El objeto independiente resultante, o None en modo interactivo.
    """
    doc = _require_document()

    if interactive:
        FreeCADGui.runCommand(COMMAND_UNCLONE)
        return None

    selection = FreeCADGui.Selection.getSelection()
    if len(selection) != 1:
        raise RuntimeError("Seleccioná exactamente un objeto.")
    obj = selection[0]

    import Arch
    import Draft

    if not getattr(obj, "CloneOf", None):
        if Draft.getType(obj) == "Clone":
            raise RuntimeError("Los clones de Draft todavía no están soportados.")
        raise RuntimeError("El objeto seleccionado no es un clon.")

    original = obj.CloneOf
    placement = FreeCAD.Placement(obj.Placement)

    doc.openTransaction("Unclone")
    try:
        if Draft.getType(obj) != Draft.getType(original):
            # El clon es de otro tipo: hay que crear un objeto del tipo original.
            new = getattr(Arch, "make" + Draft.getType(original))()
        else:
            new = obj
            new.CloneOf = None
            if getattr(new, "ViewObject", None):
                new.ViewObject.signalChangeIcon()

        for prop in original.PropertiesList:
            if prop not in SKIPPED_PROPERTIES:
                setattr(new, prop, getattr(original, prop))
        doc.recompute()
        new.Placement = original.Placement.multiply(placement)

        _replace_references(obj, new)

        if new != obj:
            label = obj.Label
            doc.removeObject(obj.Name)
            new.Label = label
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return new
