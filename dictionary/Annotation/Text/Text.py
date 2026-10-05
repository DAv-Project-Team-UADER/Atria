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

"""Text — Menú BIM → Annotation → Text.

Crea un texto, ya sea un objeto Text en la vista 3D actual, o un objeto
Annotation en la página TechDraw activa. El contenido y el punto de inserción
se pueden pasar por parámetro; si no se pasan, el comando de FreeCAD queda a la
espera de que el usuario los indique en la vista.
Comando FreeCAD: BIM_Text.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_Text"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _RequireView():
    if not FreeCADGui.ActiveDocument:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    view = FreeCADGui.activeView()
    if view is None:
        raise RuntimeError("No hay una vista activa en FreeCAD.")
    return view


def _AsVector(point):
    return FreeCAD.Vector(float(point[0]), float(point[1]), float(point[2]))


def _ActivePage():
    view = FreeCADGui.activeView()
    if hasattr(view, "getPage") and view.getPage():
        return view.getPage()
    return None


def _CreateAnnotation(page, text):
    """Crea un Annotation de TechDraw con el texto indicado."""
    import TechDraw  # noqa: F401  (registra el tipo TechDraw::DrawViewAnnotation)

    doc = _RequireDocument()
    params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    scale = page.Scale or 1.0
    annotation = doc.addObject("TechDraw::DrawViewAnnotation", "Annotation")
    annotation.Text = text
    annotation.TextSize = params.GetFloat("textheight", 10) * scale
    annotation.Font = params.GetString("textfont", "Sans")
    color = params.GetUnsigned("DefaultTextColor", 255)
    annotation.TextColor = (
        ((color >> 24) & 0xFF) / 255.0,
        ((color >> 16) & 0xFF) / 255.0,
        ((color >> 8) & 0xFF) / 255.0,
    )
    page.addView(annotation)
    doc.recompute()
    return annotation


def _CreateDraftText(text, point):
    """Crea un objeto Draft Text en la vista 3D."""
    import Draft

    doc = _RequireDocument()
    obj = Draft.make_text(
        text, placement=FreeCAD.Vector(0, 0, 0) if point is None else point
    )
    Draft.autogroup(obj)
    doc.recompute()
    return obj


def CreateText(text=None, point=None):
    """Crea un texto en la vista 3D o en la página TechDraw activa.

    Parámetros
    ----------
    text : str, opcional
        Contenido del texto. Si se omite, se activa el comando interactivo.
    point : tuple, opcional
        Punto de inserción (x, y, z) del texto en la vista 3D. Si se omite se
        usa el origen.

    Devuelve
    --------
    object: el texto creado, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()
    _RequireView()

    if text is not None:
        text = str(text).strip()
        if not text:
            raise ValueError("El contenido del texto no puede estar vacío.")

    page = _ActivePage()
    if page is not None:
        if text is None:
            FreeCADGui.runCommand(COMMAND)
            return None
        return _CreateAnnotation(page, text)

    if text is not None:
        return _CreateDraftText(text, None if point is None else _AsVector(point))

    FreeCADGui.runCommand(COMMAND)
    return None


Text = {
    "text": CreateText,
}
