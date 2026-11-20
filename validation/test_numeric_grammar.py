# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Unit tests for NumericGrammarSwitcher and numeric-only Vosk grammar restricting."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = ROOT / "GUIFreeCad"
VAL_PATH = ROOT / "validation"
DIC_PATH = ROOT / "dictionary"

for p in (ROOT, GUI_PATH, VAL_PATH, DIC_PATH):
    text = str(p)
    if text not in sys.path:
        sys.path.insert(0, text)

from GUIFreeCad.InputPrompts.CoordinateInputPrompt import CoordinateInputPrompt
from GUIFreeCad.InputPrompts.FloatInputPrompt import FloatInputPrompt
from GUIFreeCad.InputPrompts.IntegerInputPrompt import IntegerInputPrompt
from GUIFreeCad.InputPrompts.NumericGrammarSwitcher import NumericGrammarSwitcher
from GUIFreeCad.InputPrompts.NumericInputPrompt import NumericInputPrompt
from GUIFreeCad.InputPrompts.PromptVoiceRouter import PromptVoiceRouter
from Numbers.Numbers import get_numeric_grammar_phrases


class TestNumericGrammar(unittest.TestCase):
    def test_numeric_phrases_generation(self) -> None:
        phrases = NumericGrammarSwitcher.GetNumericPhrases("es")
        self.assertIsInstance(phrases, list)
        self.assertIn("[unk]", phrases)
        self.assertIn("cero", phrases)
        self.assertIn("diez", phrases)
        self.assertIn("veinte", phrases)
        self.assertIn("cien", phrases)
        self.assertIn("mil", phrases)
        self.assertIn("punto", phrases)
        self.assertIn("coma", phrases)
        self.assertIn("menos", phrases)
        self.assertIn("ok", phrases)
        self.assertIn("listo", phrases)
        self.assertIn("enviar", phrases)
        self.assertIn("cancelar", phrases)
        # Verify compound phrases
        self.assertIn("treinta y cinco", phrases)
        self.assertIn("ciento cincuenta", phrases)
        self.assertIn("diez ok", phrases)
        self.assertIn("cien ok", phrases)

    def test_numbers_numbers_module_interoperability(self) -> None:
        phrases = get_numeric_grammar_phrases("es")
        self.assertIsInstance(phrases, list)
        self.assertIn("diez", phrases)
        self.assertIn("[unk]", phrases)

    def test_prompt_classes_require_numeric_grammar(self) -> None:
        int_prompt = IntegerInputPrompt()
        float_prompt = FloatInputPrompt()
        coord_prompt = CoordinateInputPrompt()

        self.assertTrue(int_prompt.RequiresNumericGrammar())
        self.assertTrue(float_prompt.RequiresNumericGrammar())
        self.assertTrue(coord_prompt.RequiresNumericGrammar())

    def test_prompt_voice_router_activates_and_restores_grammar(self) -> None:
        # Mock AtriaVoiceService and BrowserVoiceAdapter
        mock_svc = MagicMock()
        mock_adapter = MagicMock()

        import GUIFreeCad.speech.atria_voice_service as avs
        import GUIFreeCad.integration.browser_voice_adapter as bva

        original_get = getattr(avs.AtriaVoiceService, "get", None)
        original_adapter = getattr(bva, "_ActiveAdapter", None)

        try:
            avs.AtriaVoiceService.get = staticmethod(lambda: mock_svc)
            bva._ActiveAdapter = mock_adapter

            prompt = FloatInputPrompt()

            # When prompt becomes active, numeric grammar must be activated
            PromptVoiceRouter.SetActivePrompt(prompt)
            mock_svc.set_grammar.assert_called()
            called_phrases = mock_svc.set_grammar.call_args[0][0]
            self.assertIn("diez", called_phrases)
            self.assertIn("[unk]", called_phrases)

            # When prompt clears, CAD grammar must be restored
            PromptVoiceRouter.ClearActivePrompt(prompt)
            mock_adapter.RestoreGrammar.assert_called_once()
        finally:
            if original_get is not None:
                avs.AtriaVoiceService.get = original_get
            bva._ActiveAdapter = original_adapter

    def test_numeric_input_prompt_single_utterance_with_confirmation(self) -> None:
        prompt = FloatInputPrompt()
        res = prompt.ProcessFinalText("diez ok")
        self.assertTrue(res.Success)
        self.assertEqual(res.Value, 10.0)

        prompt2 = FloatInputPrompt()
        res2 = prompt2.ProcessFinalText("ciento cincuenta listo")
        self.assertTrue(res2.Success)
        self.assertEqual(res2.Value, 150.0)

        prompt3 = IntegerInputPrompt()
        res3 = prompt3.ProcessFinalText("veinticinco enviar")
        self.assertTrue(res3.Success)
        self.assertEqual(res3.Value, 25)

    def test_coordinate_input_prompt_single_utterance_with_confirmation(self) -> None:
        prompt = CoordinateInputPrompt()
        res = prompt.ProcessFinalText("diez veinte ok")
        self.assertTrue(res.Success)
        self.assertEqual(res.Value, (10.0, 20.0))

        prompt2 = CoordinateInputPrompt()
        res2 = prompt2.ProcessFinalText("menos diez veinte listo")
        self.assertTrue(res2.Success)
        self.assertEqual(res2.Value, (-10.0, 20.0))

        prompt3 = CoordinateInputPrompt()
        res3 = prompt3.ProcessFinalText("diez punto cinco veinte punto cinco ok")
        self.assertTrue(res3.Success)
        self.assertEqual(res3.Value, (10.5, 20.5))

    def test_coordinate_input_prompt_multi_utterance_dictation(self) -> None:
        prompt = CoordinateInputPrompt()
        # First utterance: user dictates X
        p1 = prompt.ProcessFinalText("cien")
        self.assertFalse(p1.Success)  # Not confirmed yet
        # Second utterance: user dictates Y and confirms
        p2 = prompt.ProcessFinalText("doscientos ok")
        self.assertTrue(p2.Success)
        self.assertEqual(p2.Value, (100.0, 200.0))

    def test_intuitive_buttons_in_base_input_prompt(self) -> None:
        prompt = FloatInputPrompt()
        self.assertTrue(prompt._OkButton.text().startswith("✓"))
        self.assertTrue(prompt._CancelButton.text().startswith("✕"))


if __name__ == "__main__":
    unittest.main()

