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

"""Draft Slope — Menú BIM → Utils → Set slope.

Da pendiente a las Draft Lines y Draft Wires seleccionadas modificando la
coordenada Z de sus vértices, a partir del primero. La pendiente se expresa
como tangente del ángulo horizontal: 0 es horizontal, 1 sube 45 grados, -1 baja
45 grados. En una polilínea la transformación se aplica segmento por segmento.

La pendiente siempre cambia Z, así que la herramienta funciona bien sobre
líneas rectas dibujadas en el plano XY.
Comando FreeCAD: Draft_Slope.
"""

import FreeCAD
import FreeCADGui

COMMAND = "Draft_Slope"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def DraftSlope(objects=None, value=None):
    """Aplica la pendiente indicada a las Draft Wires seleccionadas.

    Parámetros
    ----------
    objects : list, opcional
        Draft Wires a las que dar pendiente. Si se omite, se usa la selección
        actual.
    value : float, opcional
        Pendiente como tangente del ángulo horizontal: 0 es horizontal, 1 sube
        45 grados, -1 baja 45 grados. Si se omite, se abre el diálogo para
        elegirla.

    Devuelve
    --------
    La lista de Draft Wires modificadas, o None en modo interactivo.
    """
    doc = _RequireDocument()

    if value is None:
        _Require3dView()
        FreeCADGui.runCommand(COMMAND)
        return None

    if objects is None:
        objects = FreeCADGui.Selection.getSelection()
    objects = list(objects)
    if not objects:
        raise ValueError("Seleccioná al menos una línea o polilínea.")

    import Draft

    doc.openTransaction("Set slope")
    try:
        changed = []
        for obj in objects:
            if Draft.getType(obj) != "Wire" or len(obj.Points) < 2:
                continue
            previous = None
            points = []
            for point in obj.Points:
                if previous is None:
                    previous = point
                else:
                    dx, dy = point.x - previous.x, point.y - previous.y
                    rise = value * FreeCAD.Vector(dx, dy, 0).Length
                    previous = FreeCAD.Vector(point.x, point.y, previous.z + rise)
                points.append(previous)
            obj.Points = points
            changed.append(obj)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return changed
