/**
 * Implementación del Algoritmo de Dijkstra con Min-Heap y Reconstrucción de Ruta en JavaScript.
 */

import { CityNotFoundError, NoPathFoundError } from './exceptions.mjs';

/**
 * Min-Heap binario para la cola de prioridad de Dijkstra.
 */
class MinHeap {
  constructor() {
    this.heap = [];
  }

  push(item) {
    this.heap.push(item);
    this._bubbleUp(this.heap.length - 1);
  }

  pop() {
    if (this.heap.length === 0) return null;
    const top = this.heap[0];
    const bottom = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = bottom;
      this._sinkDown(0);
    }
    return top;
  }

  isEmpty() {
    return this.heap.length === 0;
  }

  _bubbleUp(index) {
    const element = this.heap[index];
    while (index > 0) {
      const parentIdx = Math.floor((index - 1) / 2);
      const parent = this.heap[parentIdx];
      if (element.distance >= parent.distance) break;
      this.heap[index] = parent;
      this.heap[parentIdx] = element;
      index = parentIdx;
    }
  }

  _sinkDown(index) {
    const length = this.heap.length;
    const element = this.heap[index];

    while (true) {
      let leftChildIdx = 2 * index + 1;
      let rightChildIdx = 2 * index + 2;
      let swapIdx = null;

      if (leftChildIdx < length) {
        if (this.heap[leftChildIdx].distance < element.distance) {
          swapIdx = leftChildIdx;
        }
      }

      if (rightChildIdx < length) {
        if (
          (swapIdx === null && this.heap[rightChildIdx].distance < element.distance) ||
          (swapIdx !== null && this.heap[rightChildIdx].distance < this.heap[leftChildIdx].distance)
        ) {
          swapIdx = rightChildIdx;
        }
      }

      if (swapIdx === null) break;
      this.heap[index] = this.heap[swapIdx];
      this.heap[swapIdx] = element;
      index = swapIdx;
    }
  }
}

export class DijkstraRouter {
  constructor(graph) {
    this.graph = graph;
  }

  findFastestRoute(origin, destination) {
    // 1. Validar existencia de ciudades
    if (!this.graph.hasCity(origin)) {
      throw new CityNotFoundError(origin);
    }
    if (!this.graph.hasCity(destination)) {
      throw new CityNotFoundError(destination);
    }

    const originName = this.graph.getCityDisplayName(origin);
    const destName = this.graph.getCityDisplayName(destination);
    const originKey = this.graph._normalize(origin);
    const destKey = this.graph._normalize(destination);

    // 2. Caso límite: origen == destino
    if (originKey === destKey) {
      return {
        origin: originName,
        destination: destName,
        totalTimeMinutes: 0.0,
        path: [originName],
        segments: [],
        isReachable: true
      };
    }

    // 3. Inicialización
    const distances = new Map();
    const previous = new Map();
    const visited = new Set();
    const pq = new MinHeap();

    for (const key of this.graph._adjacency.keys()) {
      distances.set(key, Infinity);
      previous.set(key, null);
    }

    distances.set(originKey, 0.0);
    pq.push({ key: originKey, distance: 0.0 });

    // 4. Bucle principal de Dijkstra
    while (!pq.isEmpty()) {
      const { key: currentKey, distance: currentDist } = pq.pop();

      if (currentKey === destKey) break;
      if (visited.has(currentKey)) continue;
      visited.add(currentKey);

      if (currentDist > distances.get(currentKey)) continue;

      const neighbors = this.graph._adjacency.get(currentKey) || new Map();
      for (const [neighborKey, travelTime] of neighbors.entries()) {
        if (visited.has(neighborKey)) continue;

        const newDist = currentDist + travelTime;
        if (newDist < distances.get(neighborKey)) {
          distances.set(neighborKey, newDist);
          previous.set(neighborKey, currentKey);
          pq.push({ key: neighborKey, distance: newDist });
        }
      }
    }

    // 5. Validar alcanzabilidad
    if (distances.get(destKey) === Infinity) {
      throw new NoPathFoundError(originName, destName);
    }

    // 6. Reconstrucción de la ruta
    const reconstructedKeys = [];
    let curr = destKey;
    while (curr !== null) {
      reconstructedKeys.push(curr);
      curr = previous.get(curr);
    }
    reconstructedKeys.reverse();

    const path = reconstructedKeys.map(k => this.graph._displayNames.get(k));
    const segments = [];
    let cumulative = 0.0;

    for (let i = 0; i < reconstructedKeys.length - 1; i++) {
      const uKey = reconstructedKeys[i];
      const vKey = reconstructedKeys[i + 1];
      const segTime = this.graph._adjacency.get(uKey).get(vKey);
      cumulative += segTime;
      segments.push({
        origin: this.graph._displayNames.get(uKey),
        destination: this.graph._displayNames.get(vKey),
        timeMinutes: segTime,
        cumulativeTime: cumulative
      });
    }

    return {
      origin: originName,
      destination: destName,
      totalTimeMinutes: distances.get(destKey),
      path,
      segments,
      isReachable: true
    };
  }
}
