/**
 * Interfaz de Consola interactiva para Node.js usando readline/promises.
 */

import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import {
  CityNotFoundError,
  CityAlreadyExistsError,
  InvalidRouteError,
  NoPathFoundError
} from './exceptions.mjs';

export class ConsoleUI {
  constructor(system) {
    this.system = system;
  }

  _printHeader(title) {
    const width = 65;
    console.log('\n' + '='.repeat(width));
    const pad = Math.max(0, Math.floor((width - title.length - 2) / 2));
    console.log(' '.repeat(pad) + title.toUpperCase());
    console.log('='.repeat(width));
  }

  _printDivider() {
    console.log('-'.repeat(65));
  }

  _formatTime(minutes) {
    const totalMins = Math.round(minutes);
    const hours = Math.floor(totalMins / 60);
    const mins = totalMins % 60;
    if (hours > 0) {
      return `${minutes.toFixed(1)} min (${hours} h ${String(mins).padStart(2, '0')} min)`;
    }
    return `${minutes.toFixed(1)} min`;
  }

  displayCities() {
    this._printHeader('Ciudades y Red de Autopistas');
    const cities = this.system.getAllCities();

    if (cities.length === 0) {
      console.log('\n [!] No hay ciudades registradas aún en el mapa.');
      console.log('     Utilice la opción 2 para agregar una ciudad o la opción 5 para cargar datos demo.');
      return;
    }

    console.log(`\n Ciudades registradas en el sistema (${cities.length} en total):\n`);
    cities.forEach((city, idx) => {
      const connections = this.system.getCityConnections(city);
      const connKeys = Object.keys(connections);
      const num = String(idx + 1).padStart(2, '0');
      if (connKeys.length > 0) {
        const connsStr = connKeys
          .map(dest => `${dest} (${this._formatTime(connections[dest])})`)
          .join(', ');
        console.log(`  [${num}] ${city}`);
        console.log(`       └── Conexiones directas: ${connsStr}`);
      } else {
        console.log(`  [${num}] ${city} (Sin autopistas conectadas)`);
      }
    });

    const highways = this.system.getAllHighways();
    console.log(`\n Total de autopistas en la red: ${highways.length}`);
  }

  async addCityDialog(rl) {
    this._printHeader('Registrar Nueva Ciudad');
    const cityName = (await rl.question(' Nombre de la ciudad a registrar: ')).trim();
    if (!cityName) {
      console.log(' [!] Operación cancelada: El nombre no puede estar vacío.');
      return;
    }

    try {
      const registered = this.system.registerCity(cityName);
      console.log(`\n [✓] Ciudad '${registered}' registrada exitosamente.`);
    } catch (e) {
      if (e instanceof CityAlreadyExistsError) {
        console.log(`\n [!] Aviso: ${e.message}`);
      } else {
        console.log(`\n [!] Error: ${e.message}`);
      }
    }
  }

  async addHighwayDialog(rl) {
    this._printHeader('Agregar Nueva Autopista');
    const cities = this.system.getAllCities();

    if (cities.length < 2) {
      console.log('\n [!] Se necesitan al menos 2 ciudades registradas para crear una autopista.');
      const auto = (await rl.question(' ¿Desea cargar el mapa de prueba con ciudades predeterminadas? (s/n): '))
        .trim()
        .toLowerCase();
      if (auto === 's') {
        const res = this.system.loadDemoData();
        console.log(`\n [✓] Mapa cargado con ${res.citiesCount} ciudades y ${res.highwaysCount} autopistas.`);
      } else {
        return;
      }
    }

    console.log('\n Ingrese los datos de la nueva autopista:');
    let origin = (await rl.question('  • Ciudad de origen: ')).trim();
    if (!origin) {
      console.log(' [!] Operación cancelada: Origen inválido.');
      return;
    }

    if (!this.system.graph.hasCity(origin)) {
      const create = (await rl.question(`  [?] La ciudad '${origin}' no existe. ¿Registrarla ahora? (s/n): `))
        .trim()
        .toLowerCase();
      if (create === 's') {
        this.system.graph.ensureCity(origin);
        console.log(`  [✓] Ciudad '${origin}' registrada.`);
      } else {
        console.log(' [!] Operación cancelada.');
        return;
      }
    }

    let dest = (await rl.question('  • Ciudad de destino: ')).trim();
    if (!dest) {
      console.log(' [!] Operación cancelada: Destino inválido.');
      return;
    }

    if (!this.system.graph.hasCity(dest)) {
      const create = (await rl.question(`  [?] La ciudad '${dest}' no existe. ¿Registrarla ahora? (s/n): `))
        .trim()
        .toLowerCase();
      if (create === 's') {
        this.system.graph.ensureCity(dest);
        console.log(`  [✓] Ciudad '${dest}' registrada.`);
      } else {
        console.log(' [!] Operación cancelada.');
        return;
      }
    }

    if (this.system.graph._normalize(origin) === this.system.graph._normalize(dest)) {
      console.log(' [!] Error: Una autopista no puede conectar una ciudad consigo misma.');
      return;
    }

    let timeMinutes = null;
    while (timeMinutes === null) {
      const raw = (await rl.question('  • Tiempo de recorrido estimado (en minutos): ')).trim();
      const val = parseFloat(raw);
      if (Number.isNaN(val) || val <= 0) {
        console.log('    [!] Debe ingresar un número positivo mayor a 0 minutos.');
      } else {
        timeMinutes = val;
      }
    }

    const bidirRaw = (await rl.question('  • ¿La autopista es de doble sentido / bidireccional? (S/n): '))
      .trim()
      .toLowerCase();
    const bidirectional = bidirRaw !== 'n';

    try {
      this.system.addHighway(origin, dest, timeMinutes, bidirectional);
      const sentido = bidirectional ? 'doble sentido (bidireccional)' : 'sentido único';
      console.log(`\n [✓] Autopista registrada con éxito:`);
      console.log(`     ${origin} <--> ${dest} (${this._formatTime(timeMinutes)}) [${sentido}]`);
    } catch (e) {
      console.log(`\n [!] Error: ${e.message}`);
    }
  }

  async queryRouteDialog(rl) {
    this._printHeader('Consultar Ruta Más Rápida (GPS)');
    const cities = this.system.getAllCities();

    if (cities.length < 2) {
      console.log('\n [!] No hay suficientes ciudades en el sistema para calcular rutas.');
      return;
    }

    console.log('\n Ciudades disponibles:');
    cities.forEach((city, idx) => {
      const num = String(idx + 1).padStart(2, '0');
      console.log(`  [${num}] ${city}`);
    });

    console.log('\n Ingrese las ciudades a consultar:');
    const origin = (await rl.question('  • Ciudad de partida (Origen): ')).trim();
    const dest = (await rl.question('  • Ciudad de llegada (Destino): ')).trim();

    if (!origin || !dest) {
      console.log('\n [!] Debe ingresar ambas ciudades para calcular la ruta.');
      return;
    }

    try {
      const result = this.system.findFastestRoute(origin, dest);

      this._printDivider();
      console.log('  RESULTADO DEL CÁLCULO DE RUTA GPS');
      this._printDivider();
      console.log(`  • Origen:            ${result.origin}`);
      console.log(`  • Destino:           ${result.destination}`);
      console.log(`  • Tiempo Total:      ${this._formatTime(result.totalTimeMinutes)}`);

      if (result.origin === result.destination) {
        console.log('  • Estado:            Ya se encuentra en el destino.');
        console.log(`  • Recorrido:         [${result.origin}]`);
        return;
      }

      console.log(`  • Recorrido óptimo:  ${result.path.join(' ➔ ')}`);
      console.log(`  • Número de paradas: ${result.path.length - 1} tramos`);

      console.log('\n  DESGLOSE DETALLADO DEL VIAJE:');
      console.log('  ' + '-'.repeat(59));
      console.log('  #   Tramo                               Tiempo     Acumulado');
      console.log('  ' + '-'.repeat(59));

      result.segments.forEach((seg, idx) => {
        const num = String(idx + 1).padEnd(3, ' ');
        const tramo = `${seg.origin} ➔ ${seg.destination}`.padEnd(35, ' ');
        const t = `${seg.timeMinutes.toFixed(1)} min`.padStart(10, ' ');
        const c = `${seg.cumulativeTime.toFixed(1)} min`.padStart(10, ' ');
        console.log(`  ${num} ${tramo} ${t}  ${c}`);
      });
      console.log('  ' + '-'.repeat(59));
    } catch (e) {
      if (e instanceof CityNotFoundError) {
        console.log(`\n [!] Error de localización: ${e.message}`);
      } else if (e instanceof NoPathFoundError) {
        console.log(`\n [!] Ruta no disponible: ${e.message}`);
      } else {
        console.log(`\n [!] Error: ${e.message}`);
      }
    }
  }

  loadDemoDialog() {
    this._printHeader('Cargar Red Vial de Prueba');
    const res = this.system.loadDemoData();
    console.log(`\n [✓] Se cargaron exitosamente:`);
    console.log(`     • ${res.citiesCount} ciudades (CDMX, Toluca, Puebla, Querétaro, GDL, MTY, etc.)`);
    console.log(`     • ${res.highwaysCount} autopistas ponderadas por tiempo de traslado.`);
    console.log('\n ¡Ahora puede consultar rutas entre estas ciudades!');
  }

  async start() {
    const rl = readline.createInterface({ input, output });

    try {
      while (true) {
        this._printHeader('Sistema de Navegación GPS - Menú Principal');
        console.log('  1. Ver todas las ciudades y mapa de autopistas');
        console.log('  2. Agregar nueva ciudad');
        console.log('  3. Agregar nueva ruta (autopista ponderada)');
        console.log('  4. Consultar ruta más rápida (Algoritmo Dijkstra)');
        console.log('  5. Cargar mapa de prueba predeterminado');
        console.log('  6. Salir');
        this._printDivider();

        const option = (await rl.question(' Seleccione una opción [1-6]: ')).trim();

        if (option === '1') {
          this.displayCities();
        } else if (option === '2') {
          await this.addCityDialog(rl);
        } else if (option === '3') {
          await this.addHighwayDialog(rl);
        } else if (option === '4') {
          await this.queryRouteDialog(rl);
        } else if (option === '5') {
          this.loadDemoDialog();
        } else if (option === '6') {
          console.log('\n [✓] Saliendo del Sistema de Navegación GPS. ¡Buen viaje!\n');
          break;
        } else {
          console.log('\n [!] Opción no válida. Por favor elija un número del 1 al 6.');
        }

        await rl.question('\n Presione [Enter] para continuar...');
      }
    } finally {
      rl.close();
    }
  }
}
