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

        flags = here.parent / "assets" / "flags"
        if flags.is_dir() and flags not in roots:
            roots.append(flags)

        for ancestor in (here, *here.parents):
            dict_dir = ancestor / "dictionary"
            if dict_dir.is_dir() and dict_dir not in roots:
                roots.append(dict_dir)
                break

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
        "anotacion": "annotation",
        "anotación": "annotation",
        "manage": "manage",
        "administracion": "manage",
        "administración": "manage",
        "modify": "modify",
        "modificar": "modify",
        "preferences": "preferences",
        "preferencias": "preferences",
        "snapping": "snaps",
        "enganche": "snaps",
        "statusbar": "toolbars",
        "barradeenganche": "toolbars",
        "barradeestado": "toolbars",
        "utils": "tools",
        "utilidades": "tools",
        "explorer": "file",
        "explorador": "file",
        "showatriapanel": "info",
        "hideatriapanel": "salir",
        # Select / Selección
        "select": "select",
        "seleccion": "select",
        "selección": "select",
        "selection": "select",
        "next": "selforward",
        "avanzar": "selforward",
        "siguiente": "selforward",
        "previous": "selback",
        "retroceder": "selback",
        "anterior": "selback",
        "selectall": "selectall",
        "deselectall": "selectability",
        "deselect": "selectability",
        "edit": "edit",
        "editar": "edit",
        "delete": "delete",
        "borrar": "delete",
        "eliminar": "delete",
        # 2D-Drafting
        "arcfrom3points": "3points",
        "beziercurve": "bezier",
        "cubicbeziercurve": "cubic",
        # 3D-BIM
        "building": "archbuilding",
        "component": "archcomponent",
        "curtainwall": "archcurtainwall",
        "curtain_wall": "archcurtainwall",
        "door": "bimdoor",
        "externalreference": "archreference",
        "external_reference": "archreference",
        "level": "archlevel",
        "objectslibrary": "bimlibrary",
        "objects_library": "bimlibrary",
        "pipe": "archpipe",
        "pipeconnector": "archpipeconnector",
        "pipe_connector": "archpipeconnector",
        "profile": "archprofile",
        "roof": "archroof",
        "archroof": "archroof",
        "arch_roof": "archroof",
        "shapebuilder": "partshapebuilder",
        "shape_builder": "partshapebuilder",
        "site": "archsite",
        "slab": "bimslab",
        "space": "archspace",
        "wall": "archwall",
        "window": "archwindow",
        "beamreinforcement": "beam",
        "beam_reinforcement": "beam",
        "columnreinforcement": "column",
        "column_reinforcement": "column",
        "bentshaperebar": "reinforcementbentshaperebar",
        "bent_shape_rebar": "reinforcementbentshaperebar",
        "helicalrebar": "reinforcementhelicalrebar",
        "helical_rebar": "reinforcementhelicalrebar",
        "lshaperebar": "reinforcementlshaperebar",
        "l_shape_rebar": "reinforcementlshaperebar",
        "stirruprebar": "reinforcementstirruprebar",
        "stirrup_rebar": "reinforcementstirruprebar",
        "straightrebar": "reinforcementstraightrebar",
        "straight_rebar": "reinforcementstraightrebar",
        "ushaperebar": "reinforcementushaperebar",
        "u_shape_rebar": "reinforcementushaperebar",
        "cmd": "archroof",
        # Annotation
        "2ddrawing": "createobjects2d",
        "aligneddimension": "bimdimensionaligned",
        "axissystem": "archaxissystem",
        "horizontaldimension": "bimdimensionhorizontal",
        "leader": "bimleader",
        "newpage": "bimpagedefault",
        "sectioncut": "archviewcut",
        "sectionplane": "archsectionplane",
        "sectionview": "archsectionplane",
        "verticaldimension": "bimdimensionvertical",
        "createaxis": "archaxis",
        "createaxissystem": "archaxissystem",
        "creategrid": "archgrid",
        "createhatch": "drafthatch",
        "createlabel": "draftlabel",
        "createleader": "bimleader",
        "createnewpage": "bimpagedefault",
        "createnewview": "biminsertview",
        "createsectioncut": "archviewcut",
        "createsectionplane": "archsectionplane",
        "createsectionview": "archsectionplane",
        "createtext": "drafttext",
        "createtwoddrawing": "createobjects2d",
        "creardibujo2d": "createobjects2d",
        "dibujo2d": "createobjects2d",
        "eje": "archaxis",
        "sistemadeejes": "archaxissystem",
        "rejilla": "archgrid",
        "sombreado": "drafthatch",
        "etiqueta": "draftlabel",
        "lider": "bimleader",
        "líder": "bimleader",
        "nuevapagina": "bimpagedefault",
        "nuevapágina": "bimpagedefault",
        "vistanueva": "biminsertview",
        "cortedeseccion": "archviewcut",
        "cortedesección": "archviewcut",
        "planodeseccion": "archsectionplane",
        "planodesección": "archsectionplane",
        "vistadeseccion": "archsectionplane",
        "vistadesección": "archsectionplane",
        "texto": "drafttext",
        # Manage
        "draftannotationstyleeditor": "annotationstyleeditor",
        "archschedule": "archschedule",
        "bimreport": "bimreport",
        "bimmaterial": "bimmaterial",
        "managedoorsandwindows": "bimwindows",
        "manageifcelements": "bimifcelements",
        "manageifcquantities": "bimifcquantities",
        "setupproject": "bimprojectmanager",
        "gestionarpuertasyventanas": "bimwindows",
        "gestionarlementosifc": "bimifcelements",
        "gestionarcantidadesifc": "bimifcquantities",
        "configurarproyectobim": "bimprojectmanager",
        # Modify
        "addcomponent": "create",
        "compound": "partcompound",
        "makecompound": "partcompound",
        "drafttosketch": "crearsketch",
        "patharray": "array",
        "removecomponent": "delete",
        "simplecopy": "copy",
        "cutwithplane": "cut",
        "difference": "cut",
        "extrudeface": "extrude",
        "pointarray": "array",
        "polararray": "array",
        "union": "boolean",
        "cortarconplano": "cut",
        "cortarobjetos": "cut",
        "extruircara": "extrude",
        "crearmatrizporpuntos": "array",
        "crearmatrizpolar": "array",
        "unirobjetos": "boolean",
        "crearcompuesto": "boolean",
        # Preferences
        "openpreferences": "preferences",
        "openvoicepreferences": "preferences",
        "setlanguagees": "es",
        "setlanguageen": "en",
        "idiomaespanol": "es",
        "idiomaespañol": "es",
        "idiomaingles": "en",
        "idiomainglés": "en",
        # Snapping
        "workingplanefront": "front",
        "workingplane": "draftwork",
        "workingplaneside": "right",
        "workingplanetop": "top",
        "togglesnap": "snaps",
        "setworkingplanefront": "front",
        "snapcenter": "center",
        "snapendpoint": "point",
        "snapgrid": "grid",
        "snaplock": "lock",
        "snapmidpoint": "midpoint",
        "snaportho": "ortho",
        "engancheacentro": "center",
        "engancheaextremo": "point",
        "enganchearejilla": "grid",
        "bloquearenganche": "lock",
        "engancheapuntomedio": "midpoint",
        "modoortogonal": "ortho",
        "alternarenganche": "snaps",
        "activarenganche": "snaps",
        "desactivarenganche": "snaps",
        # StatusBar
        "togglestatusbar": "toolbars",
        "setunitsmm": "dimension",
        "setunitsm": "dimension",
        "setunitsin": "dimension",
        "showstatusmessage": "info",
        "barradeherramientas": "toolbars",
        "unidadesmilimetros": "dimension",
        "unidadesmilímetros": "dimension",
        "unidadesmetros": "dimension",
        "unidadespulgadas": "dimension",
        "mensajedeestado": "info",
        # Utils
        "unclone": "unlink",
        "bimtrash": "delete",
        "draftslope": "slope",
        "draftworkingplaneproxy": "draftwork",
        "bimwpview": "bimwpview",
        "archsurvey": "archsurvey",
        "draftselectgroup": "draftselectgroup",
        "addtoconstructiongroup": "draftselectgroup",
        "check": "partshapebuilder",
        "closeholes": "closewire",
        "converttoifcproject": "bimprojectmanager",
        "ifcdiff": "bimifcelements",
        "structure": "structure",
        "multiplestructures": "structure",
        "panelsheet": "panels",
        "ifcexpand": "bimifcelements",
        "ifcexplorer": "bimifcelements",
        "ifcopenshellupdate": "bimifcelements",
        "ifcshapediff": "bimifcelements",
        "imageplane": "loadimage",
        "lockifc": "lock",
        "mergewalls": "archwall",
        "meshtoshape": "partshapebuilder",
        "newifcspreadsheet": "spreadsheet",
        "nest": "panels",
        "nudgedown": "bottom",
        "nudgeextend": "extendedge",
        "nudgeleft": "left",
        "nudgeright": "right",
        "nudgerotateleft": "rotate",
        "nudgerotateright": "rotate",
        "nudgeshrink": "cut",
        "nudgeswitch": "tools",
        "nudgeup": "top",
        "panel": "archpanel",
        "glue": "join",
        "ifcproject": "bimprojectmanager",
        "panelcut": "cut",
        "reextrude": "extrude",
        "removeshapefrombim": "unlink",
        "renamewire": "wire",
        "selectnonmanifoldmeshes": "partshapebuilder",
        "structuralsystem": "structure",
        "splitmesh": "split",
        "toggle3dviewbackground": "activeview",
        "togglebimviews": "bimwpview",
        "toggleifcbrepflag": "bimifcelements",
        "togglesubcomponents": "archcomponent",
        # Explorer submenus and direct commands
        "file": "file",
        "proyecto": "proyecto",
        "edit": "edit",
        "print": "print",
        "windows": "bimwindows",
        "expressions": "spreadsheet",
        "tools": "tools",
        "examples": "examples",
        "refresh": "refresh",
        "screenshot": "screenshot",
        "textdoc": "textdoc",
        "unlink": "unlink",
        "freeze": "freeze",
        "allinstances": "allinstances",
        "variableset": "variableset",
        "help": "helpwhatsthis",
        "ayuda": "helpwhatsthis",
        "moveview": "activeview",
        # Explorer Spoken phrases
        "archivo": "file",
        "archivos": "file",
        "carpeta": "file",
        "carpetas": "file",
        "folios": "file",
        "proyectos": "proyecto",
        "editar": "edit",
        "edicion": "edit",
        "edición": "edit",
        "modificar": "edit",
        "alterar": "edit",
        "imprimir": "print",
        "generarpdf": "print",
        "exportarpdf": "print",
        "impresion": "print",
        "impresión": "print",
        "impresora": "print",
        "pdf": "print",
        "ventanas": "bimwindows",
        "ventana": "bimwindows",
        "expresion": "spreadsheet",
        "expresiones": "spreadsheet",
        "expresión": "spreadsheet",
        "herramientas": "tools",
        "herramienta": "tools",
        "utilidades": "tools",
        "barradeestructura": "structure",
        "barraestructura": "structure",
        "barradeherramientasdeestructura": "structure",
        "ejemplo": "examples",
        "ejemplos": "examples",
        "quieroaprender": "examples",
        "aprender": "examples",
        "tutoriales": "examples",
        "refrescar": "refresh",
        "recargar": "refresh",
        "actualizar": "refresh",
        "foto": "screenshot",
        "captura": "screenshot",
        "sacarfoto": "screenshot",
        "guardarpantalla": "screenshot",
        "capturadepantalla": "screenshot",
        "documentodetexto": "textdoc",
        "documento": "textdoc",
        "desvincular": "unlink",
        "quitarenlace": "unlink",
        "desenlazar": "unlink",
        "romperenlace": "unlink",
        "separarenlace": "unlink",
        "desasociar": "unlink",
        "desconectar": "unlink",
        "congelar": "freeze",
        "inmovilizar": "freeze",
        "bloquear": "freeze",
        "todaslasinstancias": "allinstances",
        "seleccionarinstancias": "allinstances",
        "todasinstancias": "allinstances",
        "conjuntodevariables": "variableset",
        "variables": "variableset",
        "setdevariables": "variableset",
        "informacion": "helpwhatsthis",
        "información": "helpwhatsthis",
        "opciones": "helpwhatsthis",
        # StandardViews Spanish
        "abajo": "bottom",
        "inferior": "bottom",
        "vistabajo": "bottom",
        "vistainferior": "bottom",
        "desdeabajo": "bottom",
        "vistabaja": "bottom",
        "zoomcaja": "boxzoom",
        "zoomrectangular": "boxzoom",
        "zoomarea": "boxzoom",
        "zoomporcaja": "boxzoom",
        "zoomdearea": "boxzoom",
        "nuevavista": "newview",
        "crearvista": "newview",
        "ventananueva": "newview",
        "nuevaventana": "newview",
        "dimetrica": "dimetric",
        "dimétrica": "dimetric",
        "vistadimetrica": "dimetric",
        "vistadimétrica": "dimetric",
        "ajustartodo": "fitall",
        "vertodo": "fitall",
        "encuadrartodo": "fitall",
        "ajustaratodo": "fitall",
        "ajustarseleccion": "fitselection",
        "ajustarselección": "fitselection",
        "encuadrarseleccion": "fitselection",
        "encuadrarselección": "fitselection",
        "frontal": "front",
        "frente": "front",
        "vistafrontal": "front",
        "vistadefrente": "front",
        "desdeelfrente": "front",
        "pantallacompleta": "fullscreen",
        "pantallaentera": "fullscreen",
        "modopantallacompleta": "fullscreen",
        "maximizavista": "fullscreen",
        "inicio": "home",
        "vistainicial": "home",
        "vistapordefecto": "home",
        "vistapredeterminada": "home",
        "restablecervista": "home",
        "isometrica": "isometric",
        "isométrica": "isometric",
        "vistaisometrica": "isometric",
        "vistaisométrica": "isometric",
        "izquierda": "left",
        "izquierdo": "left",
        "lateralizquierdo": "left",
        "vistaizquierda": "left",
        "desdelaizquierda": "left",
        "trasera": "rear",
        "posterior": "rear",
        "detras": "rear",
        "atras": "rear",
        "atrás": "rear",
        "vistatrasera": "rear",
        "desdeatras": "rear",
        "derecha": "right",
        "derecho": "right",
        "lateralderecho": "right",
        "vistaderecha": "right",
        "desdeladerecha": "right",
        "arriba": "top",
        "superior": "top",
        "planta": "top",
        "vistasuperior": "top",
        "vistadearriba": "top",
        "desdearriba": "top",
        "trimetrica": "trimetric",
        "trimétrica": "trimetric",
        "vistatrimetrica": "trimetric",
        "vistatrimétrica": "trimetric",
        "acercar": "zoomin",
        "zoommas": "zoomin",
        "zoommás": "zoomin",
        "aumentarzoom": "zoomin",
        "zoomacercar": "zoomin",
        "alejar": "zoomout",
        "zoommenos": "zoomout",
        "disminuirzoom": "zoomout",
        "zoomalejar": "zoomout",
        # MoveView Spanish
        "arrastrarvista": "activeview",
        "centrar": "activeview",
        "centraren": "activeview",
        "centrarvista": "activeview",
        "desplazarvista": "activeview",
        "ira": "activeview",
        "irapunto": "activeview",
        "iralpunto": "activeview",
        "llevara": "activeview",
        "mover": "activeview",
        "movercamara": "activeview",
        "movercámara": "activeview",
        "movervista": "activeview",
        "panear": "activeview",
        "posicionarvista": "activeview",
        # English phrases
        "files": "file",
        "folder": "file",
        "folders": "file",
        "sheets": "file",
        "documents": "file",
        "project": "proyecto",
        "projects": "proyecto",
        "editing": "edit",
        "printing": "print",
        "printer": "print",
        "window": "bimwindows",
        "expression": "spreadsheet",
        "tool": "tools",
        "utilities": "tools",
        "structuretoolbar": "structure",
        "structurebar": "structure",
        "example": "examples",
        "learn": "examples",
        "iwanttolearn": "examples",
        "wanttolearn": "examples",
        "reload": "refresh",
        "photo": "screenshot",
        "takephoto": "screenshot",
        "capture": "screenshot",
        "savescreen": "screenshot",
        "screencapture": "screenshot",
        "textdocument": "textdoc",
        "textfile": "textdoc",
        "removelink": "unlink",
        "detachlink": "unlink",
        "immobilize": "freeze",
        "selectallinstances": "allinstances",
        "variableset": "variableset",
        "varset": "variableset",
        "info": "helpwhatsthis",
        # Views & Camera
        "views": "views",
        "vistas": "views",
        "camara": "camera",
        "cámara": "camera",
        "camera": "camera",
        "perspective": "perspective",
        "perspectiva": "perspective",
        "orthographic": "orthographic",
        "ortogonal": "orthographic",
        "isometric": "isometric",
        "isometrica": "isometric",
        "isométrica": "isometric",
        "front": "front",
        "frontal": "front",
        "fitall": "fitall",
        "centrarvista": "fitall",
        "ajustartodo": "fitall",
        "fitselection": "fitselection",
        "enfocarseleccion": "fitselection",
        "enfocarselección": "fitselection",
        "rotateleft": "rotate",
        "rotateright": "rotate",
        "rotateup": "rotate",
        "rotatedown": "rotate",
        "girarizquierda": "rotate",
        "girarderecha": "rotate",
        "girararriba": "rotate",
        "girarabajo": "rotate",
        "movecamera": "camerapos",
        "movercamara": "camerapos",
        "movercámara": "camerapos",
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
        if alias and alias in self._index:
            return self._index[alias]

        # Heuristic 1: If key starts with "create", try stripping "create" or adding workbench prefixes
        if normalized.startswith("create"):
            sub = normalized[6:]
            if sub in self._index:
                return self._index[sub]
            if sub in self._ALIASES and self._ALIASES[sub] in self._index:
                return self._index[self._ALIASES[sub]]
            for prefix in ("arch", "draft", "bim", "part"):
                cand = prefix + sub
                if cand in self._index:
                    return self._index[cand]
                if cand in self._ALIASES and self._ALIASES[cand] in self._index:
                    return self._index[self._ALIASES[cand]]

        # Heuristic 2: If key starts with "snap", try stripping "snap"
        if normalized.startswith("snap"):
            sub = normalized[4:].lstrip("_")
            if sub in self._index:
                return self._index[sub]
            if sub in self._ALIASES and self._ALIASES[sub] in self._index:
                return self._index[self._ALIASES[sub]]
            for prefix in ("draftsnap", "draft"):
                cand = prefix + sub
                if cand in self._index:
                    return self._index[cand]

        # Heuristic 3: Units setting buttons
        if "units" in normalized:
            dim = self._index.get("dimension")
            if dim:
                return dim

        # Heuristic 4: Direct workbench prefixes (arch, bim, part, reinforcement)
        for prefix in ("arch", "bim", "part", "reinforcement"):
            cand = prefix + normalized
            if cand in self._index:
                return self._index[cand]
            if cand in self._ALIASES and self._ALIASES[cand] in self._index:
                return self._index[self._ALIASES[cand]]

        return ""

    def Invalidate(self) -> None:
        """Drop the cached index so the next lookup re-scans the roots."""
        self._index = None
