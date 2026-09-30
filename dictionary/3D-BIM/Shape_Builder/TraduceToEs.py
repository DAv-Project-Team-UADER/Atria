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

TraduceToEs = {
    # Constructor de formas
    'constructor de formas':       Shape_Builder,
    'abrir constructor de formas': Shape_Builder,
    'crear forma':                 Shape_Builder,
    'construir forma':             Shape_Builder,
    'crear forma geométrica':      Shape_Builder,
    'construir forma geométrica':  Shape_Builder,
    'construir cara':              Shape_Builder,
    'construir cascara':           Shape_Builder,
    'construir cáscara':           Shape_Builder,
    'construir solido':            Shape_Builder,
    'construir sólido':            Shape_Builder,
}