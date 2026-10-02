"""English spoken-word mapping for the Stirrup Rebar function of ATRIA (3D-BIM)."""

try:
    from .StirrupRebar import StirrupRebar
except ImportError:
    StirrupRebar = None

TraduceToEn = {
    "create stirrup":          StirrupRebar,
    "new stirrup":             StirrupRebar,
    "generate stirrups":       StirrupRebar,
    "add stirrup":             StirrupRebar,
    "create reinforcing hoop": StirrupRebar,
}