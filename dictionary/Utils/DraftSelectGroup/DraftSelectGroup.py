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


def DraftSelectGroup():
    """
    Selecciona de forma recursiva el contenido de un grupo o elemento contenedor 
    seleccionado (como Std Group, Draft Block, Arch BuildingPart, etc.). En lugar 
    de tener seleccionado el contenedor principal, la herramienta selecciona 
    automáticamente todos los elementos secundarios (hijos) contenidos dentro del mismo.
    """
    Gui.runCommand('Draft_SelectGroup', 0)


comandos = {
    'seleccionar contenido de grupo': DraftSelectGroup,
    'seleccionar elementos del grupo': DraftSelectGroup,
    'seleccionar hijos': DraftSelectGroup,
    'seleccionar interior del grupo': DraftSelectGroup,
    'help': ayuda
}
