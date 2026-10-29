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


def ManageDoorsAndWindows():
    """
    Abre el "BIM Windows Manager", un cuadro de diálogo que permite navegar y 
    modificar todas las ventanas y puertas del proyecto en un solo lugar. 
    Es más conveniente que editarlas una por una y asegura que todas tengan 
    configurados correctamente parámetros como etiqueta, dimensiones, descripción o material.
    """
    Gui.runCommand('BIM_Windows', 0)


comandos = {
    'gestionar puertas y ventanas': ManageDoorsAndWindows,
    'administrar ventanas': ManageDoorsAndWindows,
    'modificar aberturas': ManageDoorsAndWindows,
    'gestor de puertas': ManageDoorsAndWindows,
    'help': ayuda
}
