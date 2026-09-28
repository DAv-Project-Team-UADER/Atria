"""Comandos de voz en español para la función Tubo (Pipe) de ATRIA (3D-BIM)."""

try:
    from .Pipe import Pipe
except ImportError:
    Pipe = None

TraduceToEs = {
    "crear tubo":           Pipe,
    "nueva tubería":        Pipe,
    "generar caño":         Pipe,
    "añadir tubo":          Pipe,
}