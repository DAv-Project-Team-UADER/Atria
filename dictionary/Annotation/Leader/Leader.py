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

"""Leader — Menú BIM → Annotation → Leader.

Crea una línea de referencia (leader): un objeto Wire con un símbolo de flecha
en el último punto. Se usa junto con la herramienta Text para las anotaciones
BIM. Si se pasan los puntos, el Wire se crea directamente; si no, el comando de
FreeCAD queda a la espera de que el usuario los elija en la vista.
Comando FreeCAD: BIM_Leader.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Leader"
MIN_POINTS = 2


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _AsVectorList(points):
    return [FreeCAD.Vector(float(p[0]), float(p[1]), float(p[2])) for p in points]


def _CreateLeader(points):
    """Crea el Wire del líder con la flecha final y lo devuelve."""
    import Draft
    from draftutils import params

    doc = _RequireDocument()
    obj = Draft.make_wire(points)
    if FreeCAD.GuiUp and obj.ViewObject:
        obj.ViewObject.LineColor = params.get_param("DefaultTextColor") | 0x000000FF
        obj.ViewObject.ArrowTypeEnd = params.get_param("dimsymbolend")
    Draft.autogroup(obj)
    doc.recompute()
    return obj


def CreateLeader(points=None):
    """Crea una línea de referencia con flecha en el último punto.

    Parámetros
    ----------
    points : list, opcional
        Lista de puntos (x, y, z) que definen el líder; hacen falta al menos
        dos. Si se omite se activa el comando interactivo.

    Devuelve
    --------
    object: el Wire creado, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()
    _Require3dView()

    if points is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    points = _AsVectorList(points)
    if len(points) < MIN_POINTS:
        raise ValueError("El líder necesita al menos dos puntos.")

    return _CreateLeader(points)


Leader = {
    "leader": CreateLeader,
}
