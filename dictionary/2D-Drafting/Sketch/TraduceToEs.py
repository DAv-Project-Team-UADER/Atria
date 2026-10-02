"""Comandos de voz en español para la función Boceto (Sketch) de ATRIA (2D-Drafting)."""

try:
    from .Sketch import Sketch
except ImportError:
    Sketch = None

TraduceToEs = {
    "boceto":         Sketch,
    "nuevo boceto":   Sketch,
    "crear boceto":   Sketch,
    "sketch":         Sketch,
    "bosquejo":       Sketch,
}