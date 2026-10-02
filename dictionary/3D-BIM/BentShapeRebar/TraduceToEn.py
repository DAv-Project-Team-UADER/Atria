"""English spoken-word mapping for the Bent-Shape Rebar function of ATRIA (3D-BIM)."""

try:
    from .BentShapeRebar import BentShapeRebar
except ImportError:
    BentShapeRebar = None

TraduceToEn = {
    "create bent-shape rebar":   BentShapeRebar,
    "new bent bar":              BentShapeRebar,
    "generate bent-shape rebar": BentShapeRebar,
    "add bent reinforcing bar":  BentShapeRebar,
    "create bent rebar":         BentShapeRebar,
}