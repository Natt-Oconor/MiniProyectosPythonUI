"""
Módulo del Algoritmo de Dijkstra con Reconstrucción de Rutas.
Encuentra el camino de costo mínimo (tiempo) entre dos ciudades en un grafo ponderado.
"""

import heapq
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from models import WeightedGraph
from exceptions import CityNotFoundError, NoPathFoundError


@dataclass
class RouteSegment:
    """Representa un tramo individual de la ruta calculada."""
    origin: str
    destination: str
    time_minutes: float
    cumulative_time: float


@dataclass
class RouteResult:
    """Resultado completo del cálculo de la ruta más rápida."""
    origin: str
    destination: str
    total_time_minutes: float
    path: List[str]
    segments: List[RouteSegment]
    is_reachable: bool


class DijkstraRouter:
    """
    Calculador de rutas mínimas utilizando el Algoritmo de Dijkstra con cola de prioridad (Min-Heap).
    
    Complejidad Temporal: O((V + E) * log(V))
        - V = número de ciudades (nodos)
        - E = número de autopistas (aristas)
    Complejidad Espacial: O(V)
    """

    def __init__(self, graph: WeightedGraph):
        self._graph = graph

    def find_fastest_route(self, origin: str, destination: str) -> RouteResult:
        """
        Ejecuta el algoritmo de Dijkstra para encontrar la ruta con menor tiempo en minutos
        entre la ciudad de origen y la de destino, reconstruyendo el camino completo.

        Args:
            origin: Nombre de la ciudad de partida.
            destination: Nombre de la ciudad de llegada.

        Returns:
            RouteResult: Objeto con el tiempo total, lista de ciudades en orden y detalle de tramos.

        Raises:
            CityNotFoundError: Si alguna ciudad no existe en el grafo.
            NoPathFoundError: Si no existe camino conexo entre ambas ciudades.
        """
        # 1. Validación de existencia de ciudades
        if not self._graph.has_city(origin):
            raise CityNotFoundError(origin)
        if not self._graph.has_city(destination):
            raise CityNotFoundError(destination)

        origin_name = self._graph.get_city_display_name(origin)
        dest_name = self._graph.get_city_display_name(destination)
        origin_key = self._graph._normalize(origin)
        dest_key = self._graph._normalize(destination)

        # 2. Caso límite: La ciudad de origen es igual a la ciudad de destino
        if origin_key == dest_key:
            return RouteResult(
                origin=origin_name,
                destination=dest_name,
                total_time_minutes=0.0,
                path=[origin_name],
                segments=[],
                is_reachable=True
            )

        # 3. Inicialización de estructuras de datos de Dijkstra
        # distances guarda la distancia mínima conocida desde el origen hasta cada nodo
        all_cities = [self._graph._normalize(c) for c in self._graph.get_cities()]
        distances: Dict[str, float] = {city: float('inf') for city in all_cities}
        distances[origin_key] = 0.0

        # previous guarda el predecesor óptimo de cada nodo para reconstruir el camino
        previous: Dict[str, Optional[str]] = {city: None for city in all_cities}

        # Cola de prioridad (Min-Heap) que almacena tuplas: (distancia_acumulada, clave_nodo)
        priority_queue: List[Tuple[float, str]] = []
        heapq.heappush(priority_queue, (0.0, origin_key))

        # Conjunto de nodos ya procesados (asentados) para optimizar
        visited = set()

        # 4. Ciclo principal de exploración Dijkstra
        while priority_queue:
            current_dist, current_key = heapq.heappop(priority_queue)

            # Si ya encontramos la distancia mínima al destino, podemos terminar tempranamente
            if current_key == dest_key:
                break

            # Si el nodo ya fue procesado con una distancia menor, descartar entrada obsoleta
            if current_key in visited:
                continue
            visited.add(current_key)

            # Si la distancia extraída es mayor a la ya registrada, continuar
            if current_dist > distances[current_key]:
                continue

            # Explorar vecinos adyacentes a través del grafo
            neighbors = self._graph._adjacency.get(current_key, {})
            for neighbor_key, travel_time in neighbors.items():
                if neighbor_key in visited:
                    continue

                new_dist = current_dist + travel_time

                # Paso de Relajación:
                # Si encontramos un camino más rápido hacia neighbor_key, actualizamos
                if new_dist < distances[neighbor_key]:
                    distances[neighbor_key] = new_dist
                    previous[neighbor_key] = current_key
                    heapq.heappush(priority_queue, (new_dist, neighbor_key))

        # 5. Validación de alcanzabilidad (caso grafo inconexo)
        if distances[dest_key] == float('inf'):
            raise NoPathFoundError(origin_name, dest_name)

        # 6. Reconstrucción del camino desde el destino hacia el origen
        reconstructed_keys: List[str] = []
        curr: Optional[str] = dest_key
        while curr is not None:
            reconstructed_keys.append(curr)
            curr = previous[curr]

        # Invertir para obtener el orden natural: origen -> destino
        reconstructed_keys.reverse()

        # Convertir claves a nombres para presentación y construir detalle de tramos
        path = [self._graph._display_names[k] for k in reconstructed_keys]
        segments: List[RouteSegment] = []
        accumulated = 0.0

        for i in range(len(reconstructed_keys) - 1):
            u_key = reconstructed_keys[i]
            v_key = reconstructed_keys[i + 1]
            seg_time = self._graph._adjacency[u_key][v_key]
            accumulated += seg_time
            segments.append(
                RouteSegment(
                    origin=self._graph._display_names[u_key],
                    destination=self._graph._display_names[v_key],
                    time_minutes=seg_time,
                    cumulative_time=accumulated
                )
            )

        return RouteResult(
            origin=origin_name,
            destination=dest_name,
            total_time_minutes=distances[dest_key],
            path=path,
            segments=segments,
            is_reachable=True
        )
