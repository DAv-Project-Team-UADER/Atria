"""ATRIA preferences facade (SetLanguage public API for Browser)."""

from __future__ import annotations

from typing import Callable, Any

from GUIFreeCad.core.language_code import LanguageCode
from GUIFreeCad.core.settings import settings

LanguageChangeCallback = Callable[[LanguageCode, LanguageCode], None]


class Preferences:
    """
    Public preferences surface used by Browser and the FreeCAD GUI.
    """

    def __init__(self) -> None:
        self._language_callbacks: list[LanguageChangeCallback] = []
        settings.load()

    @property
    def SetLanguage(self) -> LanguageCode:
        return LanguageCode.FromStorage(settings.language)

    @SetLanguage.setter
    def SetLanguage(self, value: Any) -> None:
        # Extraemos el texto base (ej: 'es') para evitar el problema de los imports dobles
        if hasattr(value, "value"):
            lang_str = str(value.value)
        elif isinstance(value, str):
            lang_str = value
        else:
            raise TypeError("SetLanguage must be LanguageCode or a valid string")
            
        # Forzamos la creación usando la clase LanguageCode local
        nuevo_idioma = LanguageCode.FromStorage(lang_str)
        idioma_previo = self.SetLanguage
        
        settings.language = nuevo_idioma.value
        settings.save()
        
        # Comparamos los valores de texto en lugar de los objetos de memoria
        if idioma_previo.value != nuevo_idioma.value:
            for callback in list(self._language_callbacks):
                callback(idioma_previo, nuevo_idioma)

    def RegisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        self._language_callbacks.append(callback)

    def UnregisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        try:
            self._language_callbacks.remove(callback)
        except ValueError:
            pass


preferences = Preferences()