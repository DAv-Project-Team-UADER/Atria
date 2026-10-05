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

"""Grid — Menú BIM → Annotation → Grid.

Coloca un objeto tipo rejilla en el documento. Sirve de base para construir
objetos Arch que necesitan un marco regular pero complejo: ventanas, muros
cortina, rejillas de columnas, barandillas, etc. Es un objeto 2D editable como
una hoja de cálculo (filas, columnas, tamaños y celdas fusionadas) y también
puede comportarse como un Axis System para propagar la ubicación de otros
objetos Arch.
API de FreeCAD: Arch.makeGrid(name).
"""

import FreeCAD
import FreeCADGui

DEFAULT_NAME = "Grid"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def CreateGrid(name=DEFAULT_NAME, rows=None, columns=None, width=None, height=None):
    """Crea una rejilla 2D.

    Parámetros
    ----------
    name : str, opcional
        Nombre del objeto creado. Por defecto "Grid".
    rows : int, opcional
        Cantidad de filas de la rejilla.
    columns : int, opcional
        Cantidad de columnas de la rejilla.
    width : float, opcional
        Ancho total de la rejilla.
    height : float, opcional
        Alto total de la rejilla.

    Devuelve
    --------
    object: la rejilla creada.
    """
    doc = _RequireDocument()
    _Require3dView()

    if rows is not None and int(rows) < 1:
        raise ValueError("La rejilla necesita al menos una fila.")
    if columns is not None and int(columns) < 1:
        raise ValueError("La rejilla necesita al menos una columna.")

    import Arch

    grid = Arch.makeGrid(name=name)

    if rows is not None:
        grid.Rows = int(rows)
    if columns is not None:
        grid.Columns = int(columns)
    if width is not None:
        grid.Width = float(width)
    if height is not None:
        grid.Height = float(height)

    doc.recompute()
    return grid


Grid = {
    "grid": CreateGrid,
}