"""English spoken-word mapping for the Door function of ATRIA (3D-BIM)."""

try:
    from .Door import Door
except ImportError:
    Door = None

TraduceToEn = {
    "create door":          Door,
    "new door":             Door,
    "generate door":        Door,
    "add door":             Door,
}