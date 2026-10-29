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


def BIMTrash():
    """
    Permite mover los objetos seleccionados a un grupo especial denominado 
    "Trash" (Papelera). Si este grupo no existe en el documento en el 
    momento de ejecutar la acción, la herramienta lo crea automáticamente. 
    Ayuda a organizar y limpiar la jerarquía del modelo sin eliminar 
    permanentemente los elementos.
    """
    Gui.runCommand('BIM_Trash', 0)


comandos = {
    'mover a la papelera': BIMTrash,
    'enviar a la papelera': BIMTrash,
    'ocultar en papelera': BIMTrash,
    'descartar objetos': BIMTrash,
    'help': ayuda
}
