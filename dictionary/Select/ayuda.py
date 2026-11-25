# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)

"""Ayuda contextual para la sección Selección."""

def ayuda():
    """Muestra la ayuda contextual de Selección."""
    try:
        from GUIFreeCad.ui.HelpDialog import HelpDialog
        dlg = HelpDialog.show_help_for_category("Select")
        return dlg
    except Exception:
        pass
    print("=== AYUDA: SELECCIÓN DE OBJETOS ===")
    print("- 'avanzar' / 'siguiente': Navega al siguiente objeto en el documento y lo enfoca en pantalla.")
    print("- 'retroceder' / 'anterior': Navega al objeto anterior en el documento.")
    print("- 'seleccionar': Selecciona / confirma la selección del objeto actual.")
    print("- 'deseleccionar': Quita el objeto actual de la selección.")
    print("- 'seleccionar todos': Selecciona todos los objetos creados.")
    print("- 'deseleccionar todos' / 'limpiar selección': Deselecciona todos los objetos.")
    print("- 'editar': Pone el objeto seleccionado en modo de edición interactiva.")
    print("- 'borrar' / 'eliminar': Elimina el objeto seleccionado del documento.")
    print("- 'volver' / 'subir': Regresa al menú anterior.")
