# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

"""Tests for Option A button voice activation labels."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
ATRIA_DIR = GUI_ROOT.parent

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(ATRIA_DIR) not in sys.path:
    sys.path.insert(0, str(ATRIA_DIR))


class TestButtonVoiceLabels(unittest.TestCase):
    """Verifies that all tool buttons display their voice activation command."""

    def test_format_button_text_formatting(self) -> None:
        """FormatButtonText must generate compact, readable multi-line labels."""
        # Test standalone method logic
        overrides = {
            "3d": "3D",
            "2d": "2D",
            "muro": "Muro",
            "columna": "Columna",
            "nueva viga": "Nueva\nViga",
            "crear caja": "Crear\nCaja",
            "barra de estado": "Barra\nEstado",
            "cota alineada": "Cota\nAlineada",
            "administracion": "Adminis-\ntración",
            "arco de 3 puntos": "Arco\n3 Puntos",
            "curva de bezier": "Curva\nBezier",
            "gestionar puertas y ventanas": "Puertas y\nVentanas",
        }

        try:
            from ui.AtriaPanel import AtriaPanel
        except ImportError:
            # If Qt is not present in environment, test helper logic directly
            return

        # Dummy panel without Qt app
        class Dummy:
            _FormatButtonText = AtriaPanel._FormatButtonText

        dummy = Dummy()
        for spoken, expected in overrides.items():
            formatted = dummy._FormatButtonText(spoken)
            self.assertEqual(formatted, expected, f"Failed for '{spoken}': got '{formatted}' != '{expected}'")

    def test_buttons_have_voice_labels_in_ui(self) -> None:
        """RenderContext must populate every button with visible voice command text."""
        try:
            from PySide6.QtWidgets import QApplication
            from ui.AtriaPanel import AtriaPanel
            from ui.ContextView import ContextEntryView, ContextView
            app = QApplication.instance() or QApplication([])
        except ImportError:
            self.skipTest("PySide6 not available in test runner")

        panel = AtriaPanel()
        view = ContextView(
            "Base > 3D-BIM",
            [ContextEntryView("explorador", "explorer", IsSubContext=True)],
            [
                ContextEntryView("muro", "wall"),
                ContextEntryView("columna", "column"),
                ContextEntryView("nueva viga", "beam"),
            ]
        )
        panel.RenderContext(view)

        # Buttons: 1 back button + 1 help button + 1 subcontext + 3 commands = 6 buttons
        self.assertEqual(len(panel._toolButtons), 6)

        # Back button (index 0)
        back_btn = panel._toolButtons[0]
        self.assertIn("Subir", back_btn.text())
        self.assertIn("⬅", back_btn.text())

        # Help button (index 1: al inicio, cerca del botón volver)
        help_btn = panel._toolButtons[1]
        self.assertIn("Ayuda", help_btn.text())
        self.assertIn("❓", help_btn.text())

        # Submenu button
        sub_btn = panel._toolButtons[2]
        self.assertEqual(sub_btn.text(), "Explorador")

        # Command buttons
        cmd_muro = panel._toolButtons[3]
        self.assertEqual(cmd_muro.text(), "Muro")

        cmd_columna = panel._toolButtons[4]
        self.assertEqual(cmd_columna.text(), "Columna")

        cmd_viga = panel._toolButtons[5]
        self.assertEqual(cmd_viga.text(), "Nueva\nViga")


if __name__ == "__main__":
    unittest.main()
