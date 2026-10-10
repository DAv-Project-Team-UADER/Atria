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
    print('Comandos disponibles en 2D-Drafting:')
    print('  punto                    - Crea un punto simple en el plano de trabajo')
    print('  línea                    - Crea una línea recta a partir de dos puntos')
    print('  rectángulo               - Crea un rectángulo a partir de dos puntos')
    print('  polígono                 - Crea un polígono regular a partir de un centro y un radio')
    print('  polilínea                - Crea una secuencia de líneas rectas que une varios puntos')
    print('  círculo                  - Crea un círculo a partir de un centro y un radio')
    print('  elipse                   - Crea una elipse inscrita en el rectángulo de dos puntos')
    print('  arco                     - Crea un arco circular desde centro, radio y ángulos')
    print('  arco de 3 puntos         - Crea un arco circular a partir de tres puntos')
    print('  b spline                 - Crea una curva que pasa por un conjunto de puntos')
    print('  curva de bezier          - Crea una curva de Bézier de grado número de puntos menos uno')
    print('  curva de bezier cúbica   - Crea una curva de Bézier de tercer grado desde cuatro puntos')
    print('  chaflán                  - Crea un redondeo, chaflán o borde recto entre dos bordes')
    print('  boceto                   - Crea un nuevo boceto en el plano de trabajo')
