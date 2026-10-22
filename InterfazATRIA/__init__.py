# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Interfaz ATRIA: panel desacoplado y componentes de UI para FreeCAD."""

from .AtriaPanel import AtriaPanel, DavPanel
from .ContextView import ContextEntryView, ContextView
from .FlashOverlay import FlashOverlay
from .IconLocator import IconLocator
from .Paletas import DARK, FONT_MONO, FONT_SANS, LIGHT
from .Textos import TEXTS

__all__ = [
    "AtriaPanel",
    "DavPanel",
    "ContextEntryView",
    "ContextView",
    "FlashOverlay",
    "IconLocator",
    "DARK",
    "FONT_MONO",
    "FONT_SANS",
    "LIGHT",
    "TEXTS",
]
