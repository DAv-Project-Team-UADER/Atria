# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad AutÃ³noma de Entre RÃ­os (UADER FCYT, sede ConcepciÃ³n del Uruguay)
# Bajo la direcciÃ³n de Ernesto Ledesma
# Encargados: Micaela SaÃ¼l, Tadeo Rochas y Camila ViÃ±eg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los tÃ©rminos de la Licencia PÃºblica General GNU tal como fue publicada
# por la FundaciÃ³n para el Software Libre, en la versiÃ³n 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea Ãºtil,
# pero SIN NINGUNA GARANTÃA; incluso sin la garantÃ­a implÃ­cita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÃ“SITO PARTICULAR. Consulte la
# Licencia PÃºblica General GNU para mÃ¡s detalles.
#
# DeberÃ­as haber recibido una copia de la Licencia PÃºblica General GNU
# junto con este programa. Si no es asÃ­, consulte <http://www.gnu.org/licenses/>.

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

            from core.settings import settings
            from speech.atria_voice_service import AtriaVoiceService
            from integration.voice_bootstrap import _resolve_dictionary_root

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
            from integration.browser_voice_adapter import get_active_adapter

            adapter = get_active_adapter()
            if adapter is not None:
                adapter.RestoreGrammar()
        except Exception:
            pass
