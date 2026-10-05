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

"""Single navigable command in Browser.Context / BaseContext."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Any, Callable


def _Normalize(text: str) -> str:
    """Lowercase, collapse spaces and strip accents from a spoken phrase.

    Debe coincidir con DictionaryLoader.NormalizeSpoken: Browser normaliza la
    frase entrante con esa función (que quita acentos vía NFKD) antes de
    buscarla acá. Si acá sólo se hiciera lower(), ninguna clave con tilde o
    eñe ("diseño de pieza", "dibujo técnico", "cuadrícula") matchearía nunca.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " ".join(stripped.lower().split())


@dataclass(frozen=True)
class ContextEntry:
    """Maps a spoken phrase to an internal key and executable target."""

    Spoken: str
    InternalKey: str
    Target: Any

    def IsSubContext(self) -> bool:
        return isinstance(self.Target, dict)

    def IsCallable(self) -> bool:
        return callable(self.Target)

    def NormalizeSpoken(self) -> str:
        return _Normalize(self.Spoken)


def FindBySpoken(entries: list[ContextEntry], spoken: str) -> ContextEntry | None:
    needle = _Normalize(spoken)
    for entry in entries:
        if entry.NormalizeSpoken() == needle:
            return entry
    return None


def FindClosestBySpoken(
    entries: list[ContextEntry], spoken: str, cutoff: float = 0.82
) -> ContextEntry | None:
    """Fuzzy fallback cuando Vosk devuelve palabra similar pero no exacta.

    El modelo small-es confunde terminaciones ('elíptica'/'elíptico',
    'hiperbólica'/'hiperbola') y dígitos vs palabra ('3 puntos'/'tres
    puntos'). Si el match exacto falla, buscamos el entry con mayor
    difflib ratio y lo devolvemos si supera cutoff. Usa la misma
    normalización que FindBySpoken.
    """
    import difflib

    needle = _Normalize(spoken)
    if not needle:
        return None

    best: ContextEntry | None = None
    best_ratio = 0.0
    for entry in entries:
        ratio = difflib.SequenceMatcher(None, needle, entry.NormalizeSpoken()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = entry
    if best is not None and best_ratio >= cutoff:
        return best
    return None


def FindByInternalKey(entries: list[ContextEntry], internal_key: str) -> ContextEntry | None:
    key = internal_key.lower()
    for entry in entries:
        if entry.InternalKey.lower() == key:
            return entry
    return None
