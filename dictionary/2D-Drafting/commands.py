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

Cada funcion conserva su comportamiento original; este modulo
reune lo que antes vivia en una carpeta por funcion.
"""
import FreeCAD
import FreeCADGui
import FreeCADGui as Gui

# Registrar el módulo DraftTools de FreeCAD para que sus comandos
# (Draft_Point, Draft_Line, etc.) estén disponibles al llamar a
# Gui.runCommand. Sin este import, falla con "No such command".
# DraftTools importa internamente todos los módulos draftguitools.gui_*
# que registran los comandos con Gui.addCommand.
try:
    import DraftTools  # noqa: F401
except ImportError:
    pass


# --- Arc ---
Arc = {
    "arc": lambda: Gui.runCommand('Draft_Arc', 0)
}

# --- ArcFrom3Points ---
ArcFrom3Points = {
    "arc from 3 points": lambda: Gui.runCommand('Draft_Arc_3Points', 0)
}

# --- BSpline ---
BSpline = {
    "b spline": lambda: Gui.runCommand('Draft_BSpline', 0)
}

# --- BezierCurve ---
BezierCurve = {
    "bezier curve": lambda: Gui.runCommand('Draft_BezCurve', 0)
}

# --- Circle ---
Circle = {
    "circle": lambda: Gui.runCommand('Draft_Circle', 0)
}

# --- CubicBezierCurve ---
CubicBezierCurve = {
    "cubic bezier curve": lambda: Gui.runCommand('Draft_CubicBezCurve', 0)
}

# --- Ellipse ---
Ellipse = {
    "ellipse": lambda: Gui.runCommand('Draft_Ellipse', 0)
}

# --- Fillet ---
Fillet = {
    "fillet": lambda: Gui.runCommand('Draft_Fillet', 0)
}

# --- Line ---
Line = {
    "line": lambda: Gui.runCommand('Draft_Line', 0)
}

# --- Point ---
Point = {
    "point": lambda: Gui.runCommand('Draft_Point', 0)
}

# --- Polygon ---
Polygon = {
    "polygon": lambda: Gui.runCommand('Draft_Polygon', 0)
}

# --- Polyline ---
Polyline = {
    "polyline": lambda: Gui.runCommand('Draft_Wire', 0)
}

# --- Rectangle ---
Rectangle = {
    "rectangle": lambda: Gui.runCommand('Draft_Rectangle', 0)
}

# --- Sketch ---
def _sketch():
    import Show
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    ActiveSketch = doc.getObject('Sketch')
    if ActiveSketch is None:
        raise RuntimeError("No se encontró un objeto 'Sketch' en el documento activo.")
    tv = Show.TempoVis(doc, tag=ActiveSketch.ViewObject.TypeId)
    ActiveSketch.ViewObject.TempoVis = tv
    if ActiveSketch.ViewObject.EditingWorkbench:
        tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)
    if ActiveSketch.ViewObject.HideDependent:
        tv.hide(tv.get_all_dependent(doc.getObject('Sketch'), ''))
    if ActiveSketch.ViewObject.ShowSupport:
        tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not (ref[0].isDerivedFrom("App::Plane") or ref[0].isDerivedFrom("App::LocalCoordinateSystem"))])
    if ActiveSketch.ViewObject.ShowLinks:
        tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
    tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
    tv.hide(ActiveSketch)
    del tv
    del ActiveSketch

    ActiveSketch = doc.getObject('Sketch')
    if ActiveSketch.ViewObject.RestoreCamera:
        ActiveSketch.ViewObject.TempoVis.saveCamera()
        if ActiveSketch.ViewObject.ForceOrtho:
            ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')

Sketch = {
    "sketch": _sketch
}
