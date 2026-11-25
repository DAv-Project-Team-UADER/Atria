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

"""Voice selector for guided examples: retroceder / avanzar / enviar."""

from __future__ import annotations

from InputPrompts.ChoiceInputPrompt import ChoiceInputPrompt
from InputPrompts.ExampleStep import NAVIGATION_WORDS
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


def _AllWords(Kind: str) -> set[str]:
    """Return the navigation words of ``Kind`` in every language, as heard."""
    words = (word for table in NAVIGATION_WORDS.values() for word in table[Kind])
    return {SpokenNumberParser.NormalizeText(word) for word in words}


class ExampleChoiceInputPrompt(ChoiceInputPrompt):
    """Choice prompt that navigates with previous/next and picks with select.

    The words of the options are not spoken: only navigation is heard, so the
    grammar stays small. The accepted value is the key of the example.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # el botón Aceptar entrega el texto visible (el título); el valor es la clave del ejemplo
        self._OkButton.clicked.disconnect()
        self._OkButton.clicked.connect(lambda: self.AcceptValue(self.GetSelectedKey()))

    def GrammarPhrases(self, Language: str) -> list[str]:
        """Return previous, next, select and the cancel words of ``Language``."""
        table = NAVIGATION_WORDS.get(Language, NAVIGATION_WORDS["es"])
        phrases = [*table["previous"], *table["next"], *table["select"]]
        cancel = SpokenNumberParser.CancellationWords
        phrases.extend(
            word
            for word in PlaneGrammarSwitcher.PlanePhrases(Language)
            if SpokenNumberParser.NormalizeText(word) in cancel
        )
        return phrases

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Cancel, move with previous/next or pick the highlighted example."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)
        tokens_set = set(tokens)

        if tokens_set & SpokenNumberParser.CancellationWords:
            return self.Cancel()
        if tokens_set & (_AllWords("previous") | PlaneSelectionInputPrompt.UpWords):
            return self._Move(-1)
        if tokens_set & (_AllWords("next") | PlaneSelectionInputPrompt.DownWords):
            return self._Move(1)
        if tokens_set & _AllWords("select") or self._HasConfirmation(tokens):
            return self.AcceptValue(self.GetSelectedKey())

        self._Refresh()
        return self.GetResult()

    def _Refresh(self) -> None:
        table = NAVIGATION_WORDS.get(self._Language, NAVIGATION_WORDS["es"])
        self.SetHeardText(self._Options[self._CurrentIndex][1])
        self.SetStatus(
            f"({self._CurrentIndex + 1}/{len(self._Options)}) — "
            f"{table['previous'][0]} / {table['next'][0]}, {table['select'][0]}"
        )
