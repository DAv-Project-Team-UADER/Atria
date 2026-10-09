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

"""Localized strings and live language resolution for ATRIA input prompts.

The prompt windows must speak the same language selected in ATRIA options
(``core.preferences`` â†’ ``SetLanguage``). The executor thread passes that
language to the collector, and here every prompt resolves it at construction
time so buttons, status lines and messages follow the configured language.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_ES = "es"
_EN = "en"
_PT = "pt"


def _Normalize(value: Any) -> str:
    """Map any stored language value to es/en/pt, defaulting to es."""
    text = str(value or _ES).strip().lower()
    if "en" in text:
        return _EN
    if "pt" in text:
        return _PT
    return _ES


def ResolveLanguage() -> str:
    """Return the language configured in ATRIA options.

    Reads ``preferences.SetLanguage`` from GUIFreeCad (the same value the
    Browser and the object Tagger use). When that package cannot be imported
    the language is searched walking up to the folder that contains
    ``core/preferences.py``; the final fallback is Spanish.

    Returns:
        One of ``"es"``, ``"en"``, ``"pt"``.
    """
    try:
        from core.preferences import preferences

        return _Normalize(getattr(preferences.SetLanguage, "value", preferences.SetLanguage))
    except Exception:
        pass

    env = os.environ.get("ATRIA_GUI_FREECAD_ROOT", "").strip()
    candidates = (Path(env),) if env and Path(env).is_dir() else tuple(
        Path(__file__).resolve().parents
    )

    for gui_root in candidates:
        if not (gui_root / "core" / "preferences.py").is_file():
            continue
        gui_text = str(gui_root)
        if gui_text not in sys.path:
            sys.path.insert(0, gui_text)
        try:
            from core.preferences import preferences

            return _Normalize(
                getattr(preferences.SetLanguage, "value", preferences.SetLanguage)
            )
        except Exception:
            continue

    return _ES


_LABELS: dict[str, dict[str, str]] = {
    _EN: {
        "listening": "Listening...",
        "accepted": "Accepted",
        "cancelled": "Cancelled",
        "ok": "OK",
        "cancel": "Cancel",
        "value_not_empty": "Value cannot be empty.",
        "numeric_no_value": "No value to confirm. Say a number first.",
        "numeric_prompt": "Say a number, then say ok or send.",
        "string_waiting": "Waiting for enter or send...",
        "string_not_empty": "Text value cannot be empty.",
        "object_unavailable": "Object selection is not available: {error}",
        "object_no_doc": "No active FreeCAD document.",
        "object_no_objects": "The active FreeCAD document has no objects.",
        "object_browse_confirm": "Say advance to browse objects, then enter or send to confirm.",
        "object_browse": "Say advance to browse, or enter/send to confirm.",
        "object_select_error": "Could not select object: {error}",
        "object_selected": "Selected {name} ({current}/{total}).",
        "object_none": "No object is currently selected.",
        "param_title": "ATRIA Parameter {index}",
        "param_message": "Say the {kind} value for '{name}', then say enter or send.",
        "kind_float": "float",
        "kind_int": "integer",
        "kind_str": "text",
        "kind_object": "object",
    },
    _ES: {
        "listening": "Escuchando...",
        "accepted": "Aceptado",
        "cancelled": "Cancelado",
        "ok": "Aceptar",
        "cancel": "Cancelar",
        "value_not_empty": "El valor no puede estar vacÃ­o.",
        "numeric_no_value": "No hay un nÃºmero para confirmar. DecÃ­ un nÃºmero primero.",
        "numeric_prompt": "DecÃ­ un nÃºmero y luego decÃ­ ok o enviar.",
        "string_waiting": "Esperando okey o enviar...",
        "string_not_empty": "El texto no puede estar vacÃ­o.",
        "object_unavailable": "La selecciÃ³n de objetos no estÃ¡ disponible: {error}",
        "object_no_doc": "No hay documento activo de FreeCAD.",
        "object_no_objects": "El documento activo de FreeCAD no tiene objetos.",
        "object_browse_confirm": "DecÃ­ avanzar para recorrer objetos, luego decÃ­ enviar para confirmar.",
        "object_browse": "DecÃ­ avanzar para recorrer, o decÃ­ enviar para confirmar.",
        "object_select_error": "No se pudo seleccionar el objeto: {error}",
        "object_selected": "Seleccionado {name} ({current}/{total}).",
        "object_none": "No hay ningÃºn objeto seleccionado.",
        "param_title": "ATRIA ParÃ¡metro {index}",
        "param_message": "DecÃ­ el {kind} para '{name}' y luego decÃ­ enviar.",
        "kind_float": "nÃºmero decimal",
        "kind_int": "nÃºmero entero",
        "kind_str": "texto",
        "kind_object": "objeto del documento",
    },
    _PT: {
        "listening": "Ouvindo...",
        "accepted": "Aceito",
        "cancelled": "Cancelado",
        "ok": "OK",
        "cancel": "Cancelar",
        "value_not_empty": "O valor nÃ£o pode estar vazio.",
        "numeric_no_value": "NÃ£o hÃ¡ nÃºmero para confirmar. Diga um nÃºmero primeiro.",
        "numeric_prompt": "Diga um nÃºmero e depois diga ok ou enviar.",
        "string_waiting": "Aguardando enviar ou aceitar...",
        "string_not_empty": "O texto nÃ£o pode estar vazio.",
        "object_unavailable": "A seleÃ§Ã£o de objetos nÃ£o estÃ¡ disponÃ­vel: {error}",
        "object_no_doc": "NÃ£o hÃ¡ documento ativo no FreeCAD.",
        "object_no_objects": "O documento ativo do FreeCAD nÃ£o tem objetos.",
        "object_browse_confirm": "Diga prÃ³ximo para percorrer objetos e depois diga enviar para confirmar.",
        "object_browse": "Diga prÃ³ximo para percorrer, ou diga enviar para confirmar.",
        "object_select_error": "NÃ£o foi possÃ­vel selecionar o objeto: {error}",
        "object_selected": "Selecionado {name} ({current}/{total}).",
        "object_none": "Nenhum objeto estÃ¡ selecionado.",
        "param_title": "ATRIA ParÃ¢metro {index}",
        "param_message": "Diga o {kind} para '{name}' e depois diga enviar.",
        "kind_float": "nÃºmero decimal",
        "kind_int": "nÃºmero inteiro",
        "kind_str": "texto",
        "kind_object": "objeto do documento",
    },
}


def T(language: str, key: str, **kwargs: Any) -> str:
    """Return the localized string for ``key`` filling ``**kwargs``.

    Unsupported languages and missing keys fall back to Spanish and to the
    key itself respectively, so a translation gap never raises.
    """
    table = _LABELS.get(_Normalize(language), _LABELS[_ES])
    template = table.get(key, key)
    return template.format(**kwargs) if kwargs else template


def KindLabel(language: str, kind: str) -> str:
    """Return the localized label of a parameter kind (int/float/str/object)."""
    return T(language, f"kind_{kind}")