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

"""Switches the active Vosk grammar in and out of numeric input mode."""

from __future__ import annotations


class NumericGrammarSwitcher:
    """Swaps the Vosk grammar between CAD navigation and numeric input.

    Kept separate from PromptVoiceRouter: the router's job is tracking which
    prompt is currently active, while grammar switching is a distinct
    responsibility with its own dependencies (AtriaVoiceService, the Numbers
    dictionary, the active Browser adapter).
    """

    @staticmethod
    def ActivateNumericGrammar() -> None:
        """Switch the Vosk grammar to numeric input words for the configured language."""
        try:
            import sys
            from pathlib import Path

            from GUIFreeCad.core.settings import settings
            from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService
            from GUIFreeCad.integration.voice_bootstrap import _resolve_dictionary_root

            dic_root = str(_resolve_dictionary_root())
            if dic_root not in sys.path:
                sys.path.insert(0, dic_root)

            from Numbers.Numbers import get_numeric_grammar_phrases

            phrases = get_numeric_grammar_phrases(settings.language)
            AtriaVoiceService.get().set_grammar(phrases)
        except Exception:
            pass

    @staticmethod
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from GUIFreeCad.integration.browser_voice_adapter import get_active_adapter

            adapter = get_active_adapter()
            if adapter is not None:
                adapter.RestoreGrammar()
        except Exception:
            pass
