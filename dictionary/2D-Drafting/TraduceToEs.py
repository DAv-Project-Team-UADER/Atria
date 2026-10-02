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
"""Mapa de voz (ES) para la seccion 2D-Drafting (consolidado)."""

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

TraduceToEs = {
    # Arc
    'arco': Arc,
    'curva': Arc,
    'crear arco': Arc,
    'crear curva': Arc,
    # ArcFrom3Points
    'arco de 3 puntos': ArcFrom3Points,
    'curva de 3 puntos': ArcFrom3Points,
    'curva por 3 puntos': ArcFrom3Points,
    'arco por 3 puntos': ArcFrom3Points,
    'crear arco de 3 puntos': ArcFrom3Points,
    'crear curva de 3 puntos': ArcFrom3Points,
    'crear curva por 3 puntos': ArcFrom3Points,
    'crear arco por 3 puntos': ArcFrom3Points,
    # B-Spline
    'b spline': BSpline,
    'curva b': BSpline,
    'curva b spline': BSpline,
    'crear curva b': BSpline,
    'crear curva b spline': BSpline,
    # BezierCurve
    'curva de bezier': BezierCurve,
    'crear curva de bezier': BezierCurve,
    'crear curva bezier': BezierCurve,
    'curva bezier': BezierCurve,
    # Circle
    'crear círculo': Circle,
    'círculo': Circle,
    'circunferencia': Circle,
    'crear circunferencia': Circle,
    # CubicBezierCurve
    'curva de bezier cúbica': CubicBezierCurve,
    'curva bezier cúbica': CubicBezierCurve,
    'crear curva bezier cúbica': CubicBezierCurve,
    'crear curva de bezier cúbica': CubicBezierCurve,
    'curva cúbica': CubicBezierCurve,
    # Ellipse
    'elipse': Ellipse,
    'crear elipse': Ellipse,
    # Fillet
    'chaflán': Fillet,
    'redondear': Fillet,
    'redondear borde': Fillet,
    'recortar borde': Fillet,
    # Line
    'línea': Line,
    'crear línea': Line,
    'crear línea recta': Line,
    'línea recta': Line,
    'crear recta': Line,
    'recta': Line,
    # Point
    'punto': Point,
    'crear punto': Point,
    # Polygon
    'polígono': Polygon,
    'crear polígono': Polygon,
    'crear polígono regular': Polygon,
    'polígono regular': Polygon,
    # Polyline
    'polilínea': Polyline,
    'crear polilínea': Polyline,
    'conectar puntos': Polyline,
    # Rectangle
    'rectángulo': Rectangle,
    'crear rectángulo': Rectangle,
    # Sketch
    'boceto': Sketch,
    'nuevo boceto': Sketch,
    'crear boceto': Sketch,
    'sketch': Sketch,
    'bosquejo': Sketch,
}
