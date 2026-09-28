"""Comandos de voz en español para la función Conector (Pipe Connector) de ATRIA (3D-BIM)."""

try:
    from .PipeConnector import PipeConnector
except ImportError:
    PipeConnector = None

TraduceToEs = {
    "crear conector":       PipeConnector,
    "nuevo conector":       PipeConnector,
    "generar unión de tubos": PipeConnector,
    "añadir conexión":      PipeConnector,
}