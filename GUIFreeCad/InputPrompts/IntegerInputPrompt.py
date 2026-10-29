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

"""Integer input prompt for ATRIA voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.NumericInputPrompt import NumericInputPrompt
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import KindLabel, ResolveLanguage, T


class IntegerInputPrompt(NumericInputPrompt):
    """Prompt that captures and validates an integer value."""

    def __init__(
        self,
        Title: str | None = None,
        Message: str | None = None,
        Parent=None,
    ) -> None:
        language = ResolveLanguage()
        super().__init__(
            Title or T(language, "param_title", index="int"),
            Message or T(language, "param_message", kind=KindLabel(language, "int"), name="sides"),
            Parent,
        )

    def _ParseAccumulatedText(self, Text: str) -> int:
        return SpokenNumberParser.ParseInteger(Text)
