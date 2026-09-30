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
    from .External_Reference import External_Reference
except ImportError:
    External_Reference = None

TraduceToEn = {
    # External Reference
    'external reference':                 External_Reference,
    'insert external reference':          External_Reference,
    'create external reference':          External_Reference,
    'add external reference':             External_Reference,
    'link object from another file':      External_Reference,
    'link object from external file':     External_Reference,
    'link external object':               External_Reference,
    'link document':                      External_Reference,
    'link external document':             External_Reference,
}