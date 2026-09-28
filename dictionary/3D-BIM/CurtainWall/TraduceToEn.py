"""English spoken-word mapping for the Curtain Wall function of ATRIA (3D-BIM)."""

try:
    from .CurtainWall import CurtainWall
except ImportError:
    CurtainWall = None

TraduceToEn = {
    "create curtain wall":  CurtainWall,
    "new curtain wall":     CurtainWall,
    "generate glass facade": CurtainWall,
    "add curtain wall":     CurtainWall,
}