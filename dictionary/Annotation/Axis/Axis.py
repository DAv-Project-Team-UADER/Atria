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

"""Axis — Menú BIM → Annotation → Axis Tools → Axis.

Coloca una serie de ejes de referencia en el documento. La cantidad, la distancia
y el ángulo entre ejes son configurables, así como el estilo de numeración. Los
ejes sirven sobre todo para ajustar (snap) objetos, pueden combinarse en un
Axis System y se pueden referenciar desde otros objetos Arch para crear arrays
paramétricos.
API de FreeCAD: Arch.makeAxis(num, size, name).
"""

import FreeCAD
import FreeCADGui

DEFAULT_NUM = 5
DEFAULT_SIZE = 1000.0
DEFAULT_NAME = "Axes"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def CreateAxis(num=DEFAULT_NUM, size=DEFAULT_SIZE, name=DEFAULT_NAME):
    """Crea un sistema de ejes de referencia.

    Parámetros
    ----------
    num : int, opcional
        Cantidad de ejes a crear. Por defecto 5.
    size : float, opcional
        Distancia entre ejes. Por defecto 1000.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Axes".

    Devuelve
    --------
    object: el sistema de ejes creado.
    """
    _RequireDocument()
    _Require3dView()

    if int(num) < 1:
        raise ValueError("El sistema de ejes necesita al menos un eje.")
    if float(size) <= 0:
        raise ValueError("La distancia entre ejes debe ser mayor que cero.")

    import Arch

    return Arch.makeAxis(num=int(num), size=float(size), name=name)


Axis = {
    "axis": CreateAxis,
}