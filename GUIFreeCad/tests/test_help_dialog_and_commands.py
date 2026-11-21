# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

"""Tests para la ventana de ayuda contextual, contenido de categorías y comandos de voz."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

GUI_ROOT = Path(__file__).resolve().parents[1]
ATRIA_DIR = GUI_ROOT.parent

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(ATRIA_DIR) not in sys.path:
    sys.path.insert(0, str(ATRIA_DIR))

from GUIFreeCad.navigation.browser import Browser, BrowserResult
from GUIFreeCad.ui.HelpContent import HELP_BY_CATEGORY, get_help_for_category
from GUIFreeCad.ui.HelpDialog import AtriaHelpDialog


class TestHelpContent(unittest.TestCase):
    """Verifica que todas las categorías tengan contenido de ayuda y explicaciones de botones."""

    def test_all_main_categories_have_help(self) -> None:
        categories = [
            "Base",
            "3D-BIM",
            "2D-Drafting",
            "Annotation",
            "Manage",
            "Modify",
            "Preferences",
            "Snapping",
            "StatusBar",
            "Utils",
            "Explorer",
        ]
        for cat in categories:
            with self.subTest(category=cat):
                title, items, text = get_help_for_category(cat)
                self.assertTrue(len(title) > 0, f"Categoría {cat} no tiene título de ayuda")
                self.assertTrue(len(items) > 0, f"Categoría {cat} no tiene botones documentados")
                self.assertIn("cerrar", text.lower())
                for cmd, desc in items:
                    self.assertTrue(len(cmd) > 0, f"Comando vacío en {cat}")
                    self.assertTrue(len(desc) > 0, f"Descripción vacía para {cmd} en {cat}")

    def test_mirror_categories_help(self) -> None:
        title_bim, items_bim, _ = get_help_for_category("BIM3D")
        self.assertTrue(len(items_bim) >= 30)

        title_draft, items_draft, _ = get_help_for_category("Drafting2D")
        self.assertTrue(len(items_draft) >= 10)


class TestAtriaHelpDialogLifecycle(unittest.TestCase):
    """Verifica el ciclo de vida de la ventana de ayuda (abrir, cerrar, consultar estado)."""

    def tearDown(self) -> None:
        AtriaHelpDialog.CloseHelp()

    def test_show_and_close_help(self) -> None:
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

        # Abrir ayuda
        dlg = AtriaHelpDialog.ShowHelp(
            "Test 3D-BIM",
            [("crear muro", "Construye un muro"), ("crear losa", "Construye una losa")],
        )
        self.assertIsNotNone(dlg)
        self.assertTrue(AtriaHelpDialog.IsHelpOpen())
        self.assertEqual(AtriaHelpDialog.GetActiveDialog(), dlg)

        # Cerrar ayuda
        closed = AtriaHelpDialog.CloseHelp()
        self.assertTrue(closed)
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())
        self.assertIsNone(AtriaHelpDialog.GetActiveDialog())

    def test_close_when_not_open_returns_false(self) -> None:
        AtriaHelpDialog.CloseHelp()
        self.assertFalse(AtriaHelpDialog.CloseHelp())


class TestVoiceHelpCommands(unittest.TestCase):
    """Verifica la invocación por voz de ayuda/manual y su cierre con «cerrar ayuda» y «cerrar»."""

    def setUp(self) -> None:
        AtriaHelpDialog.CloseHelp()
        # Mock loader para crear una instancia limpia de Browser
        mock_loader = MagicMock()
        mock_loader.IsReady = False
        mock_loader.LoadBaseModuleDict.return_value = {}
        mock_loader.LoadTranslateMap.return_value = {
            "subir": "up_target",
            "ayuda": "help_target",
            "manual": "help_target",
            "cerrar ayuda": "close_help_target",
            "cerrar": "close_help_target",
        }
        mock_loader.LoadModuleDictByName.return_value = {
            "up": "up_target",
            "help": "help_target",
            "close_help": "close_help_target",
            "show_context": "context_target",
        }
        self.browser = Browser(_loader=mock_loader)

    def tearDown(self) -> None:
        AtriaHelpDialog.CloseHelp()

    def test_voice_ayuda_opens_dialog(self) -> None:
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

        res = self.browser.ProcessPhrase("ayuda")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "help")
        self.assertTrue(AtriaHelpDialog.IsHelpOpen())

    def test_voice_manual_opens_dialog(self) -> None:
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

        res = self.browser.ProcessPhrase("manual")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "help")
        self.assertTrue(AtriaHelpDialog.IsHelpOpen())

    def test_voice_cerrar_ayuda_closes_dialog(self) -> None:
        # Abrir primero
        self.browser.ProcessPhrase("ayuda")
        self.assertTrue(AtriaHelpDialog.IsHelpOpen())

        # Cerrar por voz diciendo «cerrar ayuda»
        res = self.browser.ProcessPhrase("cerrar ayuda")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "close_help")
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

    def test_voice_cerrar_closes_dialog_when_open(self) -> None:
        # Abrir primero
        self.browser.ProcessPhrase("manual")
        self.assertTrue(AtriaHelpDialog.IsHelpOpen())

        # Cerrar por voz diciendo simplemente «cerrar»
        res = self.browser.ProcessPhrase("cerrar")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "close_help")
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

    def test_voice_cerrar_ayuda_when_not_open(self) -> None:
        self.assertFalse(AtriaHelpDialog.IsHelpOpen())

        res = self.browser.ProcessPhrase("cerrar ayuda")
        self.assertFalse(res.Success)
        self.assertEqual(res.Action, "close_help")
        self.assertIn("No hay ventana", res.Message)

    def test_spoken_phrases_includes_help_and_close(self) -> None:
        phrases = self.browser.GetSpokenPhrases()
        self.assertIn("ayuda", phrases)
        self.assertIn("manual", phrases)
        self.assertIn("cerrar ayuda", phrases)
        self.assertIn("cerrar", phrases)


if __name__ == "__main__":
    unittest.main()
