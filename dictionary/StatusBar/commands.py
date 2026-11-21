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

"""Comandos FreeCAD de la seccion StatusBar."""

try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None  # type: ignore[assignment]
    FreeCADGui = None  # type: ignore[assignment]
    Gui = None  # type: ignore[assignment]


def toggle_status_bar():
    """Muestra u oculta la barra de estado de FreeCAD."""
    if Gui and hasattr(Gui, "runCommand"):
        Gui.runCommand("Std_ToggleStatusBar", 0)


def set_units_mm():
    """Configura el sistema de unidades en Milímetros estándar."""
    if FreeCAD and hasattr(FreeCAD, "ParamGet"):
        try:
            FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 0)
        except Exception:
            pass


def set_units_m():
    """Configura el sistema de unidades en Metros (MKS)."""
    if FreeCAD and hasattr(FreeCAD, "ParamGet"):
        try:
            FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 1)
        except Exception:
            pass


def set_units_in():
    """Configura el sistema de unidades en Pulgadas (UScs)."""
    if FreeCAD and hasattr(FreeCAD, "ParamGet"):
        try:
            FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 2)
        except Exception:
            pass


def show_status_message(message: str = "ATRIA listo"):
    """Muestra un mensaje en la barra de estado de FreeCAD."""
    if Gui and hasattr(Gui, "showStatusMessage"):
        Gui.showStatusMessage(str(message))
