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


def ManageIFCQuantities():
    """
    Abre el IFC Quantities Manager, que permite comprobar las cantidades explícitas 
    adjuntas a los objetos para su exportación a IFC (como Ancho, Altura o Área). 
    Muestra señales de advertencia junto a valores en cero notificando posibles 
    problemas antes de exportar, y permite corregir estas medidas directamente.
    """
    Gui.runCommand('BIM_IfcQuantities', 0)


comandos = {
    'gestionar cantidades ifc': ManageIFCQuantities,
    'administrar medidas ifc': ManageIFCQuantities,
    'verificar cantidades': ManageIFCQuantities,
    'gestor de cantidades bim': ManageIFCQuantities,
    'help': ayuda
}
