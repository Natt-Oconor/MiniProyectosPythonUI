"""
Módulo de Excepciones Personalizadas para el Sistema de Navegación GPS.
Define la jerarquía de errores para un manejo robusto de casos límite.
"""

class GPSNavigationError(Exception):
    """Clase base para todas las excepciones del sistema de navegación GPS."""
    pass

class CityNotFoundError(GPSNavigationError):
    """Se lanza cuando se intenta operar con una ciudad que no existe en el grafo."""
    def __init__(self, city_name: str):
        super().__init__(f"La ciudad '{city_name}' no existe en el mapa de navegación.")
        self.city_name = city_name

class CityAlreadyExistsError(GPSNavigationError):
    """Se lanza cuando se intenta registrar una ciudad con un nombre ya existente."""
    def __init__(self, city_name: str):
        super().__init__(f"La ciudad '{city_name}' ya está registrada en el sistema.")
        self.city_name = city_name

class InvalidRouteError(GPSNavigationError):
    """Se lanza cuando los parámetros de una autopista son inválidos (peso <= 0, auto-ciclos, etc.)."""
    pass

class NoPathFoundError(GPSNavigationError):
    """Se lanza cuando no existe ninguna conexión terrestre entre dos ciudades."""
    def __init__(self, origin: str, destination: str):
        super().__init__(f"No existe ninguna ruta disponible entre '{origin}' y '{destination}'.")
        self.origin = origin
        self.destination = destination
