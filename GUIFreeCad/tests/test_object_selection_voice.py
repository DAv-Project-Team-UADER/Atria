# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Tests unitarios y de integración para la categoría de Selección y Navegación de Objetos."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

GUI_ROOT = Path(__file__).resolve().parents[1]
ATRIA_DIR = GUI_ROOT.parent

for p in (ATRIA_DIR, GUI_ROOT):
    text = str(p)
    if text not in sys.path:
        sys.path.insert(0, text)

from GUIFreeCad.navigation.browser import Browser
from GUIFreeCad.ui.HelpContent import get_help_for_category
from GUIFreeCad.ui.IconLocator import IconLocator
from GUIFreeCad.ui.Textos import format_section_title
from selection.object_selection import ObjectSelection


class TestObjectSelectionVoiceCategory(unittest.TestCase):
    """Verifica que la categoría Select y sus comandos funcionen por voz y navegación."""

    def test_browser_enters_select_category_by_voice(self) -> None:
        from GUIFreeCad.core.language_code import LanguageCode
        from GUIFreeCad.core.preferences import Preferences

        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.Es
        dic_root = ATRIA_DIR / "dictionary"
        browser = Browser(dictionary_root=dic_root, prefs=prefs)
        self.assertEqual(browser.ContextPath, "Base")

        # Decir 'seleccionar' desde Base entra a Select
        res = browser.ProcessPhrase("seleccionar")
        self.assertTrue(res.Success)
        self.assertIn("select", browser.ContextPath.lower())

        # Dentro de Select, probar comandos
        for cmd in ["avanzar", "siguiente", "retroceder", "anterior", "seleccionar", "deseleccionar", "seleccionar todos", "deseleccionar todos", "editar", "borrar"]:
            res_cmd = browser.ProcessPhrase(cmd)
            self.assertTrue(res_cmd.Success, f"Falló comando '{cmd}' dentro de Select")
            self.assertEqual(res_cmd.Action, "execute")

        # Subir de regreso a Base
        res_up = browser.ProcessPhrase("subir")
        self.assertTrue(res_up.Success)
        self.assertEqual(browser.ContextPath, "Base")

    def test_browser_enters_select_in_english(self) -> None:
        from GUIFreeCad.core.language_code import LanguageCode
        from GUIFreeCad.core.preferences import Preferences

        prefs = Preferences()
        prefs.SetLanguage = LanguageCode.En
        dic_root = ATRIA_DIR / "dictionary"
        browser = Browser(dictionary_root=dic_root, prefs=prefs)

        res = browser.ProcessPhrase("select")
        self.assertTrue(res.Success)
        self.assertIn("select", browser.ContextPath.lower())

        for cmd in ["next", "previous", "select", "deselect", "select all", "clear selection", "edit", "delete"]:
            res_cmd = browser.ProcessPhrase(cmd)
            self.assertTrue(res_cmd.Success, f"Failed voice command '{cmd}' in English Select")
            self.assertEqual(res_cmd.Action, "execute")

    def test_object_selection_methods_mocked(self) -> None:
        sel = ObjectSelection()
        mock_doc = MagicMock()
        mock_obj1 = MagicMock(Name="Pared001", Label="Pared Principal")
        mock_obj2 = MagicMock(Name="Puerta001", Label="Puerta Entrada")
        mock_doc.Objects = [mock_obj1, mock_obj2]
        mock_doc.getObject.side_effect = lambda n: mock_obj1 if n == "Pared001" else mock_obj2

        mock_gui = MagicMock()
        import selection.object_selection as os_module
        os_module.App = MagicMock(activeDocument=lambda: mock_doc)
        os_module.Gui = mock_gui

        # SelectNext
        sel.VectorSelection(["Pared001", "Puerta001"])
        sel.SelectNext()
        mock_gui.Selection.addSelection.assert_called_with(mock_obj1)

        mock_gui.Selection.reset_mock()
        sel.SelectNext()
        mock_gui.Selection.addSelection.assert_called_with(mock_obj2)

        # SelectPrevious
        mock_gui.Selection.reset_mock()
        sel.SelectPrevious()
        mock_gui.Selection.addSelection.assert_called_with(mock_obj1)

        # SelectCurrent / DeselectCurrent
        mock_gui.Selection.reset_mock()
        sel.SelectCurrent()
        mock_gui.Selection.addSelection.assert_called_with(mock_obj1)

        mock_gui.Selection.reset_mock()
        sel.DeselectCurrent()
        mock_gui.Selection.removeSelection.assert_called_with(mock_obj1)

        # SelectAll
        mock_gui.Selection.reset_mock()
        sel.SelectAll()
        self.assertEqual(mock_gui.Selection.addSelection.call_count, 2)

        # DeselectAll
        mock_gui.Selection.reset_mock()
        sel.DeselectAll()
        mock_gui.Selection.clearSelection.assert_called_once()

    def test_icon_locator_resolves_select_icons(self) -> None:
        loc = IconLocator()
        for key in ["select", "next", "previous", "selectall", "deselectall"]:
            icon = loc.Find(key)
            self.assertTrue(len(icon) > 0, f"No se encontró icono SVG para {key}")
            self.assertTrue(icon.endswith(".svg"), f"Icono para {key} no termina en .svg")

    def test_help_content_select_category(self) -> None:
        title, items, text = get_help_for_category("Select")
        self.assertIn("Selección", title)
        cmds = [cmd for cmd, _ in items]
        self.assertIn("avanzar", cmds)
        self.assertIn("retroceder", cmds)
        self.assertIn("seleccionar", cmds)
        self.assertIn("deseleccionar", cmds)
        self.assertIn("seleccionar todos", cmds)
        self.assertIn("deseleccionar todos", cmds)


if __name__ == "__main__":
    unittest.main()
