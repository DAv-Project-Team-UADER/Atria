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

"""Comandos FreeCAD de la seccion Drafting2D (consolidado).

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
    x: float = None,
    y: float = None,
    radius: float = None,
    start_angle: float = 0.0,
    end_angle: float = 90.0,
    z: float = 0.0,
):
    """Crea un arco de circunferencia a partir de centro, radio y angulos."""
    if x is None or y is None or radius is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Arc", 0)
        return None
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    x3: float = None,
    y3: float = None,
):
    """Crea un arco a partir de tres puntos en el plano."""
    if x1 is None or y1 is None or x2 is None or y2 is None or x3 is None or y3 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Arc_3Points", 0)
        return None
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    x3: float = None,
    y3: float = None,
):
    """Crea una curva B-Spline a traves de puntos."""
    if x1 is None or y1 is None or x2 is None or y2 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_BSpline", 0)
        return None
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
        ]
        if x3 is not None and y3 is not None:
            pts.append(FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0))
        obj = Draft.make_bspline(pts)
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    x3: float = None,
    y3: float = None,
):
    """Crea una curva Bezier a traves de puntos."""
    if x1 is None or y1 is None or x2 is None or y2 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_BezCurve", 0)
        return None
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
        ]
        if x3 is not None and y3 is not None:
            pts.append(FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0))
        obj = Draft.make_bezcurve(pts)
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
    x: float = None,
    y: float = None,
    radius: float = None,
    z: float = 0.0,
):
    """Crea un circulo en el plano de trabajo a partir de su centro y radio."""
    if x is None or y is None or radius is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Circle", 0)
        return None
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    x3: float = None,
    y3: float = None,
    x4: float = None,
    y4: float = None,
):
    """Crea una curva Bezier cubica con 4 puntos de control."""
    if x1 is None or y1 is None or x2 is None or y2 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_CubicBezCurve", 0)
        return None
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
        ]
        if x3 is not None and y3 is not None:
            pts.append(FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0))
        if x4 is not None and y4 is not None:
            pts.append(FreeCAD.Vector(x4, y4, 0.0) if FreeCAD else (x4, y4, 0.0))
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
    major_radius: float = None,
    minor_radius: float = None,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea una elipse a partir de sus radios mayor y menor."""
    if major_radius is None or minor_radius is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Ellipse", 0)
        return None
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
def fillet(radius: float = None):
    """Crea un redondeo / chaflan con el radio especificado."""
    if radius is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Fillet", 0)
        return None
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    z1: float = 0.0,
    z2: float = 0.0,
):
    """Crea un segmento de linea recta entre (x1, y1, z1) y (x2, y2, z2)."""
    if x1 is None or y1 is None or x2 is None or y2 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Line", 0)
        return None
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
def point(x: float = None, y: float = None, z: float = 0.0):
    """Crea un punto en la posicion (x, y, z)."""
    if x is None or y is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Point", 0)
        return None
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
    nfaces: int = None,
    radius: float = None,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
):
    """Crea un poligono regular de n caras y radio especificado."""
    if nfaces is None or radius is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Polygon", 0)
        return None
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
    x1: float = None,
    y1: float = None,
    x2: float = None,
    y2: float = None,
    x3: float = None,
    y3: float = None,
):
    """Crea una polilinea / alambre conectando los puntos dados."""
    if x1 is None or y1 is None or x2 is None or y2 is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Wire", 0)
        return None
    doc = _get_or_create_doc()
    try:
        import Draft

        pts = [
            FreeCAD.Vector(x1, y1, 0.0) if FreeCAD else (x1, y1, 0.0),
            FreeCAD.Vector(x2, y2, 0.0) if FreeCAD else (x2, y2, 0.0),
        ]
        if x3 is not None and y3 is not None:
            pts.append(FreeCAD.Vector(x3, y3, 0.0) if FreeCAD else (x3, y3, 0.0))
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
    x: float = None,
    y: float = None,
    length: float = None,
    width: float = None,
    z: float = 0.0,
):
    """Crea un rectangulo a partir de su origen (x, y) y dimensiones (largo, ancho)."""
    if x is None or y is None or length is None or width is None:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Draft_Rectangle", 0)
        return None
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
    """Abre o crea un boceto (Sketch) en el documento activo."""
    doc = FreeCAD.ActiveDocument if FreeCAD else None
    if doc is None and FreeCAD and hasattr(FreeCAD, "newDocument"):
        doc = FreeCAD.newDocument()
    try:
        import Show
        ActiveSketch = doc.getObject("Sketch") if doc else None
        if ActiveSketch is not None and hasattr(ActiveSketch, "ViewObject"):
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
            if ActiveSketch and ActiveSketch.ViewObject.RestoreCamera:
                ActiveSketch.ViewObject.TempoVis.saveCamera()
                if ActiveSketch.ViewObject.ForceOrtho:
                    ActiveSketch.ViewObject.Document.ActiveView.setCameraType("Orthographic")
            return ActiveSketch
    except Exception:
        pass

    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Sketcher_NewSketch", 0)
    return None


# Alias canónicos exportados para TraduceToEs y TraduceToEn

class _CommandDict(dict):
    """Contenedor híbrido dict + callable:
    - Es un dict {'nombre': func} para compatibilidad con la suite de workbench.
    - Es un callable ejecutable directamente por el motor de voz y Browser.
    """
    def __init__(self, key: str, func):
        super().__init__({key: func})
        self.func = func
        self._param_specs = getattr(func, "_param_specs", None)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def __name__(self):
        return getattr(self.func, "__name__", "cmd")

# Alias híbridos canónicos
Arc = _CommandDict("arc", arc)
ArcFrom3Points = _CommandDict("arc_from_3_points", arc_from_3_points)
BSpline = _CommandDict("b_spline", b_spline)
BezierCurve = _CommandDict("bezier_curve", bezier_curve)
Circle = _CommandDict("circle", circle)
CubicBezierCurve = _CommandDict("cubic_bezier_curve", cubic_bezier_curve)
Ellipse = _CommandDict("ellipse", ellipse)
Fillet = _CommandDict("fillet", fillet)
Line = _CommandDict("line", line)
Point = _CommandDict("point", point)
Polygon = _CommandDict("polygon", polygon)
Polyline = _CommandDict("polyline", polyline)
Rectangle = _CommandDict("rectangle", rectangle)
Sketch = _CommandDict("sketch", _sketch)
