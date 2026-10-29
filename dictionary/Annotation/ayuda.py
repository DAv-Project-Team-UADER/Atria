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

def ayuda():
    print('Comandos disponibles en Annotation:')
    print('  cota alineada       - Crea una cota alineada entre dos puntos o a lo largo de una arista')
    print('  cota horizontal     - Crea una cota horizontal entre dos puntos o a lo largo de una arista')
    print('  cota vertical       - Crea una cota vertical entre dos puntos o a lo largo de una arista')
    print('  dibujo 2d           - Crea un dibujo 2D con las vistas de sección (vista y corte)')
    print('  ejes                - Coloca un sistema de ejes de referencia en el documento')
    print('  sistema de ejes     - Combina varios ejes de referencia en un único sistema')
    print('  rejilla             - Crea una rejilla 2D editable (filas, columnas y celdas)')
    print('  sombreado           - Aplica un sombreado con patrón PAT sobre caras planas')
    print('  etiqueta            - Crea una etiqueta con línea de líder y flecha')
    print('  líder               - Crea una línea de referencia con flecha al final')
    print('  página nueva        - Crea una página TechDraw a partir de una plantilla SVG')
    print('  vista nueva         - Crea vistas TechDraw en una página a partir de objetos')
    print('  corte de sección    - Crea las líneas de corte de un plano de sección')
    print('  plano de sección    - Crea un plano de sección para generar vistas 2D')
    print('  vista de sección    - Crea la proyección 2D de lo que ve un plano de sección')
    print('  texto               - Crea un texto en la vista 3D o en la página TechDraw')
