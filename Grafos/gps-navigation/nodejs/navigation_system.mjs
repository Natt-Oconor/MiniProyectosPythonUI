/**
 * Fachada del Sistema de Navegación GPS en JavaScript.
 */

import { WeightedGraph } from './models.mjs';
import { DijkstraRouter } from './dijkstra.mjs';

export class GPSNavigationSystem {
  constructor() {
    this.graph = new WeightedGraph();
    this.router = new DijkstraRouter(this.graph);
  }

  registerCity(cityName) {
    return this.graph.addCity(cityName);
  }

  addHighway(origin, destination, timeMinutes, bidirectional = true) {
    this.graph.addHighway(origin, destination, timeMinutes, bidirectional);
  }

  findFastestRoute(origin, destination) {
    return this.router.findFastestRoute(origin, destination);
  }

  getAllCities() {
    return this.graph.getCities();
  }

  getCityConnections(cityName) {
    return this.graph.getNeighbors(cityName);
  }

  getAllHighways() {
    return this.graph.getAllHighways();
  }

  loadDemoData() {
    const demoCities = [
      'Ciudad de México',
      'Puebla',
      'Querétaro',
      'Guadalajara',
      'San Luis Potosí',
      'Toluca',
      'Cuernavaca',
      'León',
      'Monterrey'
    ];

    for (const city of demoCities) {
      this.graph.ensureCity(city);
    }

    const demoRoutes = [
      ['Ciudad de México', 'Toluca', 55],
      ['Ciudad de México', 'Cuernavaca', 65],
      ['Ciudad de México', 'Puebla', 120],
      ['Ciudad de México', 'Querétaro', 150],
      ['Toluca', 'Querétaro', 130],
      ['Querétaro', 'San Luis Potosí', 135],
      ['Querétaro', 'León', 110],
      ['León', 'Guadalajara', 140],
      ['San Luis Potosí', 'Guadalajara', 195],
      ['San Luis Potosí', 'Monterrey', 310],
      ['Puebla', 'Cuernavaca', 140]
    ];

    for (const [orig, dest, minutes] of demoRoutes) {
      this.graph.addHighway(orig, dest, minutes, true);
    }

    return {
      citiesCount: demoCities.length,
      highwaysCount: demoRoutes.length
    };
  }
}
