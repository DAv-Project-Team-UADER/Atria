# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Ayuda de Vistas y Cámara — Menú ATRIA → Vistas.

Explica en lenguaje sencillo cómo cambiar de perspectiva, orientar la cámara
y navegar el modelo 3D por voz o clics.
"""

from __future__ import annotations

try:
    from dictionary._help_gui import show_help_dialog
except ImportError:
    try:
        from .._help_gui import show_help_dialog
    except ImportError:
        def show_help_dialog(title: str, content: str) -> None:
            print(f"=== Ayuda: {title} ===")
            print(content)


def ayuda() -> None:
    content = """Comandos de Cámara y Perspectiva:
  perspectiva             - Activa la cámara con perspectiva cónica (3D realista con profundidad)
  ortogonal               - Activa la cámara ortogonal/paralela (sin punto de fuga, para dibujo técnico)

Vistas estándar:
  isometrica              - Orienta el modelo en la vista isométrica 3D clásica
  frontal                 - Orienta la cámara frente a la fachada principal (plano XZ)
  superior                - Orienta la cámara desde arriba en vista de planta (plano XY)
  derecha                 - Vista lateral derecha (plano YZ)
  izquierda               - Vista lateral izquierda
  posterior               - Vista trasera o posterior
  inferior                - Vista desde abajo

Encuadre y Zoom:
  centrar vista           - Encuadra y ajusta todo el modelo en la pantalla (Fit All)
  enfocar seleccion       - Enfoca y acerca la cámara al objeto que tengas seleccionado
  acercar                 - Acerca la cámara (Zoom In)
  alejar                  - Aleja la cámara (Zoom Out)

Rotación y Movimiento:
  girar izquierda         - Rota la cámara hacia la izquierda alrededor del modelo
  girar derecha           - Rota la cámara hacia la derecha alrededor del modelo
  girar arriba            - Inclina la cámara hacia arriba
  girar abajo             - Inclina la cámara hacia abajo
  mover camara            - Pide coordenadas y centra la cámara exactamente en ese punto"""
    show_help_dialog("Vistas y Cámara", content)
