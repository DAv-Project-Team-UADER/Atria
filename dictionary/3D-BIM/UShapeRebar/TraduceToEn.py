"""English spoken-word mapping for the U-Shape Rebar function of ATRIA (3D-BIM)."""

try:
    from .UShapeRebar import UShapeRebar
except ImportError:
    UShapeRebar = None

TraduceToEn = {
    "create U-shape rebar":   UShapeRebar,
    "new U bar":              UShapeRebar,
    "generate U-shape rebar": UShapeRebar,
    "add U reinforcing bar":  UShapeRebar,
    "create U rebar":         UShapeRebar,
}