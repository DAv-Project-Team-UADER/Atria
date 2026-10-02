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

# El nombre del módulo comienza con un número, por eso se usa importlib.
try:
    from importlib import import_module
    _module = import_module(".2DDrawing", __package__)
    TwoDDrawing = (
        getattr(_module, "TwoDDrawing", None)
        or getattr(_module, "Drawing2D", None)
        or getattr(_module, "_2DDrawing", None)
    )
except (ImportError, AttributeError, TypeError):
    TwoDDrawing = None

TraduceToEn = {
    # 2D Drawing
    '2d drawing':         TwoDDrawing,
    'create 2d drawing':  TwoDDrawing,
    'add 2d drawing':     TwoDDrawing,
    '2d plan':            TwoDDrawing,
    '2d view':            TwoDDrawing,
    'create 2d view':     TwoDDrawing,
}
