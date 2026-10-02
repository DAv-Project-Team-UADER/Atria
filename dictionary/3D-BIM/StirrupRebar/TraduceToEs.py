"""Comandos de voz en español para la función Estribo (StirrupRebar) de ATRIA (3D-BIM)."""

try:
    from .StirrupRebar import StirrupRebar
except ImportError:
    StirrupRebar = None

TraduceToEs = {
    "crear estribo":           StirrupRebar,
    "nuevo estribo":           StirrupRebar,
    "generar estribos":        StirrupRebar,
    "añadir estribo":          StirrupRebar,
    "crear cerco de refuerzo": StirrupRebar,
}