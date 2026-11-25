# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg

"""Sentinels for ATRIA voice navigation (up, show_context, help, close_help, send, cancel)."""

from typing import Any

def _go_up() -> None:
    return None

def _show_context() -> None:
    return None

def _help() -> None:
    return None

def _close_help() -> None:
    return None

def _send() -> None:
    return None

def _cancel() -> None:
    return None

NavActions: dict[str, Any] = {
    "up": _go_up,
    "show_context": _show_context,
    "help": _help,
    "close_help": _close_help,
    "send": _send,
    "cancel": _cancel,
}
