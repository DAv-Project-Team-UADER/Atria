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
    from .Horizontal_Dimension import Horizontal_Dimension
except ImportError:
    Horizontal_Dimension = None 

TraduceToEn = {
    # Horizontal Dimension
    'horizontal dimension':          Horizontal_Dimension,
    'create horizontal dimension':   Horizontal_Dimension,
    'add horizontal dimension':      Horizontal_Dimension,
    'insert horizontal dimension':   Horizontal_Dimension,
    'dimension horizontally':        Horizontal_Dimension,
    'horizontal measurement':        Horizontal_Dimension,
    'create horizontal measurement': Horizontal_Dimension,
}