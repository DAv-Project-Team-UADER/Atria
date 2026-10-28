# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Comandos de navegación por voz en español."""

try:
    from .NavActions import NavActions
except ImportError:
    from NavActions import NavActions

TraduceToEs = {
    "subir": NavActions["up"],
    "volver": NavActions["up"],
    "atras": NavActions["up"],
    "contexto": NavActions["show_context"],
    "enviar": NavActions["send"],
    "aceptar": NavActions["send"],
    "cancelar": NavActions["cancel"],
}
