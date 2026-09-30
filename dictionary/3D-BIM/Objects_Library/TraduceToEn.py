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
    from .Objects_Library import Objects_Library
except ImportError:
    Objects_Library = None  

TraduceToEn = {
    # Objects Library
    'objects library':                  Objects_Library,
    'object library':                   Objects_Library,
    'open objects library':             Objects_Library,
    'open object library':              Objects_Library,
    'insert library object':            Objects_Library,
    'add library object':               Objects_Library,
    'insert object from library':       Objects_Library,
    'insert furniture':                 Objects_Library,
    'add furniture':                    Objects_Library,
    'insert equipment':                 Objects_Library,
    'add equipment':                    Objects_Library,
}