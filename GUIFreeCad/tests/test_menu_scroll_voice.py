"""Tests for voice navigation of the panel's horizontal button area."""

from __future__ import annotations

import json
import sys
import types
import unittest
from types import SimpleNamespace
from unittest import mock


class _FakeBrowser:
    def __init__(self, language: str = "es") -> None:
        self.SetLanguage = SimpleNamespace(value=language)
        self.ProcessPhrase = mock.Mock()
        self.GetSpokenPhrases = lambda: ["abrir"]
        self.GetNavWords = lambda action: (
            {"enviar", "send"} if action == "send" else {"cancelar", "cancel"}
        )


class TestMenuScrollVoiceCommands(unittest.TestCase):
    def setUp(self) -> None:
        from GUIFreeCad.integration import browser_voice_adapter

        self.module = browser_voice_adapter

    def test_scroll_phrases_are_in_voice_grammar(self) -> None:
        adapter = self.module.BrowserVoiceAdapter
        browser = _FakeBrowser()
        service = mock.Mock()
        voice_module = types.ModuleType("GUIFreeCad.speech.atria_voice_service")
        voice_module.AtriaVoiceService = SimpleNamespace(get=lambda: service)

        with mock.patch.dict(
            sys.modules,
            {"GUIFreeCad.speech.atria_voice_service": voice_module},
        ):
            instance = adapter(browser)

        grammar = service.set_grammar.call_args.args[0]
        self.assertIn("desplazar menu a la derecha", grammar)
        self.assertIn("menu derecha", grammar)
        self.assertIn("scroll menu left", grammar)
        self.assertIn("scroll menu left enviar", grammar)

    def test_spanish_and_english_scroll_phrases_reach_panel(self) -> None:
        source = mock.Mock()
        source.ScrollMenu.return_value = True
        dock_module = types.ModuleType("GUIFreeCad.integration.atria_dock_panel")
        dock_module.get_source = lambda: source
        bridge_module = types.ModuleType("GUIFreeCad.integration.freecad_gui_bridge")
        bridge_module.run_on_main_thread = lambda callback: callback()

        cases = (
            (_FakeBrowser("es"), "menú derecha", "right"),
            (_FakeBrowser("en"), "menu left send", "left"),
        )
        with (
            mock.patch.object(self.module.BrowserVoiceAdapter, "_update_grammar"),
            mock.patch.object(self.module.BrowserVoiceAdapter, "_publish_line"),
            mock.patch.object(self.module, "append_voice_history"),
            mock.patch.dict(
                sys.modules,
                {
                    "GUIFreeCad.integration.atria_dock_panel": dock_module,
                    "GUIFreeCad.integration.freecad_gui_bridge": bridge_module,
                },
            ),
        ):
            for browser, phrase, direction in cases:
                adapter = self.module.BrowserVoiceAdapter(browser)
                adapter.procesar_frase_final(phrase)
                source.ScrollMenu.assert_called_with(direction)
                browser.ProcessPhrase.assert_not_called()

    def test_service_start_and_resume_keep_adapter_scroll_phrases(self) -> None:
        from GUIFreeCad.core.settings import settings
        from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

        service = AtriaVoiceService()
        with mock.patch.object(AtriaVoiceService, "get", return_value=service):
            adapter = self.module.BrowserVoiceAdapter(_FakeBrowser())

        def latest_grammar() -> list[str]:
            return json.loads(service._grammar_queue.queue[-1])

        with (
            mock.patch.object(settings, "load"),
            mock.patch.object(service, "_ensure_mic", return_value=True),
            mock.patch.object(AtriaVoiceService, "get", return_value=service),
        ):
            service.start_cad(adapter)
            self.assertIn("desplazar menu a la derecha", latest_grammar())

            service._running = True
            service._thread = SimpleNamespace(is_alive=lambda: True)
            service.resume_cad_voice()
            self.assertIn("desplazar menu a la derecha", latest_grammar())


class TestAtriaPanelMenuScroll(unittest.TestCase):
    def test_scroll_menu_moves_a_page_and_stops_at_edges(self) -> None:
        try:
            from GUIFreeCad.ui.AtriaPanel import AtriaPanel
        except ImportError:
            self.skipTest("PySide6 is not available in test runner")

        class Scrollbar:
            def __init__(self) -> None:
                self.current = 100
                self.maximum = 600

            def value(self) -> int:
                return self.current

            def pageStep(self) -> int:
                return 250

            def setValue(self, value: int) -> None:
                self.current = max(0, min(value, self.maximum))

        scrollbar = Scrollbar()
        panel = SimpleNamespace(
            _toolScroll=SimpleNamespace(horizontalScrollBar=lambda: scrollbar),
            BUTTON_WIDTH=74,
        )

        self.assertTrue(AtriaPanel.ScrollMenu(panel, "right"))
        self.assertEqual(scrollbar.value(), 350)
        self.assertTrue(AtriaPanel.ScrollMenu(panel, "left"))
        self.assertEqual(scrollbar.value(), 100)

        scrollbar.current = scrollbar.maximum
        self.assertFalse(AtriaPanel.ScrollMenu(panel, "right"))


if __name__ == "__main__":
    unittest.main()
