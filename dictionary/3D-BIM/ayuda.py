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
    print('Comandos disponibles en 3D-BIM:')
    print('  crear sitio                     - Crea el emplazamiento o terreno del proyecto y agrupa los edificios')
    print('  crear edificio                  - Crea el grupo Edificio que organiza los niveles del modelo')
    print('  crear nivel                     - Crea un nivel o planta que agrupa objetos y comparte su altura')
    print('  crear espacio                   - Define el volumen de un ambiente y calcula su área de piso')
    print('  crear muro                      - Construye un muro desde cero o sobre una línea, cara o boceto base')
    print('  crear muro cortina              - Subdivide una cara base en montantes, travesaños y paneles')
    print('  crear columna                   - Crea un elemento estructural vertical (columna o pilar)')
    print('  crear viga                      - Crea un elemento estructural horizontal entre dos puntos')
    print('  crear losa                      - Crea una losa horizontal extruida desde una forma plana')
    print('  crear cubierta                  - Crea un techo inclinado paramétrico desde un contorno cerrado')
    print('  crear techo                     - Crea un techo inclinado con pendiente y voladizo por borde')
    print('  crear escalera                  - Crea escaleras rectas, con descansillo o con largueros')
    print('  crear marco                     - Extruye un perfil a lo largo de un trazado (barandillas, entramados)')
    print('  crear armadura                  - Crea una celosía (truss) paramétrica desde una línea o desde cero')
    print('  crear cerca                     - Repite un poste y un tramo de cerca a lo largo de una trayectoria')
    print('  crear panel                     - Crea un panel paramétrico desde un contorno 2D, liso o corrugado')
    print('  crear equipamiento              - Inserta muebles, equipos o electrodomésticos no estructurales')
    print('  crear armadura personalizada    - Coloca barras de refuerzo desde un boceto sobre la estructura')
    print('  crear ventana                   - Inserta una ventana sobre un muro y genera la abertura')
    print('  crear puerta                    - Inserta una puerta sobre un muro y genera la abertura')
    print('  crear tubo                      - Crea una tubería recta o a partir de un contorno base')
    print('  crear conector                  - Une dos o tres tubos en esquina o en T con radio de curvatura')
    print('  crear caja                      - Crea una caja de Part definiendo sus dimensiones con cuatro clics')
    print('  convertir en componente         - Convierte un objeto de Part en un componente Arch')
    print('  insertar referencia externa     - Enlaza un objeto que vive en otro archivo de FreeCAD')
    print('  crear atrapacaras               - Crea una superficie paramétrica a partir de las caras seleccionadas')
    print('  insertar objeto de biblioteca   - Abre la biblioteca de objetos (mobiliario y equipamiento)')
    print('  crear perfil                    - Crea un perfil paramétrico 2D para extruir (C, H, R, U, L, T)')
    print('  constructor de formas           - Arma aristas, alambres, caras, cáscaras y sólidos desde primitivas')
    print('  agregar refuerzo de viga        - Arma la viga: estribos y armaduras superior, inferior y de corte')
    print('  agregar refuerzo de columna     - Arma la columna: estribos y armaduras principales y secundarias')
    print('  agregar refuerzo de zapata      - Arma la zapata: malla de barras y columnas sobre ella')
    print('  agregar refuerzo de losa        - Arma la losa: mallado de barras en ambas direcciones')
    print('  crear armadura doblada          - Crea barras de refuerzo dobladas dentro de una estructura')
    print('  crear armadura helicoidal       - Crea una barra de refuerzo helicoidal dentro de una estructura')
    print('  crear armadura en L             - Crea barras de refuerzo con forma de L dentro de una estructura')
    print('  crear armadura recta            - Crea barras de refuerzo rectas dentro de una estructura')
    print('  crear estribo                   - Crea estribos (lazos cerrados) dentro de una estructura')
    print('  crear armadura en U             - Crea barras de refuerzo con forma de U dentro de una estructura')
