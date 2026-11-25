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

        num_tokens = [
            t
            for t in tokens
            if t not in SpokenNumberParser.ConfirmationWords
            and t not in SpokenNumberParser.CancellationWords
            and t != "unk"
        ]
        if num_tokens:
            phrase_part = " ".join(num_tokens)
            self._AccumulatedText = (
                (self._AccumulatedText + " " + phrase_part).strip()
                if self._AccumulatedText
                else phrase_part
            )
            self.SetHeardText(self._AccumulatedText)

        if self._HasConfirmation(tokens):
            phrase = self._AccumulatedText
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

        preview_coords = self._ExtractCoordinates(self._AccumulatedText)
        if preview_coords:
            coord_str = ", ".join(str(c) for c in preview_coords)
            self.SetStatus(f"Coordenadas leídas: ({coord_str}). Decí ok o enviar para confirmar.")
        else:
            self.SetStatus(T(self._Language, "numeric_prompt"))
        return self.GetResult()

    def _OnOkClicked(self) -> None:
        phrase = (getattr(self, "_AccumulatedText", "") or self.GetCurrentText() or "").strip()
        if not phrase:
            self.Fail(T(self._Language, "value_not_empty"))
            return
        coords = self._ExtractCoordinates(phrase)
        if not coords:
            self.Fail(
                "No se detectaron coordenadas válidas. Dictá al menos dos números."
                if self._Language == "es"
                else "No valid coordinates detected. Say at least two numbers."
            )
            return
        self.AcceptValue(coords)

    def AcceptValue(self, Value: Any | None = None) -> PromptResult:
        if isinstance(Value, str):
            coords = self._ExtractCoordinates(Value)
            if not coords:
                return self.Fail(
                    "No se detectaron coordenadas válidas."
                    if self._Language == "es"
                    else "No valid coordinates detected."
                )
            Value = coords
        return super().AcceptValue(Value)

    def _ExtractCoordinates(self, Phrase: str) -> tuple[float, ...] | None:
        """Extract two or three coordinate values from spoken phrase."""
        tokens = SpokenNumberParser.Tokenize(Phrase)
        clean = [
            t
            for t in tokens
            if t not in SpokenNumberParser.ConfirmationWords
            and t not in SpokenNumberParser.CancellationWords
            and t not in ("coord", "coordenada", "coordenadas", "unk")
        ]
        if not clean:
            return None

        merged = SpokenNumberParser._MergeTensAndUnits(clean)
        numbers: list[float] = []
        i = 0
        total = len(merged)
        while i < total:
            token = merged[i]
            sign = 1.0
            if token in SpokenNumberParser.NegativeWords or token == "-":
                sign = -1.0
                i += 1
                if i >= total:
                    break
                token = merged[i]

            val = SpokenNumberParser.TryParseFloat(token)
            if val is None and token in SpokenNumberParser.DigitWords:
                try:
                    val = float(SpokenNumberParser.DigitWords[token])
                except ValueError:
                    val = None

            if val is not None:
                if i + 1 < total and merged[i + 1] in SpokenNumberParser.DecimalWords:
                    if i + 2 < total:
                        dec_token = merged[i + 2]
                        dec_num = SpokenNumberParser.TryParseFloat(dec_token)
                        if dec_num is None and dec_token in SpokenNumberParser.DigitWords:
                            try:
                                dec_num = float(SpokenNumberParser.DigitWords[dec_token])
                            except ValueError:
                                dec_num = None
                        if dec_num is not None:
                            val = float(f"{int(val)}.{int(dec_num)}")
                            i += 2
                numbers.append(sign * val)
            i += 1

        if len(numbers) >= 2:
            return tuple(numbers[:3]) if len(numbers) >= 3 else (numbers[0], numbers[1])
        return None

