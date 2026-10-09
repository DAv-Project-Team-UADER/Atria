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

"""Language codes for ATRIA voice navigation (PascalCase public API)."""

from __future__ import annotations

from enum import Enum


class LanguageCode(Enum):
    """Preference language states (task specification: En, Es, PT)."""

    En = "en"
    Es = "es"
    PT = "pt"

    @classmethod
    def FromStorage(cls, value: str) -> "LanguageCode":
        normalized = (value or "es").strip().lower()
        for item in cls:
            if item.value == normalized:
                return item
        return cls.Es

    @property
    def TranslateModuleSuffix(self) -> str:
        """TraduceTo file stem, e.g. TraduceToEs."""
        if self is LanguageCode.En:
            return "TraduceToEn"
        if self is LanguageCode.PT:
            return "TraduceToPT"
        return "TraduceToEs"

    @property
    def AlternateTranslateSuffixes(self) -> tuple[str, ...]:
        """Fallback stems (some folders use TraduceToPt or TraduceToPtBr)."""
        if self is LanguageCode.PT:
            return ("TraduceToPT", "TraduceToPt", "TraduceToPtBr")
        if self is LanguageCode.En:
            return ("TraduceToEn",)
        return ("TraduceToEs",)
