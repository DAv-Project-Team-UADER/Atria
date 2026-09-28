"""English spoken-word mapping for the Building function of ATRIA (3D-BIM)."""

try:
    from .Building import Building
except ImportError:
    Building = None

TraduceToEn = {
    "create building":      Building,
    "new building":         Building,
    "generate building":    Building,
    "add building":         Building,
}