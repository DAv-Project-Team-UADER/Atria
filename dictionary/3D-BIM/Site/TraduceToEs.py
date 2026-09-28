"""Comandos de voz en español para la función Sitio (Site) de ATRIA (3D-BIM)."""

try:
    from .Site import Site
except ImportError:
    Site = None

TraduceToEs = {
    "crear sitio":          Site,
    "nuevo sitio":          Site,
    "generar terreno":      Site,
    "añadir emplazamiento": Site,
}