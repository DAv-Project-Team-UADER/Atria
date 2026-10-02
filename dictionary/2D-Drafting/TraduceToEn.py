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
"""Mapa de voz (EN) para la seccion 2D-Drafting (consolidado)."""

Arc = None  # TODO: sin implementacion en commands.py
ArcFrom3Points = None  # TODO: sin implementacion en commands.py
BSpline = None  # TODO: sin implementacion en commands.py
BezierCurve = None  # TODO: sin implementacion en commands.py
Circle = None  # TODO: sin implementacion en commands.py
CubicBezierCurve = None  # TODO: sin implementacion en commands.py
Ellipse = None  # TODO: sin implementacion en commands.py
Fillet = None  # TODO: sin implementacion en commands.py
Line = None  # TODO: sin implementacion en commands.py
Point = None  # TODO: sin implementacion en commands.py
Polygon = None  # TODO: sin implementacion en commands.py
Polyline = None  # TODO: sin implementacion en commands.py
Rectangle = None  # TODO: sin implementacion en commands.py
Sketch = None  # TODO: sin implementacion en commands.py

TraduceToEn = {
    # Arc
    'arc': Arc,
    'curve': Arc,
    'create arc': Arc,
    'create curve': Arc,
    # ArcFrom3Points
    'arc from 3 points': ArcFrom3Points,
    'curve from 3 points': ArcFrom3Points,
    'curve by 3 points': ArcFrom3Points,
    'arc by 3 points': ArcFrom3Points,
    'create arc from 3 points': ArcFrom3Points,
    'create curve from 3 points': ArcFrom3Points,
    'create curve by 3 points': ArcFrom3Points,
    'create arc by 3 points': ArcFrom3Points,
    # B-Spline
    'b spline': BSpline,
    'b curve': BSpline,
    'b spline curve': BSpline,
    'create b curve': BSpline,
    'create b spline curve': BSpline,
    # BezierCurve
    'bezier curve': BezierCurve,
    'create bezier curve': BezierCurve,
    # Circle
    'create circle': Circle,
    'circle': Circle,
    'circumference': Circle,
    'create circumference': Circle,
    # CubicBezierCurve
    'cubic bezier curve': CubicBezierCurve,
    'create cubic bezier curve': CubicBezierCurve,
    'cubic curve': CubicBezierCurve,
    # Ellipse
    'ellipse': Ellipse,
    'create ellipse': Ellipse,
    # Fillet
    'chamfer': Fillet,
    'fillet': Fillet,
    'fillet edge': Fillet,
    'trim edge': Fillet,
    # Line
    'line': Line,
    'create line': Line,
    'create straight line': Line,
    'straight line': Line,
    # Point
    'point': Point,
    'create point': Point,
    # Polygon
    'polygon': Polygon,
    'create polygon': Polygon,
    'create regular polygon': Polygon,
    'regular polygon': Polygon,
    # Polyline
    'polyline': Polyline,
    'create polyline': Polyline,
    'connect points': Polyline,
    # Rectangle
    'rectangle': Rectangle,
    'create rectangle': Rectangle,
    # Sketch
    'sketch': Sketch,
    'new sketch': Sketch,
    'create sketch': Sketch,
}
