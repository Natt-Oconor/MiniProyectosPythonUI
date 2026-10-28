#!/usr/bin/env python3
"""
Punto de Entrada Principal del Mini-Proyecto: Sistema de Navegación GPS.
Ejecuta la interfaz de consola interactiva.
"""

from navigation_system import GPSNavigationSystem
from cli import ConsoleUI


def main():
    system = GPSNavigationSystem()
    # Opcional: Precargar datos de prueba para comodidad del evaluador
    system.load_demo_data()
    ui = ConsoleUI(system)
    ui.show_main_menu()


if __name__ == "__main__":
    main()
