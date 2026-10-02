"""Comandos de voz en español para la función Arco de 3 puntos (ArcFrom3Points) de ATRIA (2D-Drafting)."""

try:
    from .ArcFrom3Points import ArcFrom3Points
except ImportError:
    ArcFrom3Points = None

TraduceToEs = {
    "arco de 3 puntos":             ArcFrom3Points,
    "curva de 3 puntos":            ArcFrom3Points,
    "curva por 3 puntos":           ArcFrom3Points,
    "arco por 3 puntos":            ArcFrom3Points,
    "crear arco de 3 puntos":       ArcFrom3Points,
    "crear curva de 3 puntos":      ArcFrom3Points,
    "crear curva por 3 puntos":     ArcFrom3Points,
    "crear arco por 3 puntos":      ArcFrom3Points,
}