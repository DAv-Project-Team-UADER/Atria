"""English spoken-word mapping for the Arch Rebar (Custom Rebar) function of ATRIA (3D-BIM)."""

try:
    from .ArchRebar import ArchRebar
except ImportError:
    ArchRebar = None

TraduceToEn = {
    "create custom rebar": ArchRebar,
    "new reinforcing bar": ArchRebar,
    "generate rebar":      ArchRebar,
    "add rebar":           ArchRebar,
    "create custom bar":   ArchRebar,
}