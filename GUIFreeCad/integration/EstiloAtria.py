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

"""ATRIA visual style for the 3D view: white background, graph-paper grid and a clean look for solids.

Entry points, all safe to call outside FreeCAD (they do nothing there):

- :func:`aplicarFondoBlanco` paints the 3D view background white.
- :func:`aplicarRejilla` gives Draft and Sketcher the same 2 mm grid.
- :func:`aplicarVistaAtria` applies the three view-wide settings: background, grid and line width.
- :func:`aplicarEstiloAtria` gives one object the ATRIA look (light-gray solid, dark edges).
- :func:`instalarEstiloAtria` applies the view settings and keeps the look on every new solid.

The voice command ``AplicarEstilo`` (``Operations/EspecialOperations.py``) uses
:func:`aplicarVistaAtria` and :func:`aplicarEstiloAtria`; the dock panel calls
:func:`instalarEstiloAtria` when it is mounted.
"""

from __future__ import annotations

try:
    import FreeCAD
    import FreeCADGui
except ImportError:  # fuera de FreeCAD (pruebas, documentaciÃ³n)
    FreeCAD = None
    FreeCADGui = None

# colores como (r, g, b) entre 0 y 1, el formato de ViewObject
FONDO = (1.0, 1.0, 1.0)
SOLIDO = (0.80, 0.82, 0.85)
ARISTA = (0.15, 0.15, 0.15)
ANCHO_LINEA = 2.0

# Papel cuadriculado de Draft y Sketcher: 2 x 2 mm en #D4C7C5 sobre el fondo blanco.
REJILLA = (0xD4 / 255, 0xC7 / 255, 0xC5 / 255)
PASO_REJILLA = "2 mm"

_VIEW_PARAMS = "User parameter:BaseApp/Preferences/View"
_DRAFT_PARAMS = "User parameter:BaseApp/Preferences/Mod/Draft"
_SKETCHER_PARAMS = "User parameter:BaseApp/Preferences/Mod/Sketcher/General"
# Los objetos de origen no son piezas: no se les cambia el aspecto.
_IGNORADOS = ("App::Origin", "App::Line", "App::Plane")

_observer = None


def _empaquetar(color: tuple[float, float, float], alfa: int = 255) -> int:
    """Pack an (r, g, b) colour into the unsigned RGBA integer FreeCAD stores in its parameters."""
    r, g, b = (round(canal * 255) for canal in color)
    return (r << 24) | (g << 16) | (b << 8) | alfa


def aplicarFondoBlanco() -> None:
    """Make the 3D view background plain white, now and for the next sessions."""
    if FreeCAD is None:
        return
    params = FreeCAD.ParamGet(_VIEW_PARAMS)
    fondo = _empaquetar(FONDO)
    params.SetBool("Simple", True)
    params.SetBool("Gradient", False)
    params.SetUnsigned("BackgroundColor", fondo)
    params.SetUnsigned("BackgroundColor2", fondo)
    params.SetUnsigned("BackgroundColor3", fondo)
    params.SetUnsigned("BackgroundColor4", fondo)
    # la vista abierta no relee las preferencias sola: se le pide el color directo si puede
    try:
        vista = FreeCADGui.ActiveDocument.ActiveView
        vista.setBackgroundColor(*FONDO)
    except Exception:  # noqa: BLE001 - sin vista activa o versiÃ³n sin ese mÃ©todo
        pass


def aplicarRejilla() -> None:
    """Give Draft and Sketcher the same 2 x 2 mm grid, in ``REJILLA`` and always visible."""
    if FreeCAD is None:
        return
    color = _empaquetar(REJILLA)

    draft = FreeCAD.ParamGet(_DRAFT_PARAMS)
    draft.SetBool("grid", True)
    draft.SetBool("alwaysShowGrid", True)
    draft.SetString("gridSpacing", PASO_REJILLA)
    draft.SetUnsigned("gridColor", color)
    # en Draft el parÃ¡metro es opacidad, no transparencia: 100 deja el color tal cual
    draft.SetInt("gridTransparency", 100)
    # sin borde, sin figura humana y sin ejes de colores: la cuadrÃ­cula queda pareja
    draft.SetBool("gridBorder", False)
    draft.SetBool("gridShowHuman", False)
    draft.SetBool("coloredGridAxes", False)

    sketcher = FreeCAD.ParamGet(_SKETCHER_PARAMS)
    sketcher.SetBool("ShowGrid", True)
    # con el paso automÃ¡tico la cuadrÃ­cula crece con el zoom y deja de medir 2 mm
    sketcher.SetBool("GridAuto", False)
    # el Sketcher guarda el paso como cantidad, en un subgrupo del mismo nombre
    sketcher.GetGroup("GridSize").SetString("GridSize", PASO_REJILLA)
    # una sola familia de lÃ­neas: todos los cuadros iguales, sin lÃ­neas maestras
    sketcher.SetInt("GridNumberSubdivision", 1)
    sketcher.SetUnsigned("GridLineColor", color)
    sketcher.SetUnsigned("GridDivLineColor", color)
    # 0xffff es la lÃ­nea llena; el Sketcher trae las finas punteadas
    sketcher.SetInt("GridLinePattern", 0xFFFF)
    sketcher.SetInt("GridDivLinePattern", 0xFFFF)
    sketcher.SetInt("GridTransparency", 0)


def aplicarVistaAtria() -> None:
    """Apply the ATRIA settings that belong to the view, not to one object."""
    if FreeCAD is None:
        return
    aplicarFondoBlanco()
    aplicarRejilla()
    # los objetos planos de Draft no pasan por aplicarEstiloAtria (no tienen caras):
    # el ancho les llega por la preferencia global.
    FreeCAD.ParamGet(_VIEW_PARAMS).SetInt("DefaultShapeLineWidth", round(ANCHO_LINEA))


def aplicarEstiloAtria(obj) -> bool:
    """Give ``obj`` the ATRIA look; return ``True`` when something was changed.

    Only solids and surfaces are restyled: sketches, planes, joints and any object without
    a shape keep their own appearance.

    Args:
        obj: a FreeCAD document object (``Part::Feature`` or a body/feature built on it).
    """
    if FreeCAD is None or obj is None or getattr(obj, "TypeId", "") in _IGNORADOS:
        return False
    vista = getattr(obj, "ViewObject", None)
    forma = getattr(obj, "Shape", None)
    if vista is None or forma is None or forma.isNull() or not (forma.Solids or forma.Faces):
        return False
    cambio = False
    for atributo, valor in (
        ("ShapeColor", SOLIDO),
        ("LineColor", ARISTA),
        ("LineWidth", ANCHO_LINEA),
    ):
        if hasattr(vista, atributo):
            setattr(vista, atributo, valor)
            cambio = True
    return cambio


class _EstiloObserver:
    """Document observer: styles each solid once, right after it gets its shape."""

    def __init__(self):
        # (documento, objeto) ya pintados: un recÃ¡lculo posterior no pisa los colores del usuario
        self._pintados = set()

    def slotChangedObject(self, obj, prop):  # noqa: N802 - nombre fijo de FreeCAD
        # la forma se calcula despuÃ©s de crear el objeto; reciÃ©n ahÃ­ hay algo que pintar
        if prop != "Shape":
            return
        clave = (obj.Document.Name, obj.Name)
        if clave in self._pintados:
            return
        try:
            if aplicarEstiloAtria(obj):
                self._pintados.add(clave)
        except Exception as exc:  # noqa: BLE001 - un fallo de estilo no debe cortar el modelado
            print(f"[ATRIA] Estilo visual: {exc}")


def instalarEstiloAtria() -> None:
    """Apply the view settings and style every solid created from now on.

    Calling it again does nothing.
    """
    global _observer
    if FreeCAD is None or _observer is not None:
        return
    aplicarVistaAtria()
    _observer = _EstiloObserver()
    FreeCAD.addDocumentObserver(_observer)
