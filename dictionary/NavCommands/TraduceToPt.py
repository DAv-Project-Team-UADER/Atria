# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Portuguese navigation voice commands."""

try:
    from .NavActions import NavActions
except ImportError:
    from NavActions import NavActions

TraduceToPt = {
    "subir": NavActions["up"],
    "voltar": NavActions["up"],
    "contexto": NavActions["show_context"],
    "enviar": NavActions["send"],
    "aceitar": NavActions["send"],
    "cancelar": NavActions["cancel"],
}
