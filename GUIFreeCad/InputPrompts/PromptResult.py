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

"""Common result object returned by ATRIA input prompts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PromptResult:
    """Represents the result of a voice-driven input prompt."""

    Success: bool
    Value: Any | None = None
    Cancelled: bool = False
    Error: str = ""

    @classmethod
    def Pending(cls) -> "PromptResult":
        """Build a pending prompt result."""
        return cls(Success=False)

    @classmethod
    def Ok(cls, Value: Any | None = None) -> "PromptResult":
        """Build a successful prompt result."""
        return cls(Success=True, Value=Value)

    @classmethod
    def Cancel(cls) -> "PromptResult":
        """Build a cancelled prompt result."""
        return cls(Success=False, Cancelled=True)

    @classmethod
    def Fail(cls, Error: str) -> "PromptResult":
        """Build a failed prompt result with an error message."""
        return cls(Success=False, Error=Error)
