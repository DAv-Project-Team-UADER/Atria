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

"""Shared base for prompts that accumulate spoken digits before parsing."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import T


class NumericInputPrompt(BaseInputPrompt):
    """Template for prompts that collect a number across several utterances.

    Concrete prompts (Integer, Float) only implement `_ParseAccumulatedText`;
    the accumulate/confirm/cancel voice flow lives here so a new numeric
    prompt type does not need to copy it.
    """

    def RequiresNumericGrammar(self) -> bool:
        return True

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accumulate spoken text and parse it once a confirmation word arrives.

        Supports both single-utterance dictation ("diez ok", "ciento cincuenta listo")
        and multi-utterance dictation ("diez" followed by "ok" in separate phrases).
        """
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            self._AccumulatedText = ""
            return self.Cancel()

        # Separate tokens that are not confirmation words
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
            if not self._AccumulatedText:
                self.SetStatus(T(self._Language, "numeric_no_value"))
                return self.GetResult()
            parse_text = self._AccumulatedText
            self._AccumulatedText = ""
            try:
                value = self._ParseAccumulatedText(parse_text)
            except ValueError as error:
                return self.Fail(str(error))
            return self.AcceptValue(value)

        self.SetStatus(T(self._Language, "numeric_prompt"))
        return self.GetResult()

    def _OnOkClicked(self) -> None:
        text = (getattr(self, "_AccumulatedText", "") or self.GetCurrentText() or "").strip()
        if not text:
            self.Fail(T(self._Language, "numeric_no_value"))
            return
        try:
            value = self._ParseAccumulatedText(text)
        except ValueError as error:
            self.Fail(str(error))
            return
        self.AcceptValue(value)

    def AcceptValue(self, Value: Any | None = None) -> PromptResult:
        if isinstance(Value, str):
            trimmed = Value.strip()
            if not trimmed:
                return self.Fail(T(self._Language, "value_not_empty"))
            try:
                Value = self._ParseAccumulatedText(trimmed)
            except ValueError as error:
                return self.Fail(str(error))
        return super().AcceptValue(Value)

    def _ParseAccumulatedText(self, Text: str):
        """Parse the accumulated spoken text into a numeric value.

        Subclasses must override this to return their concrete numeric type.
        """
        raise NotImplementedError
