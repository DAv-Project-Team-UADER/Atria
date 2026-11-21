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

"""Mapa de voz (ES) para la seccion Preferences."""

try:
    from .commands import open_preferences, open_voice_preferences, set_language_es, set_language_en
except ImportError:
    open_preferences = None
    open_voice_preferences = None
    set_language_es = None
    set_language_en = None

TraduceToEs = {
    'preferencias': open_preferences,
    'abrir preferencias': open_preferences,
    'configuracion': open_preferences,
    'configuración': open_preferences,
    'abrir configuracion': open_preferences,
    'abrir configuración': open_preferences,
    'ajustes': open_preferences,
    'opciones': open_preferences,
    'panel de preferencias': open_preferences,
    'configurar voz': open_voice_preferences,
    'preferencias de voz': open_voice_preferences,
    'idioma espanol': set_language_es,
    'idioma español': set_language_es,
    'idioma ingles': set_language_en,
    'idioma inglés': set_language_en,
}
