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

"""Comandos de cámara, perspectiva y navegación visual para ATRIA."""

from __future__ import annotations

try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None
    FreeCADGui = None
    Gui = None


def _get_active_view():
    """Obtiene de forma segura la vista 3D activa de FreeCAD."""
    if not Gui:
        return None
    try:
        if getattr(Gui, 'ActiveDocument', None):
            view = getattr(Gui.ActiveDocument, 'ActiveView', None)
            if view:
                return view
    except Exception:
        pass
    try:
        if hasattr(Gui, 'activeView'):
            return Gui.activeView()
    except Exception:
        pass
    return None


def _safe_view_call(view_method_name: str, cmd_name: str, msg_name: str | None = None) -> None:
    """Invoca una acción de vista sobre la cámara activa con múltiples fallbacks."""
    view = _get_active_view()
    if view and hasattr(view, view_method_name):
        try:
            getattr(view, view_method_name)()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if Gui:
        if msg_name and hasattr(Gui, 'SendMsgToActiveView'):
            try:
                Gui.SendMsgToActiveView(msg_name)
                return
            except Exception:
                pass
        try:
            Gui.runCommand(cmd_name)
            return
        except Exception:
            pass
        try:
            Gui.runCommand(cmd_name, 0)
        except Exception:
            pass


def perspective() -> None:
    """Activa la cámara con perspectiva cónica (3D realista con profundidad)."""
    view = _get_active_view()
    if view and hasattr(view, 'setCameraType'):
        try:
            view.setCameraType("Perspective")
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if Gui:
        try:
            Gui.runCommand('Std_PerspectiveCamera')
        except Exception:
            try:
                Gui.runCommand('Std_PerspectiveCamera', 1)
            except Exception:
                pass


def orthographic() -> None:
    """Activa la cámara ortogonal / paralela (sin distorsión de perspectiva, ideal para planos técnicos)."""
    view = _get_active_view()
    if view and hasattr(view, 'setCameraType'):
        try:
            view.setCameraType("Orthographic")
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if Gui:
        try:
            Gui.runCommand('Std_OrthographicCamera')
        except Exception:
            try:
                Gui.runCommand('Std_OrthographicCamera', 1)
            except Exception:
                pass


def isometric() -> None:
    """Orienta la cámara en la vista isométrica 3D estándar."""
    _safe_view_call('viewIsometric', 'Std_ViewIsometric', 'ViewIsometric')


def dimetric() -> None:
    """Orienta la cámara en la vista dimétrica 3D."""
    _safe_view_call('viewDimetric', 'Std_ViewDimetric', 'ViewDimetric')


def trimetric() -> None:
    """Orienta la cámara en la vista trimétrica 3D."""
    _safe_view_call('viewTrimetric', 'Std_ViewTrimetric', 'ViewTrimetric')


def front() -> None:
    """Orienta la cámara en la vista frontal."""
    _safe_view_call('viewFront', 'Std_ViewFront', 'ViewFront')


def top() -> None:
    """Orienta la cámara en la vista superior (planta)."""
    _safe_view_call('viewTop', 'Std_ViewTop', 'ViewTop')


def right() -> None:
    """Orienta la cámara en la vista lateral derecha."""
    _safe_view_call('viewRight', 'Std_ViewRight', 'ViewRight')


def left() -> None:
    """Orienta la cámara en la vista lateral izquierda."""
    _safe_view_call('viewLeft', 'Std_ViewLeft', 'ViewLeft')


def rear() -> None:
    """Orienta la cámara en la vista posterior (trasera)."""
    _safe_view_call('viewRear', 'Std_ViewRear', 'ViewRear')


def bottom() -> None:
    """Orienta la cámara en la vista inferior (desde abajo)."""
    _safe_view_call('viewBottom', 'Std_ViewBottom', 'ViewBottom')


def fit_all() -> None:
    """Encuadra y centra todo el modelo en la pantalla (Fit All)."""
    _safe_view_call('fitAll', 'Std_ViewFitAll', 'FitAll')


def fit_selection() -> None:
    """Enfoca la cámara en el objeto o geometría seleccionada."""
    _safe_view_call('fitSelection', 'Std_ViewFitSelection', 'FitSelection')


ZOOM_FACTOR = 0.85

def _apply_zoom(factor: float) -> None:
    view = _get_active_view()
    if view is None:
        return
    try:
        cam = view.getCameraNode() if hasattr(view, 'getCameraNode') else None
        if cam is None:
            return

        if hasattr(cam, 'height'):
            cam.height.setValue(cam.height.getValue() * factor)
        elif hasattr(cam, 'position') and hasattr(cam, 'focalDistance'):
            direction = view.getViewDirection()
            old_focal = cam.focalDistance.getValue()
            new_focal = old_focal * factor
            delta = old_focal - new_focal
            pos = cam.position.getValue()
            new_pos = [
                pos[0] + delta * direction.x,
                pos[1] + delta * direction.y,
                pos[2] + delta * direction.z,
            ]
            cam.position.setValue(new_pos)
            cam.focalDistance.setValue(new_focal)
        if hasattr(view, 'redraw'):
            view.redraw()
    except Exception:
        pass


def zoom_in() -> None:
    """Acerca la cámara (zoom in)."""
    _apply_zoom(ZOOM_FACTOR)


def zoom_out() -> None:
    """Aleja la cámara (zoom out)."""
    _apply_zoom(1.0 / ZOOM_FACTOR)


def rotate_left() -> None:
    """Gira la cámara hacia la izquierda alrededor del modelo."""
    view = _get_active_view()
    if view and hasattr(view, 'viewRotateLeft'):
        try:
            view.viewRotateLeft()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if Gui:
        try:
            Gui.runCommand('Std_ViewRotateLeft')
        except Exception:
            try:
                Gui.runCommand('Std_ViewRotateLeft', 0)
            except Exception:
                pass


def rotate_right() -> None:
    """Gira la cámara hacia la derecha alrededor del modelo."""
    view = _get_active_view()
    if view and hasattr(view, 'viewRotateRight'):
        try:
            view.viewRotateRight()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass
    if Gui:
        try:
            Gui.runCommand('Std_ViewRotateRight')
        except Exception:
            try:
                Gui.runCommand('Std_ViewRotateRight', 0)
            except Exception:
                pass


def rotate_up() -> None:
    """Inclina la cámara hacia arriba."""
    view = _get_active_view()
    if view and hasattr(view, 'viewRotateUp'):
        try:
            view.viewRotateUp()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass


def rotate_down() -> None:
    """Inclina la cámara hacia abajo."""
    view = _get_active_view()
    if view and hasattr(view, 'viewRotateDown'):
        try:
            view.viewRotateDown()
            if hasattr(view, 'redraw'):
                view.redraw()
            return
        except Exception:
            pass


try:
    from dictionary.moveview import MoveView as move_camera
except ImportError:
    try:
        from moveview import MoveView as move_camera
    except ImportError:
        def move_camera(*args, **kwargs):
            return None
