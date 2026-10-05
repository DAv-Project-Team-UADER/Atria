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

"""ATRIA preferences facade (SetLanguage public API for Browser)."""

from __future__ import annotations

from typing import Callable

from core.language_code import LanguageCode
from core.settings import settings

LanguageChangeCallback = Callable[[LanguageCode, LanguageCode], None]


class Preferences:
    """
    Public preferences surface used by Browser and the FreeCAD GUI.

    SetLanguage may be En, Es, or PT; changing it notifies registered listeners
    (Browser should reload commands from base.py).
    """

    def __init__(self) -> None:
        self._language_callbacks: list[LanguageChangeCallback] = []
        settings.load()

    @property
    def SetLanguage(self) -> LanguageCode:
        return LanguageCode.FromStorage(settings.language)

    @SetLanguage.setter
    def SetLanguage(self, value: LanguageCode) -> None:
        if not isinstance(value, LanguageCode):
            raise TypeError("SetLanguage must be LanguageCode (En, Es, or PT)")
        previous = self.SetLanguage
        settings.language = value.value
        settings.save()
        if previous is not value:
            for callback in list(self._language_callbacks):
                callback(previous, value)

    def RegisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        self._language_callbacks.append(callback)

    def UnregisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        try:
            self._language_callbacks.remove(callback)
        except ValueError:
            pass


preferences = Preferences()
