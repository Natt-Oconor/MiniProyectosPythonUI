/**
 * Pruebas unitarias para el Sistema de Navegación GPS (Node.js Test Runner).
 */

import test from 'node:test';
import assert from 'node:assert/strict';
import { WeightedGraph } from './models.mjs';
import { DijkstraRouter } from './dijkstra.mjs';
import {
  CityNotFoundError,
  CityAlreadyExistsError,
  InvalidRouteError,
  NoPathFoundError
} from './exceptions.mjs';

test('Grafo Ponderado - Agregar ciudades correctamente', () => {
  const graph = new WeightedGraph();
  const name = graph.addCity('Madrid');
  assert.equal(name, 'Madrid');
  assert.equal(graph.hasCity('Madrid'), true);
  assert.equal(graph.hasCity('madrid'), true);
  assert.equal(graph.cityCount(), 1);
});

test('Grafo Ponderado - Rechazar ciudades duplicadas', () => {
  const graph = new WeightedGraph();
  graph.addCity('Barcelona');
  assert.throws(() => graph.addCity('Barcelona'), CityAlreadyExistsError);
  assert.throws(() => graph.addCity('  barcelona  '), CityAlreadyExistsError);
});

test('Grafo Ponderado - Rechazar nombres vacíos', () => {
  const graph = new WeightedGraph();
  assert.throws(() => graph.addCity(''), Error);
  assert.throws(() => graph.addCity('   '), Error);
});

test('Grafo Ponderado - Autopistas bidireccionales y dirigidas', () => {
  const graph = new WeightedGraph();
  graph.addCity('A');
  graph.addCity('B');
  graph.addHighway('A', 'B', 45, true);

  assert.equal(graph.getNeighbors('A')['B'], 45);
  assert.equal(graph.getNeighbors('B')['A'], 45);

  graph.addCity('C');
  graph.addHighway('B', 'C', 30, false);
  assert.equal(graph.getNeighbors('B')['C'], 30);
  assert.equal(graph.getNeighbors('C')['B'], undefined);
});

test('Grafo Ponderado - Validación de tiempos y auto-ciclos', () => {
  const graph = new WeightedGraph();
  graph.addCity('A');
  graph.addCity('B');

  assert.throws(() => graph.addHighway('A', 'B', 0), InvalidRouteError);
  assert.throws(() => graph.addHighway('A', 'B', -10), InvalidRouteError);
  assert.throws(() => graph.addHighway('A', 'B', 'invalido'), InvalidRouteError);
  assert.throws(() => graph.addHighway('A', 'A', 25), InvalidRouteError);
});

test('Dijkstra - Ruta directa', () => {
  const graph = new WeightedGraph();
  graph.addCity('A');
  graph.addCity('B');
  graph.addHighway('A', 'B', 50);

  const router = new DijkstraRouter(graph);
  const result = router.findFastestRoute('A', 'B');

  assert.equal(result.totalTimeMinutes, 50);
  assert.deepEqual(result.path, ['A', 'B']);
  assert.equal(result.segments.length, 1);
});

test('Dijkstra - Camino óptimo con más paradas pero menor tiempo', () => {
  const graph = new WeightedGraph();
  for (const c of ['A', 'B', 'C', 'D']) graph.addCity(c);

  // Ruta directa de 100 min
  graph.addHighway('A', 'D', 100);
  // Ruta de 3 tramos: 20 + 30 + 20 = 70 min
  graph.addHighway('A', 'B', 20);
  graph.addHighway('B', 'C', 30);
  graph.addHighway('C', 'D', 20);

  const router = new DijkstraRouter(graph);
  const result = router.findFastestRoute('A', 'D');

  assert.equal(result.totalTimeMinutes, 70);
  assert.deepEqual(result.path, ['A', 'B', 'C', 'D']);
  assert.equal(result.segments.length, 3);
  assert.equal(result.segments[0].cumulativeTime, 20);
  assert.equal(result.segments[1].cumulativeTime, 50);
  assert.equal(result.segments[2].cumulativeTime, 70);
});

test('Dijkstra - Caso límite: Origen igual a Destino', () => {
  const graph = new WeightedGraph();
  graph.addCity('Sevilla');

  const router = new DijkstraRouter(graph);
  const result = router.findFastestRoute('Sevilla', 'Sevilla');

  assert.equal(result.totalTimeMinutes, 0);
  assert.deepEqual(result.path, ['Sevilla']);
  assert.equal(result.segments.length, 0);
});

test('Dijkstra - Caso límite: Grafo inconexo (NoPathFoundError)', () => {
  const graph = new WeightedGraph();
  graph.addCity('Isla 1');
  graph.addCity('Isla 2');

  const router = new DijkstraRouter(graph);
  assert.throws(() => router.findFastestRoute('Isla 1', 'Isla 2'), NoPathFoundError);
});

test('Dijkstra - Caso límite: Ciudades inexistentes (CityNotFoundError)', () => {
  const graph = new WeightedGraph();
  graph.addCity('Granada');

  const router = new DijkstraRouter(graph);
  assert.throws(() => router.findFastestRoute('Granada', 'Fantasma'), CityNotFoundError);
  assert.throws(() => router.findFastestRoute('Fantasma', 'Granada'), CityNotFoundError);
});
