"""Comandos de voz en español para la función Ventana (Window) de ATRIA (3D-BIM)."""

try:
    from .Window import Window
except ImportError:
    Window = None

TraduceToEs = {
    "crear ventana":        Window,
    "nueva ventana":        Window,
    "generar ventana":      Window,
    "añadir ventana":       Window,
}