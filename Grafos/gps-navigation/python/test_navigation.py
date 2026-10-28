"""
Suite de Pruebas Unitarias para el Sistema de Navegación GPS.
Cubre todos los criterios de la rúbrica: Grafo, Dijkstra, reconstrucción y casos límite.
"""

import unittest
from models import WeightedGraph
from dijkstra import DijkstraRouter
from exceptions import (
    CityNotFoundError,
    CityAlreadyExistsError,
    InvalidRouteError,
    NoPathFoundError
)


class TestWeightedGraph(unittest.TestCase):
    """Pruebas para la estructura de datos del Grafo Ponderado."""

    def setUp(self):
        self.graph = WeightedGraph()

    def test_add_city_success(self):
        """Verifica que una ciudad se agregue correctamente."""
        name = self.graph.add_city("Madrid")
        self.assertEqual(name, "Madrid")
        self.assertTrue(self.graph.has_city("Madrid"))
        self.assertTrue(self.graph.has_city("madrid"))  # Insensible a mayúsculas
        self.assertEqual(self.graph.city_count(), 1)

    def test_add_duplicate_city_raises_error(self):
        """Verifica que intentar agregar una ciudad duplicada lance CityAlreadyExistsError."""
        self.graph.add_city("Barcelona")
        with self.assertRaises(CityAlreadyExistsError):
            self.graph.add_city("Barcelona")
        with self.assertRaises(CityAlreadyExistsError):
            self.graph.add_city("  barcelona  ")

    def test_add_empty_city_name_raises_error(self):
        """Verifica que nombres vacíos o solo espacios sean rechazados."""
        with self.assertRaises(ValueError):
            self.graph.add_city("")
        with self.assertRaises(ValueError):
            self.graph.add_city("   ")

    def test_add_highway_bidirectional(self):
        """Verifica la creación de autopista de doble sentido."""
        self.graph.add_city("A")
        self.graph.add_city("B")
        self.graph.add_highway("A", "B", 45.0, bidirectional=True)

        self.assertEqual(self.graph.get_neighbors("A")["B"], 45.0)
        self.assertEqual(self.graph.get_neighbors("B")["A"], 45.0)

    def test_add_highway_directed(self):
        """Verifica la creación de autopista en un solo sentido."""
        self.graph.add_city("A")
        self.graph.add_city("B")
        self.graph.add_highway("A", "B", 60.0, bidirectional=False)

        self.assertIn("B", self.graph.get_neighbors("A"))
        self.assertNotIn("A", self.graph.get_neighbors("B"))

    def test_add_highway_invalid_time(self):
        """Verifica que tiempos <= 0 o no numéricos lancen InvalidRouteError."""
        self.graph.add_city("A")
        self.graph.add_city("B")
        with self.assertRaises(InvalidRouteError):
            self.graph.add_highway("A", "B", 0)
        with self.assertRaises(InvalidRouteError):
            self.graph.add_highway("A", "B", -15.5)
        with self.assertRaises(InvalidRouteError):
            self.graph.add_highway("A", "B", "invalido")

    def test_add_highway_self_loop(self):
        """Verifica que una ciudad no pueda conectarse a sí misma."""
        self.graph.add_city("A")
        with self.assertRaises(InvalidRouteError):
            self.graph.add_highway("A", "A", 30)

    def test_add_highway_nonexistent_city(self):
        """Verifica que ciudades no registradas lancen CityNotFoundError."""
        self.graph.add_city("A")
        with self.assertRaises(CityNotFoundError):
            self.graph.add_highway("A", "Inexistente", 50)


class TestDijkstraRouter(unittest.TestCase):
    """Pruebas para el algoritmo de Dijkstra y reconstrucción de rutas."""

    def setUp(self):
        self.graph = WeightedGraph()
        self.router = DijkstraRouter(self.graph)

    def test_direct_route(self):
        """Ruta directa entre dos nodos conectados."""
        self.graph.add_city("A")
        self.graph.add_city("B")
        self.graph.add_highway("A", "B", 50.0)

        result = self.router.find_fastest_route("A", "B")
        self.assertEqual(result.total_time_minutes, 50.0)
        self.assertEqual(result.path, ["A", "B"])
        self.assertEqual(len(result.segments), 1)

    def test_shortest_path_not_fewest_hops(self):
        """
        Verifica que Dijkstra elija el camino con menor tiempo total,
        incluso si tiene más paradas intermedias:
        Camino 1: A -> D (100 min, 1 tramo)
        Camino 2: A -> B -> C -> D (20 + 30 + 20 = 70 min, 3 tramos)
        El algoritmo debe elegir Camino 2.
        """
        for city in ["A", "B", "C", "D"]:
            self.graph.add_city(city)

        # Camino directo más largo
        self.graph.add_highway("A", "D", 100.0)
        # Camino indirecto más rápido
        self.graph.add_highway("A", "B", 20.0)
        self.graph.add_highway("B", "C", 30.0)
        self.graph.add_highway("C", "D", 20.0)

        result = self.router.find_fastest_route("A", "D")
        self.assertEqual(result.total_time_minutes, 70.0)
        self.assertEqual(result.path, ["A", "B", "C", "D"])
        self.assertEqual(len(result.segments), 3)

        # Verificar tiempos acumulados en los segmentos
        self.assertEqual(result.segments[0].cumulative_time, 20.0)
        self.assertEqual(result.segments[1].cumulative_time, 50.0)
        self.assertEqual(result.segments[2].cumulative_time, 70.0)

    def test_origin_equals_destination(self):
        """Caso límite: origen == destino."""
        self.graph.add_city("Sevilla")
        result = self.router.find_fastest_route("Sevilla", "Sevilla")
        self.assertEqual(result.total_time_minutes, 0.0)
        self.assertEqual(result.path, ["Sevilla"])
        self.assertEqual(result.segments, [])

    def test_disconnected_graph_raises_no_path_found(self):
        """Caso límite: no hay camino terrestre entre dos islas/componentes."""
        self.graph.add_city("Isla 1")
        self.graph.add_city("Isla 2")
        with self.assertRaises(NoPathFoundError):
            self.router.find_fastest_route("Isla 1", "Isla 2")

    def test_nonexistent_origin_or_destination(self):
        """Caso límite: consultar ciudades inexistentes."""
        self.graph.add_city("Granada")
        with self.assertRaises(CityNotFoundError):
            self.router.find_fastest_route("Granada", "Fantasma")
        with self.assertRaises(CityNotFoundError):
            self.router.find_fastest_route("Fantasma", "Granada")

    def test_case_insensitivity_and_spacing(self):
        """Verifica tolerancia a mayúsculas y espacios en la consulta."""
        self.graph.add_city("Ciudad Juárez")
        self.graph.add_city("Chihuahua")
        self.graph.add_highway("Ciudad Juárez", "Chihuahua", 210)

        result = self.router.find_fastest_route("  ciudad juárez  ", "CHIHUAHUA")
        self.assertEqual(result.total_time_minutes, 210.0)
        self.assertEqual(result.path, ["Ciudad Juárez", "Chihuahua"])


if __name__ == "__main__":
    unittest.main()
