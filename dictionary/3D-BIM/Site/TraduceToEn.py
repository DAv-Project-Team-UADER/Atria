"""English spoken-word mapping for the Site function of ATRIA (3D-BIM)."""

try:
    from .Site import Site
except ImportError:
    Site = None

TraduceToEn = {
    "create site":          Site,
    "new site":             Site,
    "generate terrain":     Site,
    "add site":             Site,
}