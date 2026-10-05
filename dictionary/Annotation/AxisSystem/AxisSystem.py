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

"""Axis System — Menú BIM → Annotation → Axis Tools → Axis System.

Combina dos o tres objetos Arch Axis en un único sistema, útil para definir los
puntos de intersección entre los distintos ejes. Los objetos Arch pueden usar
este sistema para duplicar su forma en esos puntos de intersección.
API de FreeCAD: Arch.makeAxisSystem(axes, name).
"""

import FreeCAD
import FreeCADGui

DEFAULT_NAME = "Axis System"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _AxesList(axes):
    """Normaliza el argumento a una lista de objetos Arch Axis."""
    import Draft

    if axes is None:
        axes = FreeCADGui.Selection.getSelection()
    axes = list(axes) if isinstance(axes, (list, tuple)) else [axes]

    if not axes:
        raise ValueError("Seleccioná al menos un eje para el sistema de ejes.")

    for axis in axes:
        if Draft.getType(axis) != "Axis":
            raise ValueError("Sólo se pueden combinar objetos Arch Axis.")

    return axes


def CreateAxisSystem(axes=None, name=DEFAULT_NAME):
    """Crea un sistema de ejes combinando los ejes indicados.

    Parámetros
    ----------
    axes : object o list, opcional
        Objeto Arch Axis o lista de ellos. Por defecto, la selección actual.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Axis System".

    Devuelve
    --------
    object: el sistema de ejes creado.
    """
    _RequireDocument()
    _Require3dView()

    import Arch

    return Arch.makeAxisSystem(_AxesList(axes), name=name)


AxisSystem = {
    "axis system": CreateAxisSystem,
}