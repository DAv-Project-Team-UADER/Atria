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


def BIMReport():
    """
    Es una herramienta para generar tablas de planificación (schedules) e informes 
    de datos a partir de un modelo BIM en FreeCAD. Utiliza un lenguaje de 
    consulta estructurado similar a SQL (dialecto BIM SQL) para seleccionar, filtrar, 
    agrupar y calcular datos o propiedades de los objetos, exportando el resultado 
    directamente a una hoja de cálculo (Spreadsheet). Permite concatenar 
    consultas a modo de "tubería" (pipeline) para flujos de trabajo complejos.
    """
    Gui.runCommand('Report_Create', 0)


comandos = {
    'crear informe bim': BIMReport,
    'generar reporte': BIMReport,
    'consultar modelo': BIMReport,
    'crear tabla de planificación': BIMReport,
    'help': ayuda
}
