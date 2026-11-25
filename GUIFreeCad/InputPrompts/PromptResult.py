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
