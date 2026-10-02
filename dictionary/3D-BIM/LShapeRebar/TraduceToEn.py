"""English spoken-word mapping for the L-Shape Rebar function of ATRIA (3D-BIM)."""

try:
    from .LShapeRebar import LShapeRebar
except ImportError:
    LShapeRebar = None

TraduceToEn = {
    "create L-shape rebar":   LShapeRebar,
    "new L bar":              LShapeRebar,
    "generate L-shape rebar": LShapeRebar,
    "add L reinforcing bar":  LShapeRebar,
    "create L rebar":         LShapeRebar,
}