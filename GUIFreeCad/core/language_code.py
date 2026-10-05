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
