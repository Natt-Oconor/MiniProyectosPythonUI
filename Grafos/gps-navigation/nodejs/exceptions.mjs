/**
 * Jerarquía de excepciones personalizadas para el Sistema de Navegación GPS.
 */

export class GPSNavigationError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class CityNotFoundError extends GPSNavigationError {
  constructor(cityName) {
    super(`La ciudad '${cityName}' no existe en el mapa de navegación.`);
    this.cityName = cityName;
  }
}

export class CityAlreadyExistsError extends GPSNavigationError {
  constructor(cityName) {
    super(`La ciudad '${cityName}' ya está registrada en el sistema.`);
    this.cityName = cityName;
  }
}

export class InvalidRouteError extends GPSNavigationError {
  constructor(message) {
    super(message);
  }
}

export class NoPathFoundError extends GPSNavigationError {
  constructor(origin, destination) {
    super(`No existe ninguna ruta disponible entre '${origin}' y '${destination}'.`);
    this.origin = origin;
    this.destination = destination;
  }
}
