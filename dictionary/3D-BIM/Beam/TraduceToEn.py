"""English spoken-word mapping for the Beam function of ATRIA (3D-BIM)."""

try:
    from .Beam import Beam
except ImportError:
    Beam = None

TraduceToEn = {
    "create beam":          Beam,
    "new beam":             Beam,
    "generate beam":        Beam,
    "add beam":             Beam,
}