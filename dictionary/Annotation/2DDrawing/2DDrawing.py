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

"""2D Drawing — Menú BIM → Annotation → Create 2D Views → 2D Drawing.

Crea un contenedor para albergar proyecciones 2D (un BuildingPart modificado
para funcionar como dibujo 2D). Si se indica un plano de sección, se generan
automáticamente la vista de sección ("Viewed lines") y el corte de sección
("Cut lines"), se aplastan sobre el plano XY y se agrupan dentro del objeto
"Drawing", exportable como un único DXF/SVG.
API de FreeCAD: Arch.make2DDrawing(objectslist, baseobj, name).
"""

import FreeCAD
import FreeCADGui

VIEWED_LINES = "Viewed lines"
CUT_LINES = "Cut lines"
CUT_FACES = "Cutfaces"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _Require3dView():
    view = FreeCADGui.activeView() if FreeCADGui.ActiveDocument else None
    if view is None or not hasattr(view, "getSceneGraph"):
        raise RuntimeError("No hay una vista 3D activa.")


def _SectionPlane(base):
    """Devuelve el plano de sección a usar, o None si no hay ninguno."""
    import Draft

    if base is not None:
        return base

    selection = FreeCADGui.Selection.getSelection()
    if len(selection) == 1 and Draft.getType(selection[0]) == "SectionPlane":
        return selection[0]
    return None


def _AddSectionView(drawing, section, mode, label):
    """Agrega al dibujo una proyección del plano de sección."""
    import Draft

    view = Draft.make_shape2dview(section)
    view.Label = label
    view.InPlace = False
    if mode is not None:
        view.ProjectionMode = mode
    drawing.addObject(view)
    return view


def _SectionCutsModel(section):
    """Verifica si el plano de sección realmente corta el modelo."""

    bb = FreeCAD.BoundBox()
    for obj in section.Objects:
        if hasattr(obj, "Shape") and obj.Shape:
            bb.add(obj.Shape.BoundBox)
    return bool(bb.isInside(section.Shape.CenterOfMass))


def CreateTwoDDrawing(base=None, objects=None, name=None):
    """Crea un dibujo 2D, con sus vistas si se pasa un plano de sección.

    Parámetros
    ----------
    base : object, opcional
        Plano de sección del que se extrae la vista. Por defecto, el único plano
        de sección de la selección actual.
    objects : list, opcional
        Contenido inicial del dibujo. Por defecto, vacío.
    name : str, opcional
        Nombre del objeto creado. Por defecto "Drawing".

    Devuelve
    --------
    object: el dibujo creado.
    """
    doc = _RequireDocument()
    _Require3dView()

    import Arch
    import Draft

    section = _SectionPlane(base)
    objectslist = list(objects) if isinstance(objects, (list, tuple)) else objects

    drawing = Arch.make2DDrawing(objectslist, baseobj=section, name=name)
    Draft.autogroup(drawing)

    if section is not None:
        _AddSectionView(drawing, section, None, VIEWED_LINES)
        if _SectionCutsModel(section):
            _AddSectionView(drawing, section, CUT_FACES, CUT_LINES)

    doc.recompute()
    return drawing


TwoDDrawing = {
    "2d drawing": CreateTwoDDrawing,
}
