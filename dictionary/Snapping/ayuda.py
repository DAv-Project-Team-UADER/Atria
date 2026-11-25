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

"""Ayuda de Snapping (Enganche) — Menú BIM → Snapping.

Explica en lenguaje sencillo qué permite hacer cada herramienta de enganche
y selección de plano de trabajo, y con qué frase de voz se invoca.
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
    content = """Comandos de plano de trabajo y enganche (Snapping):
  plano de trabajo        - Abre el panel para definir el plano de trabajo por caras, vértices o vistas rápidas
  plano superior          - Fija el plano de trabajo en posición superior (plano XY horizontal)
  plano frontal           - Fija el plano de trabajo en posición frontal (plano XZ vertical)
  plano lateral           - Fija el plano de trabajo en posición lateral (plano YZ vertical)
  alternar enganche       - Activa o desactiva de forma global los modos de enganche magnético (Snap)
  enganche a rejilla      - Activa o desactiva el enganche a los puntos de la cuadrícula
  enganche a extremo      - Engancha el cursor a los vértices y extremos de aristas y líneas
  enganche a punto medio  - Engancha el cursor al punto medio de aristas y segmentos
  enganche a centro       - Engancha el cursor al punto central de círculos, arcos y polígonos
  modo ortogonal          - Restringe el movimiento del cursor a ángulos ortogonales (0°, 90°, 180°, 270°)
  bloquear enganche       - Bloquea o congela la coordenada de referencia de enganche actual

Sinónimos y frases de voz:
  plano de trabajo:
    - definir plano de trabajo, seleccionar plano, configurar plano
  plano superior:
    - plano de trabajo superior, fijar plano arriba, plano de arriba
  plano frontal:
    - plano de trabajo frontal, vista frontal, fijar plano frontal
  plano lateral:
    - plano de trabajo lateral, vista de plano lateral, fijar plano lateral
  alternar enganche:
    - activar enganche, desactivar enganche, modo snap"""
    show_help_dialog("Enganche", content)
