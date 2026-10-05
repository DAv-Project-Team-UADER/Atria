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

"""New View — Menú BIM → Annotation → New View.

Crea una nueva vista TechDraw a partir de un plano de sección o de objetos 2D y
la inserta en una página. Cada plano de sección genera una vista DrawViewArch y
cada objeto 2D una vista DrawViewDraft, ambas con la escala de la página.
Comando FreeCAD: BIM_TDView.
"""

import FreeCAD
import FreeCADGui

COMMAND = "BIM_TDView"


def _RequireDocument():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No hay un documento de FreeCAD abierto.")
    return doc


def _SplitTargets(targets):
    """Separa los objetivos en planos de sección y objetos 2D."""
    import Draft

    sections = []
    drafts = []
    for obj in targets:
        if obj.isDerivedFrom("TechDraw::DrawPage"):
            # Una página TechDraw seleccionada no debe convertirse en vista
            continue
        if Draft.getType(obj) == "SectionPlane":
            sections.append(obj)
        else:
            drafts.append(obj)
    return sections, drafts


def _ResolvePage(page):
    """Devuelve la página destino: la indicada, la seleccionada o la primera."""
    doc = _RequireDocument()

    if page is None:
        selected = [
            obj
            for obj in FreeCADGui.Selection.getSelection()
            if obj.isDerivedFrom("TechDraw::DrawPage")
        ]
        if selected:
            return selected[0]
        pages = doc.findObjects(Type="TechDraw::DrawPage")
        return pages[0] if pages else None

    if not page.isDerivedFrom("TechDraw::DrawPage"):
        raise ValueError("El destino de la vista tiene que ser una página TechDraw.")

    return page


def _AddArchView(doc, page, section):
    view = doc.addObject("TechDraw::DrawViewArch", "BIM view")
    view.Label = section.Label
    view.Source = section
    page.addView(view)
    if page.Scale:
        view.Scale = page.Scale
    return view


def _AddDraftView(doc, page, draft):
    view = doc.addObject("TechDraw::DrawViewDraft", "DraftView")
    view.Label = draft.Label
    view.Source = draft
    page.addView(view)
    if page.Scale:
        view.Scale = page.Scale
    if "ShapeMode" in draft.PropertiesList:
        draft.ShapeMode = "Shape"
    return view


def CreateNewView(targets=None, page=None):
    """Crea e inserta una vista TechDraw en la página indicada.

    Parámetros
    ----------
    targets : object o list, opcional
        Plano de sección u objetos 2D a representar. Por defecto, la selección
        actual; si está vacía se activa el comando interactivo.
    page : object, opcional
        Página TechDraw destino. Por defecto, la página seleccionada o, si sólo
        hay una, la primera del documento.

    Devuelve
    --------
    list: las vistas creadas, o None si el comando quedó en modo interactivo.
    """
    doc = _RequireDocument()

    if targets is None:
        targets = FreeCADGui.Selection.getSelection()

    if not targets:
        FreeCADGui.runCommand(COMMAND)
        return None

    targets = list(targets) if isinstance(targets, (list, tuple)) else [targets]
    target_page = _ResolvePage(page)
    if target_page is None:
        raise ValueError("No hay ninguna página TechDraw donde insertar la vista.")

    sections, drafts = _SplitTargets(targets)
    views = [_AddArchView(doc, target_page, section) for section in sections]
    views += [_AddDraftView(doc, target_page, draft) for draft in drafts]

    doc.recompute()
    return views


NewView = {
    "new view": CreateNewView,
}
