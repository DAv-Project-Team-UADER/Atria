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
    from .Shape_Builder import Shape_Builder
except ImportError:
    Shape_Builder = None    

TraduceToEn = {
    # Shape Builder
    'shape builder':             Shape_Builder,
    'open shape builder':        Shape_Builder,
    'create shape':              Shape_Builder,
    'build shape':               Shape_Builder,
    'create geometric shape':    Shape_Builder,
    'build geometric shape':     Shape_Builder,
    'build face':                Shape_Builder,
    'build shell':               Shape_Builder,
    'build solid':               Shape_Builder,
}