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

"""Comandos FreeCAD de la seccion Preferences."""

try:
    import FreeCAD
    import FreeCADGui
    import FreeCADGui as Gui
except ImportError:
    FreeCAD = None  # type: ignore[assignment]
    FreeCADGui = None  # type: ignore[assignment]
    Gui = None  # type: ignore[assignment]


def open_preferences():
    """Abre la ventana de configuración y preferencias de ATRIA / FreeCAD."""
    try:
        from GUIFreeCad.integration.launch_preferences import open_preferences as _open_atria_prefs
        return _open_atria_prefs()
    except Exception:
        if Gui and hasattr(Gui, "runCommand"):
            Gui.runCommand("Std_DlgPreferences", 0)
            return None


def open_voice_preferences():
    """Abre las preferencias de voz y reconocimiento de ATRIA."""
    return open_preferences()


def set_language_es():
    """Establece el idioma de ATRIA en español."""
    try:
        from GUIFreeCad.core.preferences import preferences
        from GUIFreeCad.core.language_code import LanguageCode
        preferences.SetLanguage = LanguageCode.Es
    except Exception:
        pass


def set_language_en():
    """Establece el idioma de ATRIA en inglés."""
    try:
        from GUIFreeCad.core.preferences import preferences
        from GUIFreeCad.core.language_code import LanguageCode
        preferences.SetLanguage = LanguageCode.En
    except Exception:
        pass
