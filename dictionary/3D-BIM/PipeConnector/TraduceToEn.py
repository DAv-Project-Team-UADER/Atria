"""English spoken-word mapping for the Pipe Connector function of ATRIA (3D-BIM)."""

try:
    from .PipeConnector import PipeConnector
except ImportError:
    PipeConnector = None

TraduceToEn = {
    "create connector":     PipeConnector,
    "new connector":        PipeConnector,
    "generate pipe joint":  PipeConnector,
    "add connection":       PipeConnector,
}