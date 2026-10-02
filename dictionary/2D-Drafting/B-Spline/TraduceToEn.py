"""English spoken-word mapping for the B-Spline function of ATRIA (2D-Drafting)."""

try:
    # The module name contains a hyphen, so it cannot be imported with `from . import`.
    from importlib import import_module

    BSpline = import_module(".B-Spline", __package__).BSpline
except ImportError:
    BSpline = None

TraduceToEn = {
    "b spline":                 BSpline,
    "b curve":                  BSpline,
    "b spline curve":           BSpline,
    "create b curve":           BSpline,
    "create b spline curve":    BSpline,
}