"""English spoken-word mapping for the Helical Rebar function of ATRIA (3D-BIM)."""

try:
    from .HelicalRebar import HelicalRebar
except ImportError:
    HelicalRebar = None

TraduceToEn = {
    "create helical rebar":  HelicalRebar,
    "new helical bar":       HelicalRebar,
    "generate spiral rebar": HelicalRebar,
    "add helical bar":       HelicalRebar,
}