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

import FreeCADGui as Gui
from ayuda import ayuda


def BIMWPView():
    """
    Permite alinear la cámara de la vista 3D actual de manera perpendicular 
    (ortogonal) al plano de trabajo (Working Plane) que se encuentre activo. 
    Esto facilita enormemente el dibujo, la medición y la edición de elementos 
    cuando se trabaja sobre planos inclinados, fachadas o caras específicas 
    del modelo, al situar la cuadrícula (grid) de frente al usuario.
    """
    Gui.runCommand('BIM_WPView', 0)


comandos = {
    'alinear vista a plano de trabajo': BIMWPView,
    'vista de plano de trabajo': BIMWPView,
    'mirar al plano activo': BIMWPView,
    'centrar cámara en cuadrícula': BIMWPView,
    'help': ayuda
}
