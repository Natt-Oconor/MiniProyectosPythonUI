"""
Módulo de Modelado de Grafo Ponderado.
Representa ciudades (nodos) y autopistas (aristas ponderadas por tiempo en minutos).
"""

from typing import Dict, List, Tuple, Optional
from exceptions import CityNotFoundError, CityAlreadyExistsError, InvalidRouteError


class WeightedGraph:
    """
    Grafo Ponderado representado mediante Listas de Adyacencia (Diccionario de Diccionarios).
    
    Estructura interna:
        _adjacency[origen][destino] = tiempo_en_minutos
        
    Propiedades:
        - Soporta rutas dirigidas o bidireccionales.
        - Preserva nombres originales con normalización insensible a mayúsculas/espacios.
        - Los pesos representan tiempo en minutos (números flotantes positivos).
    """

    def __init__(self):
        # Mapea clave normalizada (lower, stripped) -> {clave_vecino_normalizada: tiempo_minutos}
        self._adjacency: Dict[str, Dict[str, float]] = {}
        # Mapea clave normalizada -> Nombre de presentación original
        self._display_names: Dict[str, str] = {}

    def _normalize(self, name: str) -> str:
        """Normaliza el nombre de una ciudad para búsquedas consistentes."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacío.")
        return " ".join(name.strip().split()).casefold()

    def add_city(self, name: str) -> str:
        """
        Agrega una nueva ciudad (nodo) al grafo.
        
        Args:
            name: Nombre de la ciudad.
            
        Returns:
            El nombre formateado registrado.
            
        Raises:
            CityAlreadyExistsError: Si la ciudad ya existe.
            ValueError: Si el nombre es vacío o inválido.
        """
        clean_name = " ".join(name.strip().split())
        key = self._normalize(clean_name)
        
        if key in self._adjacency:
            raise CityAlreadyExistsError(self._display_names[key])
            
        self._adjacency[key] = {}
        self._display_names[key] = clean_name
        return clean_name

    def ensure_city(self, name: str) -> str:
        """
        Obtiene la ciudad si existe, o la crea automáticamente si no existe.
        Útil al importar o registrar autopistas rápidamente.
        """
        clean_name = " ".join(name.strip().split())
        key = self._normalize(clean_name)
        if key not in self._adjacency:
            self._adjacency[key] = {}
            self._display_names[key] = clean_name
        return self._display_names[key]

    def has_city(self, name: str) -> bool:
        """Verifica si una ciudad existe en el grafo."""
        try:
            key = self._normalize(name)
            return key in self._adjacency
        except ValueError:
            return False

    def get_city_display_name(self, name: str) -> str:
        """Obtiene el nombre canónico registrado de una ciudad."""
        key = self._normalize(name)
        if key not in self._display_names:
            raise CityNotFoundError(name)
        return self._display_names[key]

    def add_highway(
        self,
        origin: str,
        destination: str,
        time_minutes: float,
        bidirectional: bool = True
    ) -> None:
        """
        Agrega o actualiza una autopista (arista ponderada) entre dos ciudades.
        
        Args:
            origin: Ciudad de partida.
            destination: Ciudad de llegada.
            time_minutes: Tiempo estimado en minutos (debe ser > 0).
            bidirectional: Si es True, permite transitar en ambos sentidos.
            
        Raises:
            InvalidRouteError: Si el tiempo es <= 0 o si origen == destino.
            CityNotFoundError: Si alguna ciudad no existe en el grafo.
        """
        key_u = self._normalize(origin)
        key_v = self._normalize(destination)

        if key_u not in self._adjacency:
            raise CityNotFoundError(origin)
        if key_v not in self._adjacency:
            raise CityNotFoundError(destination)

        if key_u == key_v:
            raise InvalidRouteError(
                f"No se puede crear una autopista con el mismo origen y destino ('{origin}')."
            )

        try:
            time_val = float(time_minutes)
        except (ValueError, TypeError):
            raise InvalidRouteError("El tiempo de viaje debe ser un valor numérico válido.")

        if time_val <= 0:
            raise InvalidRouteError(
                f"El tiempo de recorrido debe ser estrictamente mayor a 0 minutos (recibido: {time_val})."
            )

        # Asignar tiempo en lista de adyacencia
        self._adjacency[key_u][key_v] = time_val
        if bidirectional:
            self._adjacency[key_v][key_u] = time_val

    def get_cities(self) -> List[str]:
        """Retorna la lista de nombres de todas las ciudades registradas."""
        return sorted([self._display_names[k] for k in self._adjacency])

    def get_neighbors(self, city: str) -> Dict[str, float]:
        """
        Retorna un diccionario de {ciudad_vecina: tiempo_en_minutos} para una ciudad dada.
        
        Raises:
            CityNotFoundError: Si la ciudad no existe.
        """
        key = self._normalize(city)
        if key not in self._adjacency:
            raise CityNotFoundError(city)

        return {
            self._display_names[neighbor_key]: weight
            for neighbor_key, weight in self._adjacency[key].items()
        }

    def get_all_highways(self) -> List[Tuple[str, str, float]]:
        """
        Retorna la lista de todas las autopistas registradas en forma de tuplas
        (origen, destino, tiempo_minutos). Para rutas bidireccionales, solo incluye
        un sentido canónico para evitar duplicados en reportes.
        """
        seen_edges = set()
        routes = []

        for u_key, neighbors in self._adjacency.items():
            u_name = self._display_names[u_key]
            for v_key, weight in neighbors.items():
                v_name = self._display_names[v_key]
                # Si la arista es bidireccional con el mismo peso, consolidamos
                is_bidirectional = (
                    v_key in self._adjacency
                    and u_key in self._adjacency[v_key]
                    and self._adjacency[v_key][u_key] == weight
                )
                canonical_edge = tuple(sorted([u_key, v_key])) if is_bidirectional else (u_key, v_key)
                
                if canonical_edge not in seen_edges:
                    seen_edges.add(canonical_edge)
                    routes.append((u_name, v_name, weight))

        return routes

    def city_count(self) -> int:
        """Cantidad de ciudades (nodos)."""
        return len(self._adjacency)

    def highway_count(self) -> int:
        """Cantidad de autopistas (aristas únicas)."""
        return len(self.get_all_highways())
