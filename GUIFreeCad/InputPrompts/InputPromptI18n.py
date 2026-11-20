#  Copyright (C) 2026 The ATRIA Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Localized strings and live language resolution for ATRIA input prompts.

The prompt windows must speak the same language selected in ATRIA options
(``core.preferences`` → ``SetLanguage``). The executor thread passes that
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
        "object_search_title": "Search by spelling",
        "object_search_message": "Spell the object's name, letter by letter",
        "object_search_none": "Nothing looks like \"{text}\". Say search by spelling to try again.",
        "object_search_found": "Closest to \"{text}\": {name} ({current}/{total}).{others} Say send to pick it.",
        "object_search_others": " Also: {names}.",
        "param_title": "ATRIA Parameter {index}",
        "param_message": "Say the {kind} value for '{name}', then say enter or send.",
        "kind_float": "float",
        "kind_coord": "coordinates (X, Y)",
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
        "value_not_empty": "El valor no puede estar vacío.",
        "numeric_no_value": "No hay un número para confirmar. Decí un número primero.",
        "numeric_prompt": "Decí un número y luego decí ok o enviar.",
        "string_waiting": "Esperando okey o enviar...",
        "string_not_empty": "El texto no puede estar vacío.",
        "object_unavailable": "La selección de objetos no está disponible: {error}",
        "object_no_doc": "No hay documento activo de FreeCAD.",
        "object_no_objects": "El documento activo de FreeCAD no tiene objetos.",
        "object_browse_confirm": "Decí avanzar para recorrer objetos, luego decí enviar para confirmar.",
        "object_browse": "Decí avanzar para recorrer, o decí enviar para confirmar.",
        "object_select_error": "No se pudo seleccionar el objeto: {error}",
        "object_selected": "Seleccionado {name} ({current}/{total}).",
        "object_none": "No hay ningún objeto seleccionado.",
        "object_search_title": "Buscar por deletreo",
        "object_search_message": "Deletreá el nombre del objeto, letra por letra",
        "object_search_none": "Nada se parece a \"{text}\". Decí buscar por deletreo para probar de nuevo.",
        "object_search_found": "Lo más parecido a \"{text}\": {name} ({current}/{total}).{others} Decí enviar para elegirlo.",
        "object_search_others": " También: {names}.",
        "param_title": "ATRIA Parámetro {index}",
        "param_message": "Decí el {kind} para '{name}' y luego decí enviar.",
        "kind_float": "número decimal",
        "kind_coord": "coordenadas (X, Y)",
        "kind_int": "número entero",
        "kind_str": "texto",
        "kind_object": "objeto del documento",
    },
    _PT: {
        "listening": "Ouvindo...",
        "accepted": "Aceito",
        "cancelled": "Cancelado",
        "ok": "OK",
        "cancel": "Cancelar",
        "value_not_empty": "O valor não pode estar vazio.",
        "numeric_no_value": "Não há número para confirmar. Diga um número primeiro.",
        "numeric_prompt": "Diga um número e depois diga ok ou enviar.",
        "string_waiting": "Aguardando enviar ou aceitar...",
        "string_not_empty": "O texto não pode estar vazio.",
        "object_unavailable": "A seleção de objetos não está disponível: {error}",
        "object_no_doc": "Não há documento ativo no FreeCAD.",
        "object_no_objects": "O documento ativo do FreeCAD não tem objetos.",
        "object_browse_confirm": "Diga próximo para percorrer objetos e depois diga enviar para confirmar.",
        "object_browse": "Diga próximo para percorrer, ou diga enviar para confirmar.",
        "object_select_error": "Não foi possível selecionar o objeto: {error}",
        "object_selected": "Selecionado {name} ({current}/{total}).",
        "object_none": "Nenhum objeto está selecionado.",
        "object_search_title": "Buscar por soletração",
        "object_search_message": "Soletre o nome do objeto, letra por letra",
        "object_search_none": "Nada se parece com \"{text}\". Diga buscar por soletração para tentar de novo.",
        "object_search_found": "O mais parecido com \"{text}\": {name} ({current}/{total}).{others} Diga enviar para escolhê-lo.",
        "object_search_others": " Também: {names}.",
        "param_title": "ATRIA Parâmetro {index}",
        "param_message": "Diga o {kind} para '{name}' e depois diga enviar.",
        "kind_float": "número decimal",
        "kind_coord": "coordenadas (X, Y)",
        "kind_int": "número inteiro",
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


_FRIENDLY_NAMES: dict[str, dict[str, str]] = {
    _ES: {
        "x1": "Coordenada X inicial",
        "y1": "Coordenada Y inicial",
        "z1": "Coordenada Z inicial",
        "x2": "Coordenada X final",
        "y2": "Coordenada Y final",
        "z2": "Coordenada Z final",
        "x3": "Coordenada X punto 3",
        "y3": "Coordenada Y punto 3",
        "x": "Coordenada X",
        "y": "Coordenada Y",
        "z": "Coordenada Z",
        "center_x": "Centro X",
        "center_y": "Centro Y",
        "center_z": "Centro Z",
        "radius": "Radio",
        "major_radius": "Radio mayor",
        "minor_radius": "Radio menor",
        "start_angle": "Ángulo inicial",
        "end_angle": "Ángulo final",
        "length": "Longitud / Largo",
        "width": "Ancho",
        "height": "Altura / Alto",
        "thickness": "Espesor",
        "diameter": "Diámetro",
        "dx": "Desplazamiento en X",
        "dy": "Desplazamiento en Y",
        "dz": "Desplazamiento en Z",
        "angle": "Ángulo de giro",
        "factor": "Factor de escala",
        "scale": "Escala",
        "rotation": "Ángulo de rotación",
        "nfaces": "Cantidad de lados",
        "sides": "Cantidad de lados",
        "steps": "Cantidad de escalones",
        "rows": "Cantidad de filas",
        "columns": "Cantidad de columnas",
        "size": "Tamaño",
        "text": "Texto",
        "label": "Etiqueta",
        "point": "Punto / Coordenadas",
        "p1": "Primer punto",
        "p2": "Segundo punto",
        "vector": "Vector de desplazamiento",
        "delta": "Desplazamiento delta",
    },
    _EN: {
        "x1": "Initial X coordinate",
        "y1": "Initial Y coordinate",
        "z1": "Initial Z coordinate",
        "x2": "Final X coordinate",
        "y2": "Final Y coordinate",
        "z2": "Final Z coordinate",
        "x3": "Point 3 X coordinate",
        "y3": "Point 3 Y coordinate",
        "x": "X coordinate",
        "y": "Y coordinate",
        "z": "Z coordinate",
        "center_x": "Center X",
        "center_y": "Center Y",
        "center_z": "Center Z",
        "radius": "Radius",
        "major_radius": "Major radius",
        "minor_radius": "Minor radius",
        "start_angle": "Start angle",
        "end_angle": "End angle",
        "length": "Length",
        "width": "Width",
        "height": "Height",
        "thickness": "Thickness",
        "diameter": "Diameter",
        "dx": "X displacement",
        "dy": "Y displacement",
        "dz": "Z displacement",
        "angle": "Rotation angle",
        "factor": "Scale factor",
        "scale": "Scale",
        "rotation": "Rotation",
        "nfaces": "Number of sides",
        "sides": "Number of sides",
        "steps": "Number of steps",
        "rows": "Number of rows",
        "columns": "Number of columns",
        "size": "Size",
        "text": "Text",
        "label": "Label",
        "point": "Point / Coordinates",
        "p1": "First point",
        "p2": "Second point",
        "vector": "Displacement vector",
        "delta": "Delta displacement",
    },
    _PT: {
        "x1": "Coordenada X inicial",
        "y1": "Coordenada Y inicial",
        "z1": "Coordenada Z inicial",
        "x2": "Coordenada X final",
        "y2": "Coordenada Y final",
        "z2": "Coordenada Z final",
        "x3": "Coordenada X ponto 3",
        "y3": "Coordenada Y ponto 3",
        "x": "Coordenada X",
        "y": "Coordenada Y",
        "z": "Coordenada Z",
        "center_x": "Centro X",
        "center_y": "Centro Y",
        "center_z": "Centro Z",
        "radius": "Raio",
        "major_radius": "Raio maior",
        "minor_radius": "Raio menor",
        "start_angle": "Ângulo inicial",
        "end_angle": "Ângulo final",
        "length": "Comprimento",
        "width": "Largura",
        "height": "Altura",
        "thickness": "Espessura",
        "diameter": "Diâmetro",
        "dx": "Deslocamento em X",
        "dy": "Deslocamento em Y",
        "dz": "Deslocamento em Z",
        "angle": "Ângulo de rotação",
        "factor": "Fator de escala",
        "scale": "Escala",
        "rotation": "Rotação",
        "nfaces": "Número de lados",
        "sides": "Número de lados",
        "steps": "Quantidade de degraus",
        "rows": "Quantidade de linhas",
        "columns": "Quantidade de colunas",
        "size": "Tamanho",
        "text": "Texto",
        "label": "Rótulo",
        "point": "Ponto / Coordenadas",
        "p1": "Primeiro ponto",
        "p2": "Segundo ponto",
        "vector": "Vetor de deslocamento",
        "delta": "Deslocamento delta",
    },
}


def ParamFriendlyName(language: str, name: str) -> str | None:
    norm_lang = _Normalize(language)
    table = _FRIENDLY_NAMES.get(norm_lang, _FRIENDLY_NAMES[_ES])
    return table.get(str(name).strip().lower())


def ParamFriendlyMessage(language: str, name: str, kind: str) -> str | None:
    norm_lang = _Normalize(language)
    label = ParamFriendlyName(norm_lang, name)
    if not label:
        return None
    if norm_lang == _ES:
        return f"Dictá el valor para {label} y decí ok o enviar para confirmar."
    elif norm_lang == _EN:
        return f"Say the value for {label}, then say ok or send to confirm."
    return f"Diga o valor para {label} e diga ok ou enviar para confirmar."