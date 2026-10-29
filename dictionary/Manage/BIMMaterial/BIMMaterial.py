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


def BIMMaterial():
    """
    Abre el cuadro de diálogo del Administrador de Materiales BIM. Permite crear 
    nuevos materiales físicos o multi-materiales (capas), y asignarlos de forma rápida 
    a los objetos seleccionados. Este sistema centraliza la definición de aspectos 
    visuales y propiedades físicas (como color, densidad, propiedades mecánicas y térmicas) 
    integrando los elementos del documento directamente en la Vista de Árbol para facilitar 
    la portabilidad del modelo.
    """
    Gui.runCommand('BIM_Material', 0)


comandos = {
    'asignar material bim': BIMMaterial,
    'crear material': BIMMaterial,
    'gestionar materiales': BIMMaterial,
    'administrar materiales': BIMMaterial,
    'editor de materiales': BIMMaterial,
    'help': ayuda
}
