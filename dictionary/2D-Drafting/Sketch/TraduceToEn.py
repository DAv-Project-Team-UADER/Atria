"""English spoken-word mapping for the Sketch function of ATRIA (2D-Drafting)."""

try:
    from .Sketch import Sketch
except ImportError:
    Sketch = None

TraduceToEn = {
    "sketch":         Sketch,
    "new sketch":     Sketch,
    "create sketch":  Sketch,
}