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


def ManageIFCElements():
    """
    Abre el "IFC Elements Manager", un panel que permite gestionar los nombres, los tipos de IFC y los materiales de todos los elementos BIM del modelo.
    Permite ordenar los objetos, renombrarlos y hacer cambios masivos (ej. asignar el mismo tipo IFC a varios objetos a la vez) antes de exportar el modelo a IFC.
    """
    Gui.runCommand('BIM_IfcElements', 0)


comandos = {
    'gestionar elementos ifc': ManageIFCElements,
    'administrar tipos ifc': ManageIFCElements,
    'gestor de elementos bim': ManageIFCElements,
    'asignar materiales ifc': ManageIFCElements,
    'help': ayuda
}
