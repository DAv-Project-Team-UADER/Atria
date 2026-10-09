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

"""Resolve callable entries from DiccionariosEnBruto modules."""

from __future__ import annotations

import importlib.util
import os
import sys
import types
from pathlib import Path
from typing import Any, Callable


_KNOWN_DICTIONARIES: dict[str, Path] = {
    "additive": Path("Workbench") / "PartDesign" / "additive" / "additive.py",
    "geometry.line": Path("Workbench") / "Sketcher" / "Geometry" / "line" / "line.py",
}


def _DictionaryRoot() -> Path:
    env = os.environ.get("ATRIA_DICTIONARY_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    here = Path(__file__).resolve()
    for ancestor in here.parents:
        candidate = ancestor / "DiccionariosEnBruto"
        if candidate.is_dir():
            return candidate.resolve()

    return Path("DiccionariosEnBruto")


def EnsureDictionaryPath() -> Path:
    root = _DictionaryRoot()
    text = str(root)
    if root.is_dir() and text not in sys.path:
        sys.path.insert(0, text)
    return root


def _EnsurePackage(name: str, folder: Path) -> types.ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(folder)]  # type: ignore[attr-defined]
    sys.modules[name] = module
    return module


def _LoadModuleFromFile(
    module_path: Path,
    module_name: str,
    parent: types.ModuleType | None = None,
) -> Any:
    spec = importlib.util.spec_from_file_location(
        module_name,
        module_path,
        submodule_search_locations=[str(module_path.parent)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el mÃ³dulo: {module_path}")
    module = importlib.util.module_from_spec(spec)
    if parent is not None:
        module.__package__ = parent.__name__
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _LoadLeafDictionary(module_path: Path, dict_name: str) -> dict[str, Any]:
    EnsureDictionaryPath()
    folder = module_path.parent
    package_parts = module_path.relative_to(_DictionaryRoot()).parent.parts
    package_name = ".".join(("atriadict",) + package_parts)
    parent: types.ModuleType | None = None
    current_path = _DictionaryRoot()
    for part in package_parts:
        current_path = current_path / part
        full_name = ".".join(("atriadict",) + package_parts[: package_parts.index(part) + 1])
        parent = _EnsurePackage(full_name, current_path)

    param_path = folder / "_parametric.py"
    if param_path.is_file():
        _LoadModuleFromFile(param_path, f"{package_name}._parametric", parent=parent)

    module = _LoadModuleFromFile(
        module_path,
        f"{package_name}.{module_path.stem}",
        parent=parent,
    )
    table = getattr(module, dict_name, None)
    if not isinstance(table, dict):
        raise ValueError(f"El mÃ³dulo {module_path} no expone dict '{dict_name}'")
    return table


def GetDictionaryFunction(dictionary_name: str, command_key: str) -> Callable[..., Any]:
    """
    Load a command callable from DiccionariosEnBruto.

    Examples:
        GetDictionaryFunction("additive", "pad_sketch")
        GetDictionaryFunction("geometry.line", "create_by_points")
    """
    key = dictionary_name.strip().lower()
    if key not in _KNOWN_DICTIONARIES:
        raise KeyError(
            f"Diccionario '{dictionary_name}' no registrado. "
            f"Disponibles: {', '.join(sorted(_KNOWN_DICTIONARIES))}"
        )

    module_path = _DictionaryRoot() / _KNOWN_DICTIONARIES[key]
    dict_name = module_path.stem
    table = _LoadLeafDictionary(module_path, dict_name)

    if command_key not in table:
        raise KeyError(
            f"Comando '{command_key}' no existe en '{dictionary_name}'. "
            f"Claves: {', '.join(sorted(table))}"
        )

    command = table[command_key]
    if not callable(command):
        raise TypeError(f"'{command_key}' no es callable.")
    return command
