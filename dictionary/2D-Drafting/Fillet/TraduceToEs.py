"""Comandos de voz en español para la función Redondeo/Chaflán (Fillet) de ATRIA (2D-Drafting)."""

try:
    from .Fillet import Fillet
except ImportError:
    Fillet = None

TraduceToEs = {
    "chaflán":          Fillet,
    "redondear":        Fillet,
    "redondear borde":  Fillet,
    "recortar borde":   Fillet,
}