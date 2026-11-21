# Copyright (C) 2026 The ATRIA Project Team
# SPDX-License-Identifier: GPL-3.0-or-later

"""Módulo unificado para visualización de diálogos de ayuda en diccionarios ATRIA."""

from __future__ import annotations


def show_help_dialog(title: str, content: str) -> None:
    """Muestra la ayuda en consola y abre la ventana emergente de ATRIA."""
    header = f"=== Ayuda: {title} ==="
    print(header)
    print(content)

    try:
        from GUIFreeCad.ui.HelpDialog import AtriaHelpDialog
        AtriaHelpDialog.ShowHelp(title, content)
    except Exception as e:
        print(f"[ATRIA] Error mostrando ventana de ayuda: {e}")
