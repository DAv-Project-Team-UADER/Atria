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


def BIMPreflight():
    """
    Ejecuta una serie de comprobaciones diagnósticas en el modelo BIM para asegurar 
    su calidad e integridad antes de exportarlo a formatos estándar como IFC. 
    Detecta problemas comunes de modelado, como objetos que no son sólidos coplanares, 
    elementos superpuestos, falta de materiales o geometría que no está asignada 
    correctamente a la estructura del edificio (Building / Storey).
    """
    Gui.runCommand('BIM_Preflight', 0)


comandos = {
    'comprobar modelo bim': BIMPreflight,
    'validar modelo': BIMPreflight,
    'ejecutar preflight': BIMPreflight,
    'diagnóstico del proyecto': BIMPreflight,
    'help': ayuda
}
