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

"""Comandos FreeCAD de la seccion 2D-Drafting (consolidado).

Cada funcion soporta ejecucion parametrica completa con dictado por voz y
dialogos interactivos de captura de coordenadas, ademas de fallback interactivo.
"""
from __future__ import annotations

import types

try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None  # type: ignore[assignment]
    FreeCADGui = None  # type: ignore[assignment]
    Gui = None  # type: ignore[assignment]

try:
    import DraftTools  # noqa: F401
except ImportError:
    pass


class _ParamSpec:
    """Especificacion de parametro compatible con Validator y ParameterCollector."""

    def __init__(self, index: int, name: str, param_type: type, required: bool = True) -> None:
        self.index = index
        self.name = name
        self.param_type = param_type
        self.required = required


def _get_or_create_doc():
    if FreeCAD is None:
        return None
    doc = getattr(FreeCAD, "ActiveDocument", None)
    if doc is None and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    return doc


# --- Arc ---
def arc(
    x: float = 0.0,
    y: float = 0.0,
    radius: float = 50.0,
    start_angle: float = 0.0,
    end_angle: float = 90.0,
    z: float = 0.0,
):
    """Crea un arco de circunferencia a partir de centro, radio y angulos."""
    doc = _get_or_create_doc()
    try:
        import Draft

        center = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        pl = (
            FreeCAD.Placement(center, FreeCAD.Rotation())
            if FreeCAD and hasattr(FreeCAD, "Placement")
            else None
        )
        obj = Draft.make_circle(
            radius,
            placement=pl,
            startangle=start_angle,
            endangle=end_angle,
        )
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Arc", 0)
        return None


arc._param_specs = [
    _ParamSpec(1, "x", float, True),
    _ParamSpec(2, "y", float, True),
    _ParamSpec(3, "radius", float, True),
    _ParamSpec(4, "start_angle", float, True),
    _ParamSpec(5, "end_angle", float, True),
]

Arc = {"arc": arc}


# --- ArcFrom3Points ---
def arc_from_3_points(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 50.0,
    y2: float = 25.0,
    x3: float = 100.0,
    y3: float = 0.0,
):
    """Crea un arco a partir de tres puntos en el plano."""
    doc = _get_or_create_doc()
    try:
        import Draft

        p1 = FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0)
        p2 = FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0)
        p3 = FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0)
        obj = Draft.make_arc_3points([p1, p2, p3])
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Arc_3Points", 0)
        return None


arc_from_3_points._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
    _ParamSpec(5, "x3", float, True),
    _ParamSpec(6, "y3", float, True),
]

ArcFrom3Points = {"arc from 3 points": arc_from_3_points}


# --- BSpline ---
def b_spline(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 50.0,
    y2: float = 50.0,
    x3: float = 100.0,
    y3: float = 0.0,
):
    """Crea una curva B-Spline a traves de puntos."""
    doc = _get_or_create_doc()
    try:
        import Draft

        p1 = FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0)
        p2 = FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0)
        p3 = FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0)
        obj = Draft.make_bspline([p1, p2, p3])
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_BSpline", 0)
        return None


b_spline._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
    _ParamSpec(5, "x3", float, True),
    _ParamSpec(6, "y3", float, True),
]

BSpline = {"b spline": b_spline}


# --- BezierCurve ---
def bezier_curve(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 50.0,
    y2: float = 50.0,
    x3: float = 100.0,
    y3: float = 0.0,
):
    """Crea una curva Bezier a traves de puntos."""
    doc = _get_or_create_doc()
    try:
        import Draft

        p1 = FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0)
        p2 = FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0)
        p3 = FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0)
        obj = Draft.make_bezcurve([p1, p2, p3])
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_BezCurve", 0)
        return None


bezier_curve._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
    _ParamSpec(5, "x3", float, True),
    _ParamSpec(6, "y3", float, True),
]

BezierCurve = {"bezier curve": bezier_curve}


# --- Circle ---
def circle(
    x: float = 0.0,
    y: float = 0.0,
    radius: float = 50.0,
    z: float = 0.0,
):
    """Crea un circulo en el plano de trabajo a partir de su centro y radio."""
    doc = _get_or_create_doc()
    try:
        import Draft

        center = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        pl = (
            FreeCAD.Placement(center, FreeCAD.Rotation())
            if FreeCAD and hasattr(FreeCAD, "Placement")
            else None
        )
        obj = Draft.make_circle(radius, placement=pl)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Circle", 0)
        return None


circle._param_specs = [
    _ParamSpec(1, "x", float, True),
    _ParamSpec(2, "y", float, True),
    _ParamSpec(3, "radius", float, True),
]

Circle = {"circle": circle}


# --- CubicBezierCurve ---
def cubic_bezier_curve(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 25.0,
    y2: float = 50.0,
    x3: float = 75.0,
    y3: float = 50.0,
    x4: float = 100.0,
    y4: float = 0.0,
):
    """Crea una curva Bezier cubica con 4 puntos de control."""
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
            FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0),
            FreeCAD.Vector(x4, y4, 0.0) if FreeCAD else (x4, y4, 0.0),
        ]
        obj = Draft.make_bezcurve(pts)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_CubicBezCurve", 0)
        return None


cubic_bezier_curve._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
    _ParamSpec(5, "x3", float, True),
    _ParamSpec(6, "y3", float, True),
    _ParamSpec(7, "x4", float, True),
    _ParamSpec(8, "y4", float, True),
]

CubicBezierCurve = {"cubic bezier curve": cubic_bezier_curve}


# --- Ellipse ---
def ellipse(
    major_radius: float = 100.0,
    minor_radius: float = 50.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una elipse a partir de sus radios mayor y menor."""
    doc = _get_or_create_doc()
    try:
        import Draft

        center = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        pl = (
            FreeCAD.Placement(center, FreeCAD.Rotation())
            if FreeCAD and hasattr(FreeCAD, "Placement")
            else None
        )
        obj = Draft.make_ellipse(major_radius, minor_radius, placement=pl)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Ellipse", 0)
        return None


ellipse._param_specs = [
    _ParamSpec(1, "major_radius", float, True),
    _ParamSpec(2, "minor_radius", float, True),
]

Ellipse = {"ellipse": ellipse}


# --- Fillet ---
def fillet(radius: float = 10.0):
    """Crea un redondeo / chaflan con el radio especificado."""
    doc = _get_or_create_doc()
    try:
        import Draft

        selection = FreeCADGui.Selection.getSelection() if FreeCADGui else []
        if selection:
            obj = Draft.make_fillet(selection, radius)
            if doc and hasattr(doc, "recompute"):
                doc.recompute()
            return obj
    except Exception:
        pass
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Draft_Fillet", 0)
    return None


fillet._param_specs = [
    _ParamSpec(1, "radius", float, True),
]

Fillet = {"fillet": fillet}


# --- Line ---
def line(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 100.0,
    y2: float = 0.0,
    z1: float = 0.0,
    z2: float = 0.0,
):
    """Crea un segmento de linea recta entre (x1, y1, z1) y (x2, y2, z2)."""
    doc = _get_or_create_doc()
    try:
        import Draft

        p1 = FreeCAD.Vector(x1, y1, z1) if FreeCAD else (x1, y1, z1)
        p2 = FreeCAD.Vector(x2, y2, z2) if FreeCAD else (x2, y2, z2)
        obj = Draft.make_line(p1, p2)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Line", 0)
        return None


line._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
]

Line = {"line": line}


# --- Point ---
def point(x: float = 0.0, y: float = 0.0, z: float = 0.0):
    """Crea un punto en la posicion (x, y, z)."""
    doc = _get_or_create_doc()
    try:
        import Draft

        pt = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        obj = Draft.make_point(pt)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Point", 0)
        return None


point._param_specs = [
    _ParamSpec(1, "x", float, True),
    _ParamSpec(2, "y", float, True),
]

Point = {"point": point}


# --- Polygon ---
def polygon(
    nfaces: int = 6,
    radius: float = 50.0,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea un poligono regular de n caras y radio especificado."""
    doc = _get_or_create_doc()
    try:
        import Draft

        center = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        pl = (
            FreeCAD.Placement(center, FreeCAD.Rotation())
            if FreeCAD and hasattr(FreeCAD, "Placement")
            else None
        )
        obj = Draft.make_polygon(nfaces, radius, placement=pl)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Polygon", 0)
        return None


polygon._param_specs = [
    _ParamSpec(1, "nfaces", int, True),
    _ParamSpec(2, "radius", float, True),
]

Polygon = {"polygon": polygon}


# --- Polyline ---
def polyline(
    x1: float = 0.0,
    y1: float = 0.0,
    x2: float = 50.0,
    y2: float = 50.0,
    x3: float = 100.0,
    y3: float = 0.0,
):
    """Crea una polilinea / alambre conectando los puntos dados."""
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
            FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0),
        ]
        obj = Draft.make_wire(pts)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Wire", 0)
        return None


polyline._param_specs = [
    _ParamSpec(1, "x1", float, True),
    _ParamSpec(2, "y1", float, True),
    _ParamSpec(3, "x2", float, True),
    _ParamSpec(4, "y2", float, True),
]

Polyline = {"polyline": polyline}


# --- Rectangle ---
def rectangle(
    x: float = 0.0,
    y: float = 0.0,
    length: float = 100.0,
    width: float = 50.0,
    z: float = 0.0,
):
    """Crea un rectangulo a partir de su origen (x, y) y dimensiones (largo, ancho)."""
    doc = _get_or_create_doc()
    try:
        import Draft

        center = FreeCAD.Vector(x, y, z) if FreeCAD else (x, y, z)
        pl = (
            FreeCAD.Placement(center, FreeCAD.Rotation())
            if FreeCAD and hasattr(FreeCAD, "Placement")
            else None
        )
        obj = Draft.make_rectangle(length, width, placement=pl)
        if doc and hasattr(doc, "recompute"):
            doc.recompute()
        return obj
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Rectangle", 0)
        return None


rectangle._param_specs = [
    _ParamSpec(1, "x", float, True),
    _ParamSpec(2, "y", float, True),
    _ParamSpec(3, "length", float, True),
    _ParamSpec(4, "width", float, True),
]

Rectangle = {"rectangle": rectangle}


# --- Sketch ---
def _sketch():
    import Show

    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    ActiveSketch = doc.getObject("Sketch")
    if ActiveSketch is None:
        raise RuntimeError("No se encontró un objeto 'Sketch' en el documento activo.")
    tv = Show.TempoVis(doc, tag=ActiveSketch.ViewObject.TypeId)
    ActiveSketch.ViewObject.TempoVis = tv
    if ActiveSketch.ViewObject.EditingWorkbench:
        tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)
    if ActiveSketch.ViewObject.HideDependent:
        tv.hide(tv.get_all_dependent(doc.getObject("Sketch"), ""))
    if ActiveSketch.ViewObject.ShowSupport:
        tv.show(
            [
                ref[0]
                for ref in ActiveSketch.AttachmentSupport
                if not (
                    ref[0].isDerivedFrom("App::Plane")
                    or ref[0].isDerivedFrom("App::LocalCoordinateSystem")
                )
            ]
        )
    if ActiveSketch.ViewObject.ShowLinks:
        tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
    tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
    tv.hide(ActiveSketch)
    del tv
    del ActiveSketch

    ActiveSketch = doc.getObject("Sketch")
    if ActiveSketch.ViewObject.RestoreCamera:
        ActiveSketch.ViewObject.TempoVis.saveCamera()
        if ActiveSketch.ViewObject.ForceOrtho:
            ActiveSketch.ViewObject.Document.ActiveView.setCameraType("Orthographic")


Sketch = {"sketch": _sketch}
