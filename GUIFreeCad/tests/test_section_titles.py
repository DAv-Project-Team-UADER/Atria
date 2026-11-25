# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

"""Tests for section titles and UX labels across ATRIA categories."""

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


class TestSectionTitles(unittest.TestCase):
    """Verifies that each section presents a clear, descriptive title."""

    def test_format_section_title_all_main_categories_es(self) -> None:
        from ui.Textos import format_section_title

        expected = {
            "Base": "Sección: Categorías Principales",
            "": "Sección: Categorías Principales",
            "Base > 3D-BIM": "Sección: 3D - Modelado BIM",
            "Base > 2D-Drafting": "Sección: 2D - Dibujo y Boceto",
            "Base > Annotation": "Sección: Anotación y Cotas",
            "Base > Manage": "Sección: Administración y Gestión BIM",
            "Base > Modify": "Sección: Modificar y Transformar",
            "Base > Preferences": "Sección: Preferencias y Ajustes",
            "Base > Snapping": "Sección: Enganche (Snapping)",
            "Base > StatusBar": "Sección: Barra de Estado y Vistas",
            "Base > Utils": "Sección: Utilidades y Herramientas",
            "Base > Explorer": "Sección: Explorador de Archivos",
            "Base > Explorer > file": "Sección: Explorador de Archivos > Archivo",
            "Base > Explorer > edit": "Sección: Explorador de Archivos > Edición",
            "Base > Explorer > print": "Sección: Explorador de Archivos > Imprimir / Exportar PDF",
        }

        for path, exp in expected.items():
            with self.subTest(path=path):
                title = format_section_title(path, "es")
                self.assertEqual(title, exp)

    def test_format_section_title_multilingual(self) -> None:
        from ui.Textos import format_section_title

        # English
        self.assertEqual(
            format_section_title("Base > 3D-BIM", "en"),
            "Section: 3D - BIM Modeling"
        )
        self.assertEqual(
            format_section_title("Base > Explorer > file", "en"),
            "Section: File Explorer > File"
        )

        # Portuguese
        self.assertEqual(
            format_section_title("Base > 3D-BIM", "pt"),
            "Seção: 3D - Modelagem BIM"
        )

    def test_panel_section_title_updates_on_render_context(self) -> None:
        """AtriaPanel._sectionTitleLabel must reflect the active section."""
        try:
            from PySide6.QtWidgets import QApplication
            from ui.AtriaPanel import AtriaPanel
            from ui.ContextView import ContextView
            app = QApplication.instance() or QApplication([])
        except ImportError:
            self.skipTest("PySide6 not available in test runner")

        panel = AtriaPanel()
        self.assertEqual(panel.CurrentSectionTitle, "Sección: Categorías Principales")

        # Render 3D-BIM
        panel.RenderContext(ContextView("Base > 3D-BIM"))
        self.assertEqual(panel.CurrentSectionTitle, "Sección: 3D - Modelado BIM")
        self.assertEqual(panel._sectionTitleLabel.text(), "Sección: 3D - Modelado BIM")

        # Render Modify
        panel.RenderContext(ContextView("Base > Modify"))
        self.assertEqual(panel.CurrentSectionTitle, "Sección: Modificar y Transformar")

        # Switch to English
        panel.SetLanguage("en")
        self.assertEqual(panel.CurrentSectionTitle, "Section: Modify & Transform")

    def test_explorer_button_is_first_in_base_context(self) -> None:
        """Explorer must be the first button in Base icon list."""
        try:
            from PySide6.QtWidgets import QApplication
            from ui.AtriaPanel import AtriaPanel
            from ui.ContextView import ContextView, ContextEntryView
            app = QApplication.instance() or QApplication([])
        except ImportError:
            self.skipTest("PySide6 not available in test runner")

        panel = AtriaPanel()
        base_view = ContextView(
            "Base",
            [
                ContextEntryView("2d", "2D-Drafting", IsSubContext=True),
                ContextEntryView("3d", "3D-BIM", IsSubContext=True),
                ContextEntryView("anotacion", "Annotation", IsSubContext=True),
                ContextEntryView("explorador", "Explorer", IsSubContext=True),
            ],
            []
        )
        panel.RenderContext(base_view)

        # First button must be Explorer
        self.assertGreaterEqual(len(panel._toolButtons), 4)
        first_btn = panel._toolButtons[0]
        self.assertIn("Explorador", first_btn.text())


if __name__ == "__main__":
    unittest.main()
