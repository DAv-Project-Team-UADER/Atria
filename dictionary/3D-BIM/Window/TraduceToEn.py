"""English spoken-word mapping for the Window function of ATRIA (3D-BIM)."""

try:
    from .Window import Window
except ImportError:
    Window = None

TraduceToEn = {
    "create window":        Window,
    "new window":           Window,
    "generate window":      Window,
    "add window":           Window,
}