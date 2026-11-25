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


def BIMSetup():
    """
    Ofrece una versión simplificada de las preferencias, reuniendo las configuraciones 
    más utilizadas para el trabajo BIM en una sola pantalla. Cualquier cambio realizado 
    aquí tiene el mismo efecto que cambiar la configuración correspondiente en las 
    Preferencias generales de FreeCAD.
    """
    Gui.runCommand('BIM_Setup', 0)


comandos = {
    'abrir configuración bim': BIMSetup,
    'configuración bim': BIMSetup,
    'preferencias bim': BIMSetup,
    'ajustes bim': BIMSetup,
    'help': ayuda
}
