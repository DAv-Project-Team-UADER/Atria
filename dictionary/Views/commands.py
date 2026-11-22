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


def perspective() -> None:
    """Activa la cámara con perspectiva cónica (3D realista con profundidad)."""
    if Gui:
        try:
            Gui.runCommand('Std_PerspectiveCamera', 1)
        except Exception:
            pass


def orthographic() -> None:
    """Activa la cámara ortogonal / paralela (sin distorsión de perspectiva, ideal para planos técnicos)."""
    if Gui:
        try:
            Gui.runCommand('Std_OrthographicCamera', 1)
        except Exception:
            pass


def isometric() -> None:
    """Orienta la cámara en la vista isométrica 3D estándar."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewIsometric', 0)
        except Exception:
            pass


def front() -> None:
    """Orienta la cámara en la vista frontal."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewFront', 0)
        except Exception:
            pass


def top() -> None:
    """Orienta la cámara en la vista superior (planta)."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewTop', 0)
        except Exception:
            pass


def right() -> None:
    """Orienta la cámara en la vista lateral derecha."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewRight', 0)
        except Exception:
            pass


def left() -> None:
    """Orienta la cámara en la vista lateral izquierda."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewLeft', 0)
        except Exception:
            pass


def rear() -> None:
    """Orienta la cámara en la vista posterior (trasera)."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewRear', 0)
        except Exception:
            pass


def bottom() -> None:
    """Orienta la cámara en la vista inferior (desde abajo)."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewBottom', 0)
        except Exception:
            pass


def fit_all() -> None:
    """Encuadra y centra todo el modelo en la pantalla (Fit All)."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewFitAll', 0)
        except Exception:
            pass


def fit_selection() -> None:
    """Enfoca la cámara en el objeto o geometría seleccionada."""
    if Gui:
        try:
            Gui.runCommand('Std_ViewFitSelection', 0)
        except Exception:
            pass


ZOOM_FACTOR = 0.85

def _apply_zoom(factor: float) -> None:
    if not Gui:
        return
    try:
        view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
        if view is None and hasattr(Gui, 'activeView'):
            view = Gui.activeView()
        if view is None:
            return

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
    if not Gui:
        return
    try:
        view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
        if view is None and hasattr(Gui, 'activeView'):
            view = Gui.activeView()
        if view and hasattr(view, 'viewRotateLeft'):
            view.viewRotateLeft()
        else:
            Gui.runCommand('Std_ViewRotateLeft', 0)
    except Exception:
        pass


def rotate_right() -> None:
    """Gira la cámara hacia la derecha alrededor del modelo."""
    if not Gui:
        return
    try:
        view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
        if view is None and hasattr(Gui, 'activeView'):
            view = Gui.activeView()
        if view and hasattr(view, 'viewRotateRight'):
            view.viewRotateRight()
        else:
            Gui.runCommand('Std_ViewRotateRight', 0)
    except Exception:
        pass


def rotate_up() -> None:
    """Inclina la cámara hacia arriba."""
    if not Gui:
        return
    try:
        view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
        if view is None and hasattr(Gui, 'activeView'):
            view = Gui.activeView()
        if view and hasattr(view, 'viewRotateUp'):
            view.viewRotateUp()
    except Exception:
        pass


def rotate_down() -> None:
    """Inclina la cámara hacia abajo."""
    if not Gui:
        return
    try:
        view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
        if view is None and hasattr(Gui, 'activeView'):
            view = Gui.activeView()
        if view and hasattr(view, 'viewRotateDown'):
            view.viewRotateDown()
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
