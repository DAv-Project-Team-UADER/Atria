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
    "ajuda": NavActions["help"],
    "manual": NavActions["help"],
    "fechar ajuda": NavActions["close_help"],
    "fechar": NavActions["close_help"],
    "enviar": NavActions["send"],
    "aceitar": NavActions["send"],
    "cancelar": NavActions["cancel"],
}
