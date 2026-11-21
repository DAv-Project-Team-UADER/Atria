# Copyright (C) 2026 The ATRIA Project Team
# SPDX-License-Identifier: GPL-3.0-or-later

"""Compatibilidad hacia atrás para Explorer: reexporta show_help_dialog unificado."""

from __future__ import annotations

try:
    from dictionary._help_gui import show_help_dialog
except ImportError:
    try:
        from _help_gui import show_help_dialog
    except ImportError:
        def show_help_dialog(title: str, content: str) -> None:
            print(f"=== Ayuda: {title} ===")
            print(content)
            try:
                from GUIFreeCad.ui.HelpDialog import AtriaHelpDialog
                AtriaHelpDialog.ShowHelp(title, content)
            except Exception:
                pass
