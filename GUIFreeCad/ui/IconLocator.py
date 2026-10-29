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

"""Resolve dictionary keys to SVG icon paths."""

from __future__ import annotations

import os
from pathlib import Path


class IconLocator:
    """Finds the SVG of a dictionary key, indexing each source once.

    The previous implementation walked the whole dictionary tree **per button
    and per re-render**, with no cache. Here the index is built lazily on the
    first lookup and reused over ``InterfazATRIA/Icons`` (centralized icon store).

    Args:
        SearchRoots: directories to index, highest priority first. When
            omitted they are resolved from this file's location.

    Example::

        locator = IconLocator()
        path = locator.Find("extrude")   # "" when there is no icon
    """

    def __init__(self, SearchRoots: list[Path] | None = None) -> None:
        self._roots = SearchRoots if SearchRoots is not None else self._DefaultRoots()
        self._index: dict[str, str] | None = None

    @staticmethod
    def _DefaultRoots() -> list[Path]:
        """Icon directories, resolved relative to this file."""
        here = Path(__file__).resolve().parent
        roots: list[Path] = []

        env = os.environ.get("ATRIA_ICONS_ROOT", "").strip()
        if env and Path(env).is_dir():
            roots.append(Path(env).resolve())

        for ancestor in (here, *here.parents):
            candidate = ancestor / "InterfazATRIA" / "Icons"
            if candidate.is_dir() and candidate not in roots:
                roots.append(candidate)
                break

        if (here / "Icons").is_dir() and (here / "Icons") not in roots:
            roots.append(here / "Icons")

        return [r for r in roots if r.is_dir()]

    def _BuildIndex(self) -> dict[str, str]:
        """Map ``nombre-normalizado`` → ruta, recorriendo cada raiz una vez.

        Las claves se indexan en minusculas y sin separadores: la clave del
        diccionario es ``lineattributes`` y el archivo ``LineAttributes.svg``,
        o ``new_sketch`` contra ``NewSketch.svg``. Comparar literal dejaba esos
        botones con el fallback de dos letras.

        La primera raiz que define un nombre gana, para que un icono propio
        de InterfazATRIA pueda pisar al del arbol de diccionarios.
        """
        index: dict[str, str] = {}
        for root in self._roots:
            for dirpath, _dirnames, filenames in os.walk(root):
                for filename in filenames:
                    if not filename.lower().endswith(".svg"):
                        continue
                    key = self._Normalize(filename[:-4])
                    index.setdefault(key, os.path.join(dirpath, filename))
        return index

    @staticmethod
    def _Normalize(Name: str) -> str:
        """minusculas, sin guiones ni guiones bajos ni espacios."""
        return Name.lower().replace("_", "").replace("-", "").replace(" ", "")

    #: Claves cuyo icono existe con otro nombre. El diccionario usa el termino
    #: en español o abreviado y el SVG el ingles o el nombre largo; en vez de
    #: renombrar archivos de otras carpetas se mapea acá.
    _ALIASES = {
        "pieza": "part",
        "circulo": "circle",
        "stdview": "standardviews",
        "vistaestandar": "standardviews",
        "2ddrafting": "draft",
        "drafting": "draft",
        "3dbim": "workbenchsketcher",
        "bim": "workbenchsketcher",
        "annotation": "annotation",
        "manage": "manage",
        "modify": "modify",
        "preferences": "preferences",
        "snapping": "snaps",
        "statusbar": "toolbars",
        "utils": "tools",
        "showatriapanel": "info",
        "hideatriapanel": "salir",
        # 2D-Drafting
        "arcfrom3points": "3points",
        "beziercurve": "bezier",
        "cubicbeziercurve": "cubic",
        # Annotation
        "2ddrawing": "createobjects2d",
        "aligneddimension": "dimension",
        "axissystem": "axis",
        "horizontaldimension": "horizontal",
        "leader": "leaderline",
        "newpage": "pagedefault",
        "sectioncut": "section",
        "sectionplane": "section",
        "verticaldimension": "vertical",
        # Manage
        "draftannotationstyleeditor": "annotationstyleeditor",
        "archschedule": "spreadsheet",
        "bimreport": "spreadsheet",
        "bimmaterial": "material",
        # Modify
        "addcomponent": "create",
        "compound": "makecompound",
        "drafttosketch": "crearsketch",
        "patharray": "array",
        "removecomponent": "delete",
        "simplecopy": "copy",
        # Snapping
        "workingplanefront": "front",
        "workingplane": "draftwork",
        "workingplaneside": "right",
        "workingplanetop": "top",
        # Utils
        "unclone": "unlink",
        "bimtrash": "delete",
        "draftslope": "slope",
        "draftworkingplaneproxy": "draftwork",
        "bimwpview": "view",
        "archsurvey": "measure",
        "draftselectgroup": "group",
    }

    def Find(self, Key: str) -> str:
        """Path to the icon for that key.

        Args:
            Key: internal dictionary key, e.g. ``"extrude"``.

        Returns:
            Absolute path to the SVG, or ``""`` when there is none. The caller
            decides the fallback; this never raises.
        """
        if not Key:
            return ""
        if self._index is None:
            self._index = self._BuildIndex()
        normalized = self._Normalize(Key)
        found = self._index.get(normalized, "")
        if found:
            return found
        alias = self._ALIASES.get(normalized)
        return self._index.get(alias, "") if alias else ""

    def Invalidate(self) -> None:
        """Drop the cached index so the next lookup re-scans the roots."""
        self._index = None
