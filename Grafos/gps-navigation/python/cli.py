"""
Módulo de Interfaz de Consola (CLI) para el Sistema de Navegación GPS.
Maneja la interacción con el usuario, menús interactivos, formato de salida y captura de errores.
"""

import sys
from typing import Optional
from navigation_system import GPSNavigationSystem
from exceptions import (
    GPSNavigationError,
    CityNotFoundError,
    CityAlreadyExistsError,
    InvalidRouteError,
    NoPathFoundError
)


class ConsoleUI:
    """Gestiona la experiencia de usuario interactiva por consola."""

    def __init__(self, system: GPSNavigationSystem):
        self.system = system

    def _print_header(self, title: str) -> None:
        """Imprime un encabezado con formato estilizado."""
        width = 65
        print("\n" + "=" * width)
        print(f"  {title.upper()}".center(width))
        print("=" * width)

    def _print_divider(self) -> None:
        """Imprime un separador horizontal discreto."""
        print("-" * 65)

    def _format_time(self, minutes: float) -> str:
        """Convierte minutos a formato legible de horas y minutos."""
        total_mins = int(round(minutes))
        hours = total_mins // 60
        mins = total_mins % 60
        if hours > 0:
            return f"{minutes:.1f} min ({hours} h {mins:02d} min)"
        return f"{minutes:.1f} min"

    def display_cities(self) -> None:
        """Muestra la lista de ciudades registradas y sus conexiones viales."""
        self._print_header("Ciudades y Red de Autopistas")
        cities = self.system.get_all_cities()

        if not cities:
            print("\n [!] No hay ciudades registradas aún en el mapa.")
            print("     Utilice la opción 2 para agregar una ciudad o la opción 5 para cargar datos de prueba.")
            return

        print(f"\n Ciudades registradas en el sistema ({len(cities)} en total):\n")
        for idx, city in enumerate(cities, start=1):
            connections = self.system.get_city_connections(city)
            if connections:
                conns_str = ", ".join([f"{dest} ({self._format_time(time)})" for dest, time in connections.items()])
                print(f"  [{idx:02d}] {city}")
                print(f"       └── Conexiones directas: {conns_str}")
            else:
                print(f"  [{idx:02d}] {city} (Sin autopistas conectadas)")

        highways = self.system.get_all_highways()
        print(f"\n Total de autopistas en la red: {len(highways)}")

    def add_city_dialog(self) -> None:
        """Diálogo interactivo para registrar una nueva ciudad."""
        self._print_header("Registrar Nueva Ciudad")
        try:
            city_name = input(" Nombre de la ciudad a registrar: ").strip()
            if not city_name:
                print(" [!] Operación cancelada: El nombre no puede estar vacío.")
                return

            registered_name = self.system.register_city(city_name)
            print(f"\n [✓] Ciudad '{registered_name}' registrada exitosamente.")
        except CityAlreadyExistsError as e:
            print(f"\n [!] Aviso: {e}")
        except ValueError as e:
            print(f"\n [!] Error de validación: {e}")

    def add_highway_dialog(self) -> None:
        """Diálogo interactivo para registrar una nueva autopista entre dos ciudades."""
        self._print_header("Agregar Nueva Autopista")
        cities = self.system.get_all_cities()

        if len(cities) < 2:
            print("\n [!] Se necesitan al menos 2 ciudades registradas para crear una autopista.")
            print("     Actualmente registradas: " + (", ".join(cities) if cities else "Ninguna"))
            auto_load = input(" ¿Desea cargar el mapa de prueba con ciudades predeterminadas? (s/n): ").strip().lower()
            if auto_load == 's':
                c_cnt, h_cnt = self.system.load_demo_data()
                print(f"\n [✓] Mapa cargado con {c_cnt} ciudades y {h_cnt} autopistas.")
            else:
                return

        print("\n Ingrese los datos de la nueva autopista:")
        origin = input("  • Ciudad de origen: ").strip()
        if not origin:
            print(" [!] Operación cancelada: Origen inválido.")
            return

        # Verificar si origen existe, si no, dar opción de registrarlo
        if not self.system.graph.has_city(origin):
            crear = input(f"  [?] La ciudad '{origin}' no existe. ¿Desea registrarla ahora? (s/n): ").strip().lower()
            if crear == 's':
                self.system.graph.ensure_city(origin)
                print(f"  [✓] Ciudad '{origin}' registrada.")
            else:
                print(" [!] Operación cancelada.")
                return

        destination = input("  • Ciudad de destino: ").strip()
        if not destination:
            print(" [!] Operación cancelada: Destino inválido.")
            return

        # Verificar si destino existe
        if not self.system.graph.has_city(destination):
            crear = input(f"  [?] La ciudad '{destination}' no existe. ¿Desea registrarla ahora? (s/n): ").strip().lower()
            if crear == 's':
                self.system.graph.ensure_city(destination)
                print(f"  [✓] Ciudad '{destination}' registrada.")
            else:
                print(" [!] Operación cancelada.")
                return

        if self.system.graph._normalize(origin) == self.system.graph._normalize(destination):
            print(" [!] Error: Una autopista no puede conectar una ciudad consigo misma.")
            return

        # Solicitar tiempo con manejo seguro de entrada numérica
        time_minutes = None
        while time_minutes is None:
            time_raw = input("  • Tiempo de recorrido estimado (en minutos): ").strip()
            try:
                val = float(time_raw)
                if val <= 0:
                    print("    [!] El tiempo debe ser un número positivo mayor a 0 minutos. Intente de nuevo.")
                else:
                    time_minutes = val
            except ValueError:
                print("    [!] Entrada inválida. Por favor ingrese un número (ejemplo: 45 o 120.5).")

        bidir_raw = input("  • ¿La autopista es de doble sentido / bidireccional? (S/n): ").strip().lower()
        bidirectional = (bidir_raw != 'n')

        try:
            self.system.add_highway(origin, destination, time_minutes, bidirectional=bidirectional)
            sentido = "doble sentido (bidireccional)" if bidirectional else "sentido único"
            print(f"\n [✓] Autopista registrada con éxito:")
            print(f"     {origin} <--> {destination} ({self._format_time(time_minutes)}) [{sentido}]")
        except InvalidRouteError as e:
            print(f"\n [!] Error en la ruta: {e}")
        except CityNotFoundError as e:
            print(f"\n [!] Error: {e}")

    def query_route_dialog(self) -> None:
        """Diálogo interactivo para calcular y visualizar la ruta más rápida con Dijkstra."""
        self._print_header("Consultar Ruta Más Rápida (GPS)")
        cities = self.system.get_all_cities()

        if len(cities) < 2:
            print("\n [!] No hay suficientes ciudades en el sistema para calcular rutas.")
            print("     Agregue ciudades y autopistas o cargue los datos de prueba.")
            return

        print("\n Ciudades disponibles:")
        # Mostrar en columnas ordenadas
        for i, city in enumerate(cities, start=1):
            print(f"  [{i:02d}] {city}")

        print("\n Ingrese las ciudades a consultar:")
        origin_input = input("  • Ciudad de partida (Origen): ").strip()
        dest_input = input("  • Ciudad de llegada (Destino): ").strip()

        if not origin_input or not dest_input:
            print("\n [!] Debe ingresar ambas ciudades para calcular la ruta.")
            return

        try:
            # Invocar el router de Dijkstra
            result = self.system.find_fastest_route(origin_input, dest_input)

            self._print_divider()
            print(f"  RESULTADO DEL CÁLCULO DE RUTA GPS")
            self._print_divider()
            print(f"  • Origen:            {result.origin}")
            print(f"  • Destino:           {result.destination}")
            print(f"  • Tiempo Total:      {self._format_time(result.total_time_minutes)}")
            
            # Caso especial: Origen == Destino
            if result.origin == result.destination:
                print(f"  • Estado:            Ya se encuentra en el destino.")
                print(f"  • Recorrido:         [{result.origin}]")
                return

            # Reconstrucción del recorrido completo
            route_str = " ➔ ".join(result.path)
            print(f"  • Recorrido óptimo:  {route_str}")
            print(f"  • Número de paradas: {len(result.path) - 1} tramos")

            print("\n  DESGLOSE DETALLADO DEL VIAJE:")
            print("  " + "-" * 59)
            print(f"  {'#':<3} {'Tramo':<35} {'Tiempo':<10} {'Acumulado'}")
            print("  " + "-" * 59)
            for idx, seg in enumerate(result.segments, start=1):
                tramo = f"{seg.origin} ➔ {seg.destination}"
                print(
                    f"  {idx:<3} {tramo:<35} {seg.time_minutes:>5.1f} min   "
                    f"{seg.cumulative_time:>5.1f} min"
                )
            print("  " + "-" * 59)

        except CityNotFoundError as e:
            print(f"\n [!] Error de localización: {e}")
            print("     Verifique la ortografía con la lista de ciudades disponibles.")
        except NoPathFoundError as e:
            print(f"\n [!] Ruta no disponible: {e}")
            print("     Las ciudades seleccionadas pertenecen a componentes viales desconectados.")
        except GPSNavigationError as e:
            print(f"\n [!] Error en el sistema de navegación: {e}")

    def load_demo_dialog(self) -> None:
        """Carga una red vial representativa para pruebas inmediatas."""
        self._print_header("Cargar Red Vial de Prueba")
        num_cities, num_highways = self.system.load_demo_data()
        print(f"\n [✓] Se cargaron exitosamente:")
        print(f"     • {num_cities} ciudades (CDMX, Toluca, Puebla, Querétaro, GDL, MTY, etc.)")
        print(f"     • {num_highways} autopistas ponderadas por tiempo de traslado.")
        print("\n ¡Ahora puede consultar rutas entre estas ciudades!")

    def show_main_menu(self) -> None:
        """Muestra el menú principal y coordina la ejecución en bucle interactivo."""
        while True:
            self._print_header("Sistema de Navegación GPS - Menú Principal")
            print("  1. Ver todas las ciudades y mapa de autopistas")
            print("  2. Agregar nueva ciudad")
            print("  3. Agregar nueva ruta (autopista ponderada)")
            print("  4. Consultar ruta más rápida (Algoritmo Dijkstra)")
            print("  5. Cargar mapa de prueba predeterminado")
            print("  6. Salir")
            self._print_divider()

            try:
                option = input(" Seleccione una opción [1-6]: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n [✓] Saliendo del Sistema de Navegación GPS. ¡Buen viaje!\n")
                sys.exit(0)

            if option == "1":
                self.display_cities()
            elif option == "2":
                self.add_city_dialog()
            elif option == "3":
                self.add_highway_dialog()
            elif option == "4":
                self.query_route_dialog()
            elif option == "5":
                self.load_demo_dialog()
            elif option == "6":
                print("\n [✓] Saliendo del Sistema de Navegación GPS. ¡Buen viaje!\n")
                break
            else:
                print("\n [!] Opción no válida. Por favor elija un número del 1 al 6.")

            input("\n Presione [Enter] para continuar...")
