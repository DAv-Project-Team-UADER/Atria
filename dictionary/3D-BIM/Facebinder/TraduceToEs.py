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
try:
    from .Facebinder import Facebinder
except ImportError:
    Facebinder = None

TraduceToEs = {
    # Atrapacaras
    'crear atrapacaras':             Facebinder,
    'atrapacaras':                   Facebinder,
    'facebinder':                    Facebinder,
    'crear facebinder':              Facebinder,
    'superficie desde caras':        Facebinder,
    'crear superficie desde caras':  Facebinder,
    'revestimiento de caras':        Facebinder,
    'crear revestimiento de caras':  Facebinder,
}