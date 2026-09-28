"""English spoken-word mapping for the Pipe function of ATRIA (3D-BIM)."""

try:
    from .Pipe import Pipe
except ImportError:
    Pipe = None

TraduceToEn = {
    "create pipe":          Pipe,
    "new piping":           Pipe,
    "generate conduit":     Pipe,
    "add pipe":             Pipe,
}