# 🗺️ Mini-Proyecto: Sistema de Navegación GPS

Sistema inteligente de navegación que modela ciudades como nodos y autopistas como aristas ponderadas por tiempo de traslado (en minutos). Utiliza el **Algoritmo de Dijkstra con Min-Heap** para calcular y reconstruir paso a paso la ruta más rápida entre cualquier par de ciudades.

---

## 📋 Cumplimiento de la Rúbrica de Evaluación

| Criterio | Porcentaje | Implementación Realizada |
| :--- | :---: | :--- |
| **Implementación de Grafo Ponderado** | **25%** | Clase `WeightedGraph` con lista de adyacencia (`Dict[str, Dict[str, float]]` / `Map`), normalización insensible a mayúsculas, soporte de rutas bidireccionales y dirigidas, y control de nodos/aristas. |
| **Algoritmo Dijkstra con Reconstrucción de Ruta** | **35%** | Clase `DijkstraRouter` optimizada con cola de prioridad (Min-Heap / `heapq`), complejidad $O((V + E) \log V)$, terminación temprana al alcanzar destino, seguimiento de predecesores, cálculo de tramos individuales y tiempo acumulado. |
| **Interfaz de Usuario (Consola)** | **20%** | Clase `ConsoleUI` con menú interactivo [1-6], tablas formateadas, formato de tiempo amigable (`X min (H h MM min)`), desglose visual tramo por tramo con flechas `➔` y precarga de datos de prueba con un solo click. |
| **Manejo de Excepciones y Casos Límite** | **10%** | Jerarquía de excepciones (`GPSNavigationError`, `CityNotFoundError`, `CityAlreadyExistsError`, `InvalidRouteError`, `NoPathFoundError`). Control de: ciudades inexistentes, origen == destino, grafos inconexos / islas, tiempos $\le 0$, auto-ciclos y entradas no numéricas. |
| **Calidad de Código y Comentarios** | **10%** | Arquitectura modular en capas (Modelo, Algoritmo, Fachada, CLI, Excepciones), tipado estricto (`typing` / JSDoc), docstrings en español acordes a PEP-257 y suite de pruebas unitarias automatizadas. |

---

## 🏗️ Estructura del Proyecto

El proyecto se entrega en dos implementaciones completas y funcionales: **Python** y **Node.js (JavaScript ES Modules)**.

```text
gps-navigation/
│
├── python/                      # Implementación en Python 3
│   ├── __init__.py
│   ├── exceptions.py            # Jerarquía de excepciones
│   ├── models.py                # Grafo ponderado (WeightedGraph)
│   ├── dijkstra.py              # Algoritmo Dijkstra y reconstrucción
│   ├── navigation_system.py     # Fachada y controlador
│   ├── cli.py                   # Interfaz interactiva de consola
│   ├── main.py                  # Punto de entrada principal
│   └── test_navigation.py       # Pruebas unitarias (unittest)
│
├── nodejs/                      # Implementación en Node.js (ESM)
│   ├── exceptions.mjs           # Jerarquía de errores
│   ├── models.mjs               # Grafo ponderado
│   ├── dijkstra.mjs             # Dijkstra con MinHeap binario
│   ├── navigation_system.mjs    # Fachada y datos de prueba
│   ├── cli.mjs                  # Interfaz con readline interactivo
│   ├── index.mjs                # Punto de entrada principal
│   ├── test_navigation.mjs      # Pruebas con node:test
│   └── package.json
│
└── README.md                    # Esta documentación
```

---

## ⚡ Guía de Ejecución

### Opción 1: Ejecución en Python 🐍

#### Requisitos
- Python 3.8 o superior (librería estándar, no requiere `pip install`).

#### Ejecutar la aplicación interactiva:
```bash
cd python
python main.py
```

#### Ejecutar la suite de pruebas unitarias:
```bash
cd python
python -m unittest test_navigation.py -v
```

---

### Opción 2: Ejecución en Node.js 🟩

#### Requisitos
- Node.js 18 o superior (sin dependencias externas).

#### Ejecutar la aplicación interactiva:
```bash
cd nodejs
node index.mjs
```

#### Ejecutar la suite de pruebas unitarias:
```bash
cd nodejs
npm test
# o directamente:
node --test test_navigation.mjs
```

---

## 🔍 Detalles del Algoritmo y Casos Límite

### 1. Grafo Ponderado (`WeightedGraph`)
- **Estructura:** Lista de adyacencia usando diccionarios anidados.
- **Normalización de Nombres:** Permite buscar `"guadalajara"`, `" GUADALAJARA "` o `"Guadalajara"` indistintamente, pero preserva el formato de visualización original.
- **Validaciones:**
  - No permite tiempos menores o iguales a 0 minutos.
  - No permite que una autopista conecte una ciudad con ella misma.
  - No permite registrar nombres vacíos.

### 2. Algoritmo de Dijkstra (`DijkstraRouter`)
- **Complejidad Temporal:** $O((V + E) \log V)$, donde $V$ es el número de ciudades y $E$ el número de autopistas.
- **Estructura Min-Heap:** En cada iteración se extrae el nodo no visitado con menor distancia acumulada.
- **Optimización de Parada Temprana:** Tan pronto como el nodo destino es extraído del heap, la ruta mínima está garantizada y la búsqueda finaliza.
- **Reconstrucción del Camino:** Mediante el mapeo de predecesores `previous[nodo]`, se retrocede desde el destino hasta el origen y se invierte la secuencia.
- **Cálculo de Tramos:** Genera una lista de objetos `RouteSegment` con:
  - Ciudad origen del tramo.
  - Ciudad destino del tramo.
  - Tiempo de ese tramo específico en minutos.
  - Tiempo acumulado hasta ese punto del viaje.

### 3. Casos Límite Contemplados
1. **Origen igual a Destino (`origen == destino`):**
   - Retorna de inmediato tiempo = 0.0 minutos, ruta = `[origen]` y 0 tramos.
2. **Grafo Inconexo / Sin Ruta Terrestre:**
   - Si no existe un camino conexo entre las ciudades, lanza `NoPathFoundError` informando que no hay conexión posible.
3. **Ciudades Inexistentes:**
   - Si se consulta una ciudad no registrada, lanza `CityNotFoundError`.
4. **Camino con más paradas pero menor tiempo:**
   - Si una ruta con 3 paradas toma 70 min y una directa toma 100 min, Dijkstra selecciona la de 70 min.
5. **Entradas erróneas en la consola:**
   - Letras ingresadas cuando se espera tiempo en minutos se capturan solicitando un nuevo ingreso sin detener el programa.
