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

"""Section Plane — Menú BIM → Annotation → Section Plane.

Crea un plano de sección, que define un plano de sección o de vista. Toma su
ubicación según el plano de trabajo de Draft actual y puede reubicarse y
reorientarse moviéndolo y rotándolo, hasta describir la vista 2D deseada. Los
objetos seleccionados al crearlo se añaden automáticamente y otros pueden
añadirse o quitarse después. Por sí solo no genera ninguna vista: es la base
del flujo de producción de dibujos 2D.
API de FreeCAD: Arch.makeSectionPlane(objectslist, name).
"""

import FreeCAD
import FreeCADGui

DEFAULT_NAME = "Section"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def CreateSectionPlane(objects=None, name=DEFAULT_NAME):
    """Crea un plano de sección según el plano de trabajo actual.

    Parámetros
    ----------
    objects : object o list, opcional
        Objetos a incluir en la sección. Si se omite, el plano considera todo
        el documento.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Section".

    Devuelve
    --------
    object: el plano de sección creado.
    """
    _RequireDocument()
    _Require3dView()

    import Arch

    objectslist = None
    if objects is not None:
        objectslist = list(objects) if isinstance(objects, (list, tuple)) else [objects]

    return Arch.makeSectionPlane(objectslist, name=name)


SectionPlane = {
    "section plane": CreateSectionPlane,
}
