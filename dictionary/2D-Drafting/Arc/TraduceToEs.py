"""Comandos de voz en español para la función Arco (Arc) de ATRIA (2D-Drafting)."""

try:
    from .Arc import Arc
except ImportError:
    Arc = None

TraduceToEs = {
    "arco":            Arc,
    "curva":           Arc,
    "crear arco":      Arc,
    "crear curva":     Arc,
}