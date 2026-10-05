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

"""New Page — Menú BIM → Annotation → New Page.

Crea una nueva página TechDraw a partir de una plantilla SVG, lista para recibir
vistas (New View) y anotaciones. Sin ruta de plantilla, el comando de FreeCAD
abre su propio diálogo para elegirla y recuerda la última usada.
Comando FreeCAD: BIM_TDPage.
"""

import os

import FreeCAD
import FreeCADGui

COMMAND = "BIM_TDPage"
PARAM_GROUP = "User parameter:BaseApp/Preferences/Mod/BIM"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _CreatePage(template):
    """Crea la página TechDraw con su plantilla y devuelve la página."""
    import TechDraw  # noqa: F401  (registra los tipos TechDraw)

    doc = _RequireDocument()
    filename = os.path.abspath(str(template))
    if not os.path.isfile(filename):
        raise ValueError("No se encontró la plantilla SVG indicada.")

    page = doc.addObject("TechDraw::DrawPage", "Page")
    page.Label = os.path.splitext(os.path.basename(filename))[0]
    draw_template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    draw_template.Template = filename
    draw_template.Label = "Template"
    page.Template = draw_template

    FreeCAD.ParamGet(PARAM_GROUP).SetString(
        "TDTemplateDir", filename.replace("\\", "/")
    )
    _ReadEditableScale(page, draw_template)

    doc.recompute()
    return page


def _ReadEditableScale(page, draw_template):
    """Toma la escala del texto editable "scale" de la plantilla, si la tiene."""
    texts = draw_template.EditableTexts
    for key in ["scale", "Scale", "SCALE", "scaling", "Scaling", "SCALING"]:
        value = texts.get(key)
        if not value:
            continue
        value = value.replace(":", "/")
        if "/" in value:
            try:
                numerator, denominator = value.split("/", 1)
                page.Scale = float(numerator) / float(denominator)
            except (ValueError, ZeroDivisionError):
                pass
        else:
            try:
                page.Scale = float(value)
            except ValueError:
                pass
        return


def CreateNewPage(template=None):
    """Crea una página TechDraw nueva a partir de una plantilla SVG.

    Parámetros
    ----------
    template : str, opcional
        Ruta del archivo SVG de la plantilla. Si se omite se activa el comando
        interactivo, que deja elegir la plantilla.

    Devuelve
    --------
    object: la página creada, o None si el comando quedó en modo interactivo.
    """
    _RequireDocument()

    if template is None:
        FreeCADGui.runCommand(COMMAND)
        return None

    return _CreatePage(template)


NewPage = {
    "new page": CreateNewPage,
}
