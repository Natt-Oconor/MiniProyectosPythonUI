# 🎬 Sistema de Recomendación con Grafos Bipartitos en Python

Un mini-proyecto didáctico y funcional que implementa un motor de recomendación de películas utilizando **teoría de grafos** y **filtrado colaborativo**. Desarrollado con una arquitectura híbrida: estructura de grafo y algoritmos matemáticos programados desde cero en **POO (Python nativo)**, y visualización de alta resolución con **NetworkX** y **Matplotlib**.

---

## 🧠 Conceptos de Teoría de Grafos Aplicados

### 1. Grafo Bipartito $G = (U, V, E)$
Un grafo bipartito es aquel cuyos vértices pueden dividirse en dos conjuntos disjuntos $U$ y $V$, de tal manera que ninguna arista conecte vértices del mismo conjunto:
* **Conjunto $U$ (Usuarios):** Alicia, Bob, Carlos, Diana, Elena, Fernando, Sofía.
* **Conjunto $V$ (Ítems / Películas):** The Matrix, Interstellar, Pulp Fiction, Coco, etc.
* **Aristas ponderadas $E$:** Calificaciones que los usuarios otorgaron a las películas (del $1.0$ al $5.0$).

### 2. Caminos de Longitud 3 en el Grafo (Explicabilidad)
¿Por qué el sistema sugiere una película? La recomendación se fundamenta en un camino de 3 saltos en el grafo bipartito:
$$\text{Usuario}_A \xrightarrow{\text{vio}} \text{Película}_{\text{común}} \xleftarrow{\text{vio}} \text{Usuario}_B \xrightarrow{\text{le encantó}} \text{Película}_{\text{sugerida}}$$

Ejemplo:
$$\text{Fernando} \to \text{The Matrix} \to \text{Alicia} \to \text{Inception}$$

### 3. Similitud de Coseno sobre Grados y Calificaciones
Para determinar qué usuarios tienen gustos afines, calculamos el coseno vectorial de sus valoraciones en las películas que ambos vieron:
$$\text{sim}(u, v) = \frac{\sum_{i \in I_{comunes}} r_{u,i} \cdot r_{v,i}}{\sqrt{\sum r_{u,i}^2} \cdot \sqrt{\sum r_{v,i}^2}}$$

### 4. Puntuación Proyectada
Para una película $i$ no vista por el usuario $u$:
$$\hat{r}_{u, i} = \frac{\sum_{v \in \text{Vecinos}(i)} \text{sim}(u, v) \cdot r_{v, i}}{\sum_{v \in \text{Vecinos}(i)} |\text{sim}(u, v)|}$$

---

## 📁 Estructura del Proyecto

```
grafo_recomendador/
├── app_gui.py        # 🖥️ Interfaz Gráfica de Escritorio (CustomTkinter + Matplotlib)
├── graph.py          # Clase GrafoBipartitoRecomendador y algoritmos desde cero
├── visualizer.py     # Renderizado visual estético con NetworkX y Matplotlib
├── data.py           # Catálogo inicial de películas y perfiles de usuarios
├── main.py           # Menú interactivo en consola y modo demostración
├── requirements.txt  # Dependencias (networkx, matplotlib, customtkinter)
└── README.md         # Documentación teórica y técnica
```

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. 🖥️ Abrir la Interfaz Gráfica de Escritorio (UI)
```bash
python app_gui.py
```
*(O también mediante `python main.py --gui`)*

**Características de la UI:**
* 🎯 **Selector de usuario objetivo** para explorar recomendaciones en tiempo real.
* 📊 **Canvas interactivo** con el grafo bipartito renderizado al instante.
* 🌓 **Modo Oscuro / Modo Claro** con paleta de colores adaptativa.
* ➕ **Modal para registrar calificaciones** o nuevos usuarios/películas.
* 💾 **Exportador de imágenes PNG** con un solo clic.

### 3. Ejecutar la demostración en consola
```bash
python main.py --demo
```

### 4. Ejecutar el menú interactivo en terminal
```bash
python main.py
```
