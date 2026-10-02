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

"""BIM Layers — Menú BIM → Manage → Manage Layers.

Administra las capas del proyecto. Una capa es un grupo especial que propaga
automáticamente sus propiedades visuales (color de línea, color de forma, grosor
de línea, estilo de dibujo y transparencia) a los objetos que contiene, y es
compatible con la importación y exportación a IFC y DXF/DWG.

Sin argumentos abre el Administrador de Capas; con argumentos crea la capa
directamente.
Comando FreeCAD: BIM_Layers.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Layers"

DEFAULTS = {
    "line_color": (0.0, 0.0, 0.0),
    "shape_color": (0.8, 0.8, 0.8),
    "line_width": 2.0,
    "draw_style": "Solid",
    "transparency": 0,
}


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def BIMLayers(
    name,
    line_color=None,
    shape_color=None,
    line_width=None,
    draw_style=None,
    transparency=None,
    objects=None,
    apply=True,
):
    """Crea una capa BIM con las propiedades visuales indicadas.

    Los objetos que se agreguen a la capa adoptan de inmediato sus propiedades
    visuales. Si se omite algún parámetro visual se usa el valor por defecto de
    Draft: negro y 2.0 de grosor para la línea, gris claro y opaco para la forma.

    Parámetros
    ----------
    name : str
        Nombre de la capa. Es el único dato obligatorio.
    line_color : tuple, opcional
        Color de la línea como tripla RGB de 0.0 a 1.0.
    shape_color : tuple, opcional
        Color de la forma como tripla RGB de 0.0 a 1.0.
    line_width : float, opcional
        Grosor de la línea, en píxeles.
    draw_style : str, opcional
        Estilo de dibujo: "Solid", "Dashed", "Dotted" o "Dashdot".
    transparency : int, opcional
        Transparencia de la forma, de 0 (opaco) a 100.
    objects : list, opcional
        Objetos a agregar a la capa al crearla.
    apply : bool
        Si es False, solo crea la capa y deja las propiedades visuales sin
        tocar, tal cual quedarían con la interfaz cerrada.

    Devuelve
    --------
    El objeto Draft Layer creado.
    """
    doc = _RequireDocument()

    if not name:
        raise ValueError("La capa necesita un nombre.")

    if not (
        line_color or shape_color or line_width or draw_style or transparency or objects
    ):
        # Solo el nombre no alcanza para una ruta no interactiva: el nombre va
        # con el resto de las propiedades visuales, que es lo que hace el
        # administrador de capas.
        _Require3dView()
        FreeCADGui.runCommand(COMMAND)
        return None

    kwargs = {}
    if apply:
        kwargs = {
            "line_color": DEFAULTS["line_color"] if line_color is None else line_color,
            "shape_color": DEFAULTS["shape_color"]
            if shape_color is None
            else shape_color,
            "line_width": DEFAULTS["line_width"] if line_width is None else line_width,
            "draw_style": DEFAULTS["draw_style"] if draw_style is None else draw_style,
            "transparency": DEFAULTS["transparency"]
            if transparency is None
            else transparency,
        }

    import Draft

    doc.openTransaction("Layer")
    try:
        created = Draft.make_layer(name, **kwargs)
        if objects:
            # Los objetos se cuelgan del contenedor de capas, no de la capa.
            from draftmake.make_layer import get_layer_container

            container = get_layer_container()
            for obj in objects:
                container.addObject(obj)
        doc.recompute()
    except Exception:
        doc.abortTransaction()
        raise
    doc.commitTransaction()
    doc.recompute()
    return created
