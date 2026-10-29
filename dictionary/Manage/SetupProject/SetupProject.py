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


def SetupProject():
    """
    Crea un proyecto IFC nativo en el documento actual. En el estándar IFC, 
    un proyecto (IfcProject) es el objeto raíz que engloba todo el contenido del 
    modelo (sitio, edificio, etc.). Es obligatorio tener al menos uno en cada 
    archivo IFC para poder exportarlo correctamente.
    """
    Gui.runCommand('BIM_Project', 0)


comandos = {
    'configurar proyecto bim': SetupProject,
    'crear proyecto ifc': SetupProject,
    'nuevo proyecto bim': SetupProject,
    'iniciar proyecto raíz': SetupProject,
    'help': ayuda
}
