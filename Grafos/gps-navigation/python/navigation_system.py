"""
Módulo del Sistema de Navegación GPS.
Fachada que encapsula la lógica de negocio, validaciones y administración del mapa.
"""

from typing import List, Dict, Tuple, Optional
from models import WeightedGraph
from dijkstra import DijkstraRouter, RouteResult
from exceptions import (
    GPSNavigationError,
    CityNotFoundError,
    CityAlreadyExistsError,
    InvalidRouteError,
    NoPathFoundError
)


class GPSNavigationSystem:
    """
    Controlador principal del Sistema de Navegación GPS.
    Provee una API unificada para gestionar la red vial y consultar rutas óptimas.
    """

    def __init__(self):
        self.graph = WeightedGraph()
        self.router = DijkstraRouter(self.graph)

    def register_city(self, city_name: str) -> str:
        """Registra una nueva ciudad en el mapa."""
        return self.graph.add_city(city_name)

    def add_highway(
        self,
        origin: str,
        destination: str,
        time_minutes: float,
        bidirectional: bool = True
    ) -> None:
        """
        Agrega una autopista ponderada por tiempo entre dos ciudades.
        Si las ciudades no están registradas, lanza CityNotFoundError.
        """
        self.graph.add_highway(origin, destination, time_minutes, bidirectional)

    def find_fastest_route(self, origin: str, destination: str) -> RouteResult:
        """Calcula la ruta más rápida entre dos ciudades usando Dijkstra."""
        return self.router.find_fastest_route(origin, destination)

    def get_all_cities(self) -> List[str]:
        """Retorna todas las ciudades ordenadas alfabéticamente."""
        return self.graph.get_cities()

    def get_city_connections(self, city_name: str) -> Dict[str, float]:
        """Retorna las conexiones directas de una ciudad con sus tiempos de viaje."""
        return self.graph.get_neighbors(city_name)

    def get_all_highways(self) -> List[Tuple[str, str, float]]:
        """Retorna todas las autopistas registradas."""
        return self.graph.get_all_highways()

    def load_demo_data(self) -> Tuple[int, int]:
        """
        Carga una red vial de prueba representativa.
        Retorna (ciudades_agregadas, autopistas_agregadas).
        """
        demo_cities = [
            "Ciudad de México",
            "Puebla",
            "Querétaro",
            "Guadalajara",
            "San Luis Potosí",
            "Toluca",
            "Cuernavaca",
            "León",
            "Monterrey"
        ]

        # Registrar ciudades
        for city in demo_cities:
            self.graph.ensure_city(city)

        # Autopistas con tiempos realistas en minutos
        demo_routes = [
            ("Ciudad de México", "Toluca", 55),
            ("Ciudad de México", "Cuernavaca", 65),
            ("Ciudad de México", "Puebla", 120),
            ("Ciudad de México", "Querétaro", 150),
            ("Toluca", "Querétaro", 130),
            ("Querétaro", "San Luis Potosí", 135),
            ("Querétaro", "León", 110),
            ("León", "Guadalajara", 140),
            ("San Luis Potosí", "Guadalajara", 195),
            ("San Luis Potosí", "Monterrey", 310),
            ("Puebla", "Cuernavaca", 140),
        ]

        for orig, dest, minutes in demo_routes:
            self.graph.add_highway(orig, dest, minutes, bidirectional=True)

        return len(demo_cities), len(demo_routes)
