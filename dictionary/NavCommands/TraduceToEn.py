# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""English navigation voice commands."""

try:
    from .NavActions import NavActions
except ImportError:
    from NavActions import NavActions

TraduceToEn = {
    "up": NavActions["up"],
    "back": NavActions["up"],
    "context": NavActions["show_context"],
    "send": NavActions["send"],
    "accept": NavActions["send"],
    "cancel": NavActions["cancel"],
}
