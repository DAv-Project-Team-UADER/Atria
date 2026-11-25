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

"""Mapa de voz (ES) para la seccion StatusBar."""

try:
    from .commands import toggle_status_bar, set_units_mm, set_units_m, set_units_in, show_status_message
except ImportError:
    toggle_status_bar = None
    set_units_mm = None
    set_units_m = None
    set_units_in = None
    show_status_message = None

TraduceToEs = {
    'barra de estado': toggle_status_bar,
    'alternar barra de estado': toggle_status_bar,
    'mostrar barra de estado': toggle_status_bar,
    'ocultar barra de estado': toggle_status_bar,
    'unidades milimetros': set_units_mm,
    'unidades milímetros': set_units_mm,
    'cambiar a milimetros': set_units_mm,
    'unidades metros': set_units_m,
    'cambiar a metros': set_units_m,
    'unidades pulgadas': set_units_in,
    'cambiar a pulgadas': set_units_in,
    'estado listo': show_status_message,
}
