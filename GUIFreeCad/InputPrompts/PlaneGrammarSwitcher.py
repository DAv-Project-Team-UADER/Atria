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

"""Switches the active Vosk grammar in and out of plane-selection mode.

El selector de plano (``PlaneSelectionInputPrompt``) solo necesita que Vosk
escuche un puñado de palabras (arriba/abajo/okey/cancelar). Sin esto, el
modelo abierto confunde "abajo" con "trabajo" y otros falsos positivos del
vocabulario completo. Al activarse se acota la gramática a esas frases, y al
cerrarse se restaura la gramática del contexto CAD.
"""

from __future__ import annotations


# Frases mínimas por idioma para navegar el selector de plano. Se mantienen
# deliberadamente chicas (es el punto de acotar): arriba/abajo para mover el
# eje, y un abanico de sinónimos de confirmación/cancelación para que el
# usuario pueda decir "okey", "enviar", "listo", "vale", etc. sin tener que
# recordar una sola palabra. Toda palabra aquí debe existir también en
# NavCommands/TraduceTo*.py o SpokenNumberParser, de modo que el prompt la
# reconozca al llegar el texto final.
_PLANE_PHRASES: dict[str, list[str]] = {
    "es": [
        "arriba", "abajo",
        # confirmación — incluye "okey" pedido explícitamente + sinónimos de NavCommands
        "okey", "okay", "ok", "enviar", "aceptar", "confirmar", "entrar",
        "listo", "vale", "hecho", "dale", "si", "sí", "bueno",
        # cancelación
        "cancelar", "cancela", "descartar", "anular", "abortar", "no",
        "olvidalo", "olvidálo",
    ],
    "en": [
        "up", "down",
        "okey", "okay", "ok", "send", "enter", "accept", "confirm",
        "done", "yes", "yep",
        "cancel", "discard", "abort", "no", "never mind",
    ],
    "pt": [
        "cima", "abaixo",
        "okey", "okay", "ok", "enviar", "aceitar", "confirmar", "entrar",
        "pronto", "feito", "sim",
        "cancelar", "cancelamento", "descartar", "anular", "abortar", "nao", "nÃ£o",
    ],
}


class PlaneGrammarSwitcher:
    """Restricts Vosk grammar to the sketch plane selection words."""

    @staticmethod
    def PlanePhrases(Language: str = "es") -> list[str]:
        """Return the plane-selection phrases for ``Language`` ("es"/"en"/"pt")."""
        return list(_PLANE_PHRASES.get(Language, _PLANE_PHRASES["es"]))

    @staticmethod
    def CurrentLanguage() -> str:
        """Return the configured ATRIA language ("es"/"en"/"pt"), "es" if unknown."""
        try:
            from GUIFreeCad.core.settings import settings

            return str(settings.language)
        except Exception:
            return "es"

    @staticmethod
    def ActivateGrammar(Phrases: list[str]) -> None:
        """Restrict the Vosk grammar to ``Phrases`` (used by any restricted prompt)."""
        try:
            from GUIFreeCad.speech.atria_voice_service import AtriaVoiceService

            AtriaVoiceService.get().set_grammar(Phrases)
        except Exception:
            # Sin gramática acotada el reconocimiento sigue andando, solo con
            # el vocabulario abierto: se nota, no se derriba el selector.
            pass

    @staticmethod
    def ActivatePlaneGrammar() -> None:
        """Restrict the Vosk grammar to the plane-selection words."""
        PlaneGrammarSwitcher.ActivateGrammar(
            PlaneGrammarSwitcher.PlanePhrases(PlaneGrammarSwitcher.CurrentLanguage())
        )

    @staticmethod
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from InputPrompts.NumericGrammarSwitcher import NumericGrammarSwitcher

            NumericGrammarSwitcher.RestoreCadGrammar()
        except Exception:
            pass
