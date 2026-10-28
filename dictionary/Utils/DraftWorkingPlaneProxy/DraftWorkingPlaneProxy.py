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


def DraftWorkingPlaneProxy():
    """
    Permite guardar el estado actual del plano de trabajo (Working Plane) y la vista 
    de la cámara (dirección de la vista) en un objeto "Proxy". Al seleccionar este 
    objeto en la Vista de Árbol posteriormente, se restaura automáticamente esa misma 
    orientación del plano y vista guardados, facilitando cambiar rápidamente entre 
    diferentes áreas u orientaciones de trabajo complejas dentro del proyecto.
    """
    Gui.runCommand('Draft_WorkingPlaneProxy', 0)


comandos = {
    'crear proxy de plano de trabajo': DraftWorkingPlaneProxy,
    'guardar plano de trabajo': DraftWorkingPlaneProxy,
    'guardar vista de trabajo': DraftWorkingPlaneProxy,
    'crear estado de plano': DraftWorkingPlaneProxy,
    'help': ayuda
}
