#!/usr/bin/env node
/**
 * Punto de entrada del Sistema de Navegación GPS (Node.js).
 */

import { GPSNavigationSystem } from './navigation_system.mjs';
import { ConsoleUI } from './cli.mjs';

const system = new GPSNavigationSystem();
system.loadDemoData(); // Precarga ciudades y autopistas iniciales

const ui = new ConsoleUI(system);
await ui.start();
