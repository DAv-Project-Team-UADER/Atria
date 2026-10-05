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

"""Voice-driven selector for one option among a few named ones."""

from __future__ import annotations

from typing import Iterable

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class ChoiceInputPrompt(BaseInputPrompt):
    """Pick one option: say its name, or browse with up/down and confirm.

    ``Options`` is a list of ``(key, visible text, words that pick it)``. The
    accepted value is the key of the chosen option.
    """

    def __init__(
        self,
        Options: list[tuple[str, str, Iterable[str]]],
        Title: str = "ATRIA Choice",
        Message: str = "ElegÃ­ una opciÃ³n",
        Parent=None,
    ) -> None:
        if not Options:
            raise ValueError("ChoiceInputPrompt needs at least one option")
        super().__init__(Title, Message, Parent)
        self._Options = [(key, label, tuple(words)) for key, label, words in Options]
        self._OptionWords = [self._Normalized(words) for _key, _label, words in self._Options]
        self._CurrentIndex = 0
        self._Refresh()

    @staticmethod
    def _Normalized(Words: Iterable[str]) -> set[str]:
        """Return the words as they look once heard (no accents, lowercase)."""
        normalized = (SpokenNumberParser.NormalizeText(word).strip() for word in Words)
        return {word for word in normalized if word}

    def GrammarPhrases(self, Language: str) -> list[str]:
        """Return the Vosk phrases: navigation, confirm, cancel and option words."""
        phrases = PlaneGrammarSwitcher.PlanePhrases(Language)
        for _key, _label, words in self._Options:
            phrases.extend(word for word in words if word not in phrases)
        return phrases

    def GetSelectedKey(self) -> str:
        """Return the key of the highlighted option."""
        return self._Options[self._CurrentIndex][0]

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Cancel, pick by name, move with up/down or confirm the highlighted one."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)
        tokens_set = set(tokens)

        if tokens_set & SpokenNumberParser.CancellationWords:
            return self.Cancel()

        spoken = f" {' '.join(tokens)} "
        for index, words in enumerate(self._OptionWords):
            if any(f" {word} " in spoken for word in words):
                self._CurrentIndex = index
                return self.AcceptValue(self.GetSelectedKey())

        if tokens_set & PlaneSelectionInputPrompt.DownWords:
            return self._Move(1)
        if tokens_set & PlaneSelectionInputPrompt.UpWords:
            return self._Move(-1)
        if self._HasConfirmation(tokens):
            return self.AcceptValue(self.GetSelectedKey())

        self._Refresh()
        return self.GetResult()

    def _Move(self, Direction: int) -> PromptResult:
        self._Step(Direction)
        self._Result = PromptResult.Pending()
        self._Refresh()
        return self.GetResult()

    def _Step(self, Direction: int) -> None:
        self._CurrentIndex = (self._CurrentIndex + Direction) % len(self._Options)

    def _Refresh(self) -> None:
        self.SetHeardText(self._Options[self._CurrentIndex][1])
        self.SetStatus(
            f"({self._CurrentIndex + 1}/{len(self._Options)})"
            " â€” arriba/abajo, okey/enviar, cancelar."
        )
