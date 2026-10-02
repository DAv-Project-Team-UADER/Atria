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

"""BIM Material — Menú BIM → Manage → Material.

Administra los materiales del documento. Un material define la apariencia y las
propiedades físicas de los elementos (color, transparencia, densidad, propiedades
mecánicas y térmicas) y se vincula a los objetos BIM a través de su propiedad
`Material`. Los materiales nuevos aparecen en la vista de árbol bajo el grupo
"Materials".

Sin argumentos abre el administrador de materiales; con argumentos crea el
material y lo asigna.
Comando FreeCAD: BIM_Material.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Material"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _Assign(material, objects):
    """Vincula el material a cada objeto que admita la propiedad Material."""
    for obj in objects:
        if "Material" not in obj.PropertiesList:
            raise ValueError(
                f"{obj.Label or obj.Name} no admite la propiedad Material."
            )
        obj.Material = material


def BIMMaterial(
    name=None,
    color=None,
    transparency=None,
    multi=False,
    objects=None,
    physical=None,
):
    """Crea un material BIM y opcionalmente lo asigna a objetos.

    Parámetros
    ----------
    name : str, opcional
        Nombre del material. Si se omite, FreeCAD usa "Material".
    color : tuple, opcional
        Color como tripla RGB de 0.0 a 1.0, o cuádrupla con alfa de 0.0 a 1.0.
    transparency : float, opcional
        Transparencia de 0 a 100. Solo tiene efecto si no se pasa `color`.
    multi : bool
        Si es True, crea un multi-material (capas de materiales) en lugar de un
        material simple.
    objects : list, opcional
        Objetos BIM a los que asignar el material creado.
    physical : dict, opcional
        Propiedades físicas del material (densidad, módulo de elasticidad,
        resistencia a la tracción, etc.) que se copian al nuevo material.

    Devuelve
    --------
    El objeto Material o MultiMaterial creado.
    """
    doc = _RequireDocument()

    if not (name or color or transparency or objects or physical):
        _Require3dView()
        FreeCADGui.runCommand(COMMAND)
        return None

    if multi and (color or transparency or physical):
        raise ValueError(
            "Un multi-material no lleva color ni propiedades físicas propias."
        )

    import Arch

    doc.openTransaction("Material")
    try:
        created = (
            Arch.makeMultiMaterial(name)
            if multi
            else Arch.makeMaterial(name, color, transparency)
        )

        if physical:
            props = (
                created.PropertiesList if not multi else created.Material.PropertiesList
            )
            target = created if not multi else created.Material
            for key, value in physical.items():
                if key not in props:
                    raise ValueError(f"El material no tiene la propiedad {key}.")
                setattr(target, key, value)

        if objects:
            _Assign(created, objects)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return created
