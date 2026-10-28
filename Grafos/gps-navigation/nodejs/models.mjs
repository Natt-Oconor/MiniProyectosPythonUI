/**
 * Módulo de Grafo Ponderado en JavaScript (ES Modules).
 */

import {
  CityNotFoundError,
  CityAlreadyExistsError,
  InvalidRouteError
} from './exceptions.mjs';

export class WeightedGraph {
  constructor() {
    // Map: normalized_key -> Map(neighbor_key -> weight_in_minutes)
    this._adjacency = new Map();
    // Map: normalized_key -> original_display_name
    this._displayNames = new Map();
  }

  _normalize(name) {
    if (typeof name !== 'string' || !name.trim()) {
      throw new Error('El nombre de la ciudad no puede estar vacío.');
    }
    return name.trim().replace(/\s+/g, ' ').toLowerCase();
  }

  addCity(name) {
    if (typeof name !== 'string' || !name.trim()) {
      throw new Error('El nombre de la ciudad no puede estar vacío.');
    }
    const cleanName = name.trim().replace(/\s+/g, ' ');
    const key = this._normalize(cleanName);

    if (this._adjacency.has(key)) {
      throw new CityAlreadyExistsError(this._displayNames.get(key));
    }

    this._adjacency.set(key, new Map());
    this._displayNames.set(key, cleanName);
    return cleanName;
  }

  ensureCity(name) {
    const cleanName = name.trim().replace(/\s+/g, ' ');
    const key = this._normalize(cleanName);
    if (!this._adjacency.has(key)) {
      this._adjacency.set(key, new Map());
      this._displayNames.set(key, cleanName);
    }
    return this._displayNames.get(key);
  }

  hasCity(name) {
    try {
      const key = this._normalize(name);
      return this._adjacency.has(key);
    } catch {
      return false;
    }
  }

  getCityDisplayName(name) {
    const key = this._normalize(name);
    if (!this._displayNames.has(key)) {
      throw new CityNotFoundError(name);
    }
    return this._displayNames.get(key);
  }

  addHighway(origin, destination, timeMinutes, bidirectional = true) {
    const keyU = this._normalize(origin);
    const keyV = this._normalize(destination);

    if (!this._adjacency.has(keyU)) {
      throw new CityNotFoundError(origin);
    }
    if (!this._adjacency.has(keyV)) {
      throw new CityNotFoundError(destination);
    }

    if (keyU === keyV) {
      throw new InvalidRouteError(
        `No se puede crear una autopista con el mismo origen y destino ('${origin}').`
      );
    }

    const timeVal = Number(timeMinutes);
    if (Number.isNaN(timeVal)) {
      throw new InvalidRouteError('El tiempo de viaje debe ser un valor numérico.');
    }
    if (timeVal <= 0) {
      throw new InvalidRouteError(
        `El tiempo de recorrido debe ser mayor a 0 minutos (recibido: ${timeVal}).`
      );
    }

    this._adjacency.get(keyU).set(keyV, timeVal);
    if (bidirectional) {
      this._adjacency.get(keyV).set(keyU, timeVal);
    }
  }

  getCities() {
    return Array.from(this._displayNames.values()).sort((a, b) =>
      a.localeCompare(b, undefined, { sensitivity: 'base' })
    );
  }

  getNeighbors(city) {
    const key = this._normalize(city);
    if (!this._adjacency.has(key)) {
      throw new CityNotFoundError(city);
    }

    const result = {};
    for (const [neighborKey, weight] of this._adjacency.get(key).entries()) {
      result[this._displayNames.get(neighborKey)] = weight;
    }
    return result;
  }

  getAllHighways() {
    const seen = new Set();
    const highways = [];

    for (const [uKey, neighbors] of this._adjacency.entries()) {
      const uName = this._displayNames.get(uKey);
      for (const [vKey, weight] of neighbors.entries()) {
        const vName = this._displayNames.get(vKey);

        const isBidirectional =
          this._adjacency.has(vKey) &&
          this._adjacency.get(vKey).has(uKey) &&
          this._adjacency.get(vKey).get(uKey) === weight;

        const canonicalEdge = isBidirectional
          ? [uKey, vKey].sort().join('::')
          : `${uKey}->${vKey}`;

        if (!seen.has(canonicalEdge)) {
          seen.add(canonicalEdge);
          highways.push({ origin: uName, destination: vName, timeMinutes: weight });
        }
      }
    }

    return highways;
  }

  cityCount() {
    return this._adjacency.size;
  }

  highwayCount() {
    return this.getAllHighways().length;
  }
}
