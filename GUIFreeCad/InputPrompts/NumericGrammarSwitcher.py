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

import logging

from InputPrompts.SpokenNumberParser import SpokenNumberParser

log = logging.getLogger("ATRIA.NumericGrammarSwitcher")


class NumericGrammarSwitcher:
    """Swaps the Vosk grammar between CAD navigation and numeric input.

    Restricts Vosk exclusively to numbers, decimal separators, signs,
    and confirmation/cancellation words when an input prompt is awaiting
    parameters. This prevents Vosk from outputting random CAD words or
    hallucinating commands when the user dictates numbers.
    """

    @classmethod
    def GetNumericPhrases(cls, Language: str = "es") -> list[str]:
        """Return a deduplicated, sorted list of all valid spoken numeric phrases."""
        phrases: set[str] = set()

        # 1. Palabras de dígitos y números base (0-19, 20-90, 100-900, 1000)
        for word in SpokenNumberParser.DigitWords.keys():
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.TensWords.keys():
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.HundredsWords.keys():
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.ThousandsWords.keys():
            phrases.add(word.lower().strip())

        # 2. Conectores, decimales y negativos
        for word in SpokenNumberParser.ConnectorWords:
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.DecimalWords:
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.NegativeWords:
            phrases.add(word.lower().strip())

        # 3. Confirmación y cancelación
        for word in SpokenNumberParser.ConfirmationWords:
            phrases.add(word.lower().strip())
        for word in SpokenNumberParser.CancellationWords:
            phrases.add(word.lower().strip())

        # 4. Palabras auxiliares de coordenadas y dimensiones
        for aux in (
            "x",
            "y",
            "z",
            "punto",
            "point",
            "coord",
            "coordenada",
            "coordenadas",
            "milimetro",
            "milimetros",
            "milímetro",
            "milímetros",
            "mm",
            "metro",
            "metros",
            "m",
            "centimetro",
            "centimetros",
            "centímetro",
            "centímetros",
            "cm",
        ):
            phrases.add(aux)

        # 5. Dígitos numéricos directos
        for d in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            phrases.add(d)

        # 6. Compuestos en español (decena + conector + unidad)
        es_tens = ["treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
        es_units = [
            "uno",
            "un",
            "una",
            "dos",
            "tres",
            "cuatro",
            "cinco",
            "seis",
            "siete",
            "ocho",
            "nueve",
        ]
        for ten in es_tens:
            for unit in es_units:
                phrases.add(f"{ten} y {unit}")

        # 7. Compuestos comunes de centenas y miles
        es_hundreds = [
            "cien",
            "ciento",
            "doscientos",
            "trescientos",
            "cuatrocientos",
            "quinientos",
            "seiscientos",
            "setecientos",
            "ochocientos",
            "novecientos",
        ]
        common_subs = [
            "diez",
            "veinte",
            "veinticinco",
            "treinta",
            "cincuenta",
            "cinco mil",
            "dos mil",
        ]
        for h in es_hundreds:
            for sub in common_subs:
                phrases.add(f"{h} {sub}")

        # 8. Combinaciones comunes con confirmación directa (dictado fluido en un solo respiro)
        common_spoken_numbers = [
            "cero",
            "uno",
            "dos",
            "tres",
            "cuatro",
            "cinco",
            "diez",
            "quince",
            "veinte",
            "veinticinco",
            "treinta",
            "cincuenta",
            "cien",
            "ciento cincuenta",
            "doscientos",
            "doscientos cincuenta",
            "quinientos",
            "mil",
            "dos mil",
            "cinco mil",
            "cero cero",
            "diez diez",
            "diez veinte",
            "veinte diez",
            "cero cinco",
        ]
        for num in common_spoken_numbers:
            phrases.add(f"{num} ok")
            phrases.add(f"{num} listo")
            phrases.add(f"{num} enviar")

        # 9. Comodín Vosk
        phrases.add("[unk]")

        return sorted(phrases)

    @staticmethod
    def ActivateNumericGrammar() -> None:
        """Switch the Vosk grammar to numeric input words for the configured language."""
        try:
            from GUIFreeCad.core.settings import settings

            lang = getattr(settings, "language", "es") or "es"
        except Exception:
            lang = "es"

        try:
            from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

            phrases = NumericGrammarSwitcher.GetNumericPhrases(lang)
            AtriaVoiceService.get().set_grammar(phrases)
            log.info("Gramática numérica activada (%d frases)", len(phrases))
        except Exception as exc:
            log.exception("No se pudo activar la gramática numérica: %s", exc)

    @staticmethod
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from GUIFreeCad.integration.browser_voice_adapter import get_active_adapter

            adapter = get_active_adapter()
            if adapter is None:
                from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

                svc = AtriaVoiceService.get()
                adapter = getattr(svc, "_cad_adapter", None)

            if adapter is not None and hasattr(adapter, "RestoreGrammar"):
                adapter.RestoreGrammar()
                log.info("Gramática CAD restaurada vía RestoreGrammar")
            elif adapter is not None:
                browser = getattr(adapter, "_browser", getattr(adapter, "browser", None))
                if browser is not None and hasattr(browser, "GetSpokenPhrases"):
                    from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

                    AtriaVoiceService.get().set_grammar(browser.GetSpokenPhrases())
                    log.info("Gramática CAD restaurada vía Browser.GetSpokenPhrases")
        except Exception as exc:
            log.exception("No se pudo restaurar la gramática CAD: %s", exc)
