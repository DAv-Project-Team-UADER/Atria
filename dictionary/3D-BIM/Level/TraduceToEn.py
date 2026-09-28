"""English spoken-word mapping for the Level function of ATRIA (3D-BIM)."""

try:
    from .Level import Level
except ImportError:
    Level = None

TraduceToEn = {
    "create level":         Level,
    "new level":            Level,
    "generate floor":       Level,
    "add level":            Level,
    "create floor":         Level,
}