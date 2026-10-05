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

"""One frame of a guided example and the navigation words shared by its prompts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

# Palabras de navegaciÃ³n por idioma. Las usan el selector de ejemplos y el
# reproductor; ambos aceptan las de los tres idiomas a la vez.
NAVIGATION_WORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "es": {
        "previous": ("retroceder",),
        "next": ("avanzar",),
        "select": ("enviar",),
        "skip": ("saltar",),
    },
    "en": {
        "previous": ("back",),
        "next": ("next",),
        "select": ("send",),
        "skip": ("skip",),
    },
    "pt": {
        "previous": ("voltar",),
        "next": ("prÃ³ximo",),
        "select": ("enviar",),
        "skip": ("pular",),
    },
}

# SinÃ³nimos que el reproductor da por buenos: palabra oÃ­da (sin tildes) -> palabra esperada.
WORD_SYNONYMS: dict[str, str] = {
    "coma": "punto",
}

_DEFAULT_LANGUAGE = "es"


def _Pick(Table: Any, Language: str) -> Any:
    """Return ``Table[Language]`` falling back to Spanish; ``None`` when absent."""
    if not isinstance(Table, dict):
        return Table
    return Table.get(Language, Table.get(_DEFAULT_LANGUAGE))


@dataclass(frozen=True, eq=False)
class ExampleStep:
    """A frame: what to show, what to say to do it in ATRIA, and what to run."""

    Text: dict[str, str]
    Path: dict[str, tuple[str, ...]]
    Action: Callable[[], None]
    Values: Any = None

    def GetText(self, Language: str) -> str:
        """Return the instruction in ``Language`` (Spanish if missing)."""
        return _Pick(self.Text, Language) or ""

    def GetPath(self, Language: str) -> tuple[str, ...]:
        """Return the command-tree phrases in ``Language`` (Spanish if missing)."""
        return tuple(_Pick(self.Path, Language) or ())

    def GetValues(self, Language: str) -> tuple[str, ...]:
        """Return the words dictated in the command dialogs.

        ``Values`` may be a per-language dict or a function ``f(language)``
        evaluated on every call, since it can depend on the document.
        """
        values = self.Values
        if values is None:
            return ()
        if callable(values):
            return tuple(values(Language))
        return tuple(_Pick(values, Language) or ())

    def GetSay(self, Language: str) -> tuple[str, ...]:
        """Return everything to say, in order: path first, then values."""
        return self.GetPath(Language) + self.GetValues(Language)
