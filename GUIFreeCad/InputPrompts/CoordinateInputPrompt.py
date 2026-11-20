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

"""Coordinate / point input prompt for ATRIA voice-driven diagramming."""

from __future__ import annotations

import re
from typing import Any

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import KindLabel, ResolveLanguage, T


class CoordinateInputPrompt(BaseInputPrompt):
    """Prompt that captures 2D or 3D coordinate pairs / triplets by voice.

    Users can dictate:
    - In Spanish: "diez veinte ok", "cero cero enviar", "cien doscientos cincuenta listo"
    - In English: "ten twenty ok", "zero zero send"
    - In Portuguese: "dez vinte ok", "zero zero enviar"
    Or dictate coordinates one by one and confirm with an acceptance word.
    """

    def __init__(
        self,
        Title: str | None = None,
        Message: str | None = None,
        Parent: Any = None,
        ExpectedDimensions: int = 2,
    ) -> None:
        language = ResolveLanguage()
        self.ExpectedDimensions = ExpectedDimensions
        super().__init__(
            Title or T(language, "param_title", index="coordenadas"),
            Message
            or (
                "Dictá las coordenadas (X, Y) o punto, por ejemplo «diez veinte», y decí ok o enviar."
                if language == "es"
                else (
                    "Say the (X, Y) coordinates, e.g. 'ten twenty', then say ok or send."
                    if language == "en"
                    else "Diga as coordenadas (X, Y), ex: «dez vinte», e depois diga ok ou enviar."
                )
            ),
            Parent,
        )

    def RequiresNumericGrammar(self) -> bool:
        return True

    def ProcessFinalText(self, Text: str) -> PromptResult:
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            self._AccumulatedText = ""
            return self.Cancel()

        if self._HasConfirmation(tokens):
            phrase = self._AccumulatedText or Text
            self._AccumulatedText = ""
            coords = self._ExtractCoordinates(phrase)
            if not coords:
                self.SetStatus(
                    "No se detectaron coordenadas válidas. Dictá al menos dos números."
                    if self._Language == "es"
                    else "No valid coordinates detected. Say at least two numbers."
                )
                return self.GetResult()
            return self.AcceptValue(coords)

        self._AccumulatedText = (
            (self._AccumulatedText + " " + Text).strip() if self._AccumulatedText else Text
        )
        preview_coords = self._ExtractCoordinates(self._AccumulatedText)
        if preview_coords:
            coord_str = ", ".join(str(c) for c in preview_coords)
            self.SetStatus(f"Coordenadas leídas: ({coord_str}). Decí ok o enviar para confirmar.")
        else:
            self.SetStatus(T(self._Language, "numeric_prompt"))
        return self.GetResult()

    def _ExtractCoordinates(self, Phrase: str) -> tuple[float, ...] | None:
        """Extract two or three coordinate values from spoken phrase."""
        tokens = SpokenNumberParser.Tokenize(Phrase)
        clean_tokens = [
            t
            for t in tokens
            if t not in SpokenNumberParser.ConfirmationWords
            and t not in SpokenNumberParser.CancellationWords
            and t not in ("x", "y", "z", "punto", "point", "coord", "coordenada")
        ]
        if not clean_tokens:
            return None

        merged = SpokenNumberParser._MergeTensAndUnits(clean_tokens)
        numbers: list[float] = []

        for token in merged:
            num = SpokenNumberParser.TryParseFloat(token)
            if num is not None:
                numbers.append(num)
            elif token in SpokenNumberParser.DigitWords:
                try:
                    numbers.append(float(SpokenNumberParser.DigitWords[token]))
                except ValueError:
                    pass

        if len(numbers) >= 2:
            return tuple(numbers[:3]) if len(numbers) >= 3 else (numbers[0], numbers[1])
        return None
