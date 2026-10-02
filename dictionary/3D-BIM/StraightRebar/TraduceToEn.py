"""English spoken-word mapping for the Straight Rebar function of ATRIA (3D-BIM)."""

try:
    from .StraightRebar import StraightRebar
except ImportError:
    StraightRebar = None

TraduceToEn = {
    "create straight rebar":        StraightRebar,
    "new straight bar":             StraightRebar,
    "generate straight rebar":      StraightRebar,
    "add straight reinforcing bar": StraightRebar,
}