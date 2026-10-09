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

import FreeCADGui as Gui

def _sketch():
    import Show
    ActiveSketch = Gui.getDocument('Unnamed').getObject('Sketch')
    tv = Show.TempoVis(Gui.ActiveDocument, tag= ActiveSketch.ViewObject.TypeId)
    ActiveSketch.ViewObject.TempoVis = tv
    if ActiveSketch.ViewObject.EditingWorkbench:
      tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)
    if ActiveSketch.ViewObject.HideDependent:
      tv.hide(tv.get_all_dependent(Gui.getDocument('Unnamed').getObject('Sketch'), ''))
    if ActiveSketch.ViewObject.ShowSupport:
      tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not (ref[0].isDerivedFrom("App::Plane") or ref[0].isDerivedFrom("App::LocalCoordinateSystem"))])
    if ActiveSketch.ViewObject.ShowLinks:
      tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
    tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
    tv.hide(ActiveSketch)
    del(tv)
    del(ActiveSketch)

    ActiveSketch = Gui.getDocument('Unnamed').getObject('Sketch')
    if ActiveSketch.ViewObject.RestoreCamera:
      ActiveSketch.ViewObject.TempoVis.saveCamera()
      if ActiveSketch.ViewObject.ForceOrtho:
        ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')

Sketch = {
    "sketch": _sketch()
}
