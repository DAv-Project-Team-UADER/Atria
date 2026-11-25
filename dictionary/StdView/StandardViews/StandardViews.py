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
try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None  # type: ignore[assignment]
    FreeCADGui = None  # type: ignore[assignment]
    Gui = None  # type: ignore[assignment]
from .ayuda import ayuda

ZOOM_FACTOR = 0.9  # 10% de variación


def _apply_zoom(factor):
    """Apply zoom by directly modifying the active 3D view camera node.

    Args:
        factor (float): Multiplier for zoom. < 1 zooms in (closer), > 1 zooms out (farther).
    """
    view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
    if view is None and hasattr(Gui, 'activeView'):
        view = Gui.activeView()
    if view is None:
        return

    cam = view.getCameraNode()
    if cam is None:
        return

    # Cámara Ortográfica (modo por defecto de FreeCAD)
    if hasattr(cam, 'height'):
        cam.height.setValue(cam.height.getValue() * factor)
    # Cámara Perspectiva
    elif hasattr(cam, 'position') and hasattr(cam, 'focalDistance'):
        direction = view.getViewDirection()
        old_focal = cam.focalDistance.getValue()
        new_focal = old_focal * factor
        delta = old_focal - new_focal  # positivo al acercar (factor < 1)

        pos = cam.position.getValue()
        new_pos = [
            pos[0] + delta * direction.x,
            pos[1] + delta * direction.y,
            pos[2] + delta * direction.z,
        ]
        cam.position.setValue(new_pos)
        cam.focalDistance.setValue(new_focal)

    view.redraw()


def _zoom_in():
    """Acercar la cámara un 10%."""
    _apply_zoom(ZOOM_FACTOR)


def _zoom_out():
    """Alejar la cámara un 10%."""
    _apply_zoom(1.0 / ZOOM_FACTOR)

def _toggle_fullscreen():
    """Alterna el modo de pantalla completa de la ventana principal."""
    try:
        Gui.runCommand('Std_MainFullscreen', 0)
    except Exception:
        mw = Gui.getMainWindow()
        if mw:
            if mw.isFullScreen():
                mw.showNormal()
            else:
                mw.showFullScreen()




def _safe_view_call(view_method_name, cmd_name, msg_name=None):
    if not Gui:
        return
    view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
    if view is None and hasattr(Gui, 'activeView'):
        view = Gui.activeView()
    if view and hasattr(view, view_method_name):
        try:
            getattr(view, view_method_name)()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if msg_name and hasattr(Gui, 'SendMsgToActiveView'):
        try:
            Gui.SendMsgToActiveView(msg_name)
            return
        except Exception:
            pass
    try:
        Gui.runCommand(cmd_name)
    except Exception:
        try:
            Gui.runCommand(cmd_name, 0)
        except Exception:
            pass


# Diccionario ATRIA - StdView / StandardViews
StandardViews = {
    'bottom':       lambda: _safe_view_call('viewBottom', 'Std_ViewBottom', 'ViewBottom'),
    'boxzoom':      lambda: Gui.runCommand('Std_ViewBoxZoom') if Gui else None,
    'newview':      lambda: Gui.runCommand('Std_ViewCreate') if Gui else None,
    'dimetric':     lambda: _safe_view_call('viewDimetric', 'Std_ViewDimetric', 'ViewDimetric'),
    'fitall':       lambda: _safe_view_call('fitAll', 'Std_ViewFitAll', 'FitAll'),
    'fitselection': lambda: _safe_view_call('fitSelection', 'Std_ViewFitSelection', 'FitSelection'),
    'front':        lambda: _safe_view_call('viewFront', 'Std_ViewFront', 'ViewFront'),
    'fullscreen':   _toggle_fullscreen,
    'home':         lambda: Gui.runCommand('Std_ViewHome') if Gui else None,
    'isometric':    lambda: _safe_view_call('viewIsometric', 'Std_ViewIsometric', 'ViewIsometric'),
    'left':         lambda: _safe_view_call('viewLeft', 'Std_ViewLeft', 'ViewLeft'),
    'rear':         lambda: _safe_view_call('viewRear', 'Std_ViewRear', 'ViewRear'),
    'right':        lambda: _safe_view_call('viewRight', 'Std_ViewRight', 'ViewRight'),
    'top':          lambda: _safe_view_call('viewTop', 'Std_ViewTop', 'ViewTop'),
    'trimetric':    lambda: _safe_view_call('viewTrimetric', 'Std_ViewTrimetric', 'ViewTrimetric'),
    'zoomin':       _zoom_in,
    'zoomout':      _zoom_out,
    'help':         ayuda,
}