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


def BIMIFCProperties():
    """
    Permite gestionar y asignar propiedades IFC a los objetos dentro de un modelo BIM. 
    Facilita la adición de conjuntos de propiedades (Property Sets o Psets) predefinidos 
    o la creación de propiedades personalizadas para cumplir con los requerimientos 
    específicos del proyecto.
    """
    Gui.runCommand('BIM_IfcProperties', 0)


comandos = {
    'gestionar propiedades ifc': BIMIFCProperties,
    'administrar propiedades ifc': BIMIFCProperties,
    'asignar propiedades bim': BIMIFCProperties,
    'configurar psets': BIMIFCProperties,
    'help': ayuda
}
