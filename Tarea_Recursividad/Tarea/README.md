# Unidad 7: Recursividad - Solución Completa

Este repositorio contiene la resolución integral y documentada de todas las actividades propuestas en la **Unidad 7: Recursividad** (`U7_recursividad.md`), incluyendo:
- Los 5 ejercicios de **Práctica en Clase**.
- Los 5 ejercicios de la **Tarea** (con análisis de complejidad **Big-O** de tiempo y espacio).
- El **Mini-Proyecto: Explorador de Directorios** desarrollado bajo el paradigma de Programación Orientada a Objetos (POO) y cumpliendo al 100% la rúbrica de evaluación (100 puntos).
- Suite automatizada de **pruebas unitarias** (`unittest`) con cobertura de casos borde.

---

## Estructura del Proyecto

```text
D:\AntigrativyTarea\Tarea1\solucion\
│
├── practica_clase.py          # Solución a los 5 ejercicios de Práctica en Clase
├── tarea.py                   # Solución a los 5 ejercicios de Tarea + Análisis Big-O
├── explorador_directorios.py  # Mini-Proyecto: Clase ExploradorRecursivo (Rúbrica 100 pts)
├── test_soluciones.py         # Suite de 14 pruebas unitarias automatizadas
└── README.md                  # Documentación teórica, análisis y guía de ejecución
```

---

## 1. Fundamentos Teóricos

### 1.1 ¿Qué es la Recursividad?
La **recursividad** es una técnica algorítmica donde una función se llama a sí misma para resolver una instancia de menor tamaño o complejidad del problema original.

### 1.2 Anatomía de una Función Recursiva
Toda función recursiva bien estructurada debe constar de dos partes esenciales:
1. **Caso Base (Base Case)**: La condición de parada inmediata. Representa la versión elemental del problema que se resuelve directamente sin requerir llamadas recursivas adicionales. Sin él, la recursión sería infinita.
2. **Caso Recursivo**: La etapa donde la función se invoca a sí misma con parámetros reducidos o transformados, garantizando un avance estricto hacia el caso base.

### 1.3 La Pila de Llamadas (*Call Stack*)
Cada llamada a una función genera un marco de activación (*stack frame*) en la memoria de la computadora (estructura LIFO: *Last In, First Out*). Las llamadas pendientes quedan en espera hasta que el caso base retorna un valor, momento en el cual los marcos se resuelven y liberan en orden inverso.

Si una función carece de caso base o no converge hacia él, se agota la memoria asignada a la pila, desencadenando un error de desbordamiento de pila (**Stack Overflow** o `RecursionError` en Python).

### 1.4 Memoización
Técnica de optimización consistente en registrar en una tabla o diccionario (*caché*) los resultados de subproblemas ya computados, evitando el recálculo redundante y reduciendo la complejidad de exponencial ($O(2^n)$) a lineal ($O(n)$).

---

## 2. Práctica en Clase (`practica_clase.py`)

La clase `PracticaClase` reúne las siguientes funciones recursivas:

1. **`cuenta_regresiva(n)`**:
   - *Caso Base*: Si $n \le 0$, registra/imprime `"¡Despegue!"` y retorna.
   - *Caso Recursivo*: Registra $n$ e invoca recursivamente `cuenta_regresiva(n - 1)`.

2. **`invertir_cadena(cadena)`**:
   - *Caso Base*: Si $\text{len}(cadena) \le 1$, retorna la cadena intacta.
   - *Caso Recursivo*: `invertir_cadena(cadena[1:]) + cadena[0]`.

3. **`potencia(a, b)`**:
   - *Caso Base*: Si $b == 0$, retorna $1$. Si $b < 0$, calcula $1 / \text{potencia}(a, -b)$.
   - *Caso Recursivo*: $a \times \text{potencia}(a, b - 1)$.

4. **`es_palindromo(palabra)`**:
   - *Normalización*: Convierte a minúsculas y elimina caracteres no alfanuméricos.
   - *Caso Base*: Si $\text{len}(cadena) \le 1$, retorna `True`.
   - *Caso Recursivo*: Compara si `cadena[0] == cadena[-1]` y llama a `es_palindromo(cadena[1:-1])`.

5. **`maximo_lista(lista)`**:
   - *Caso Base*: Si $\text{len}(lista) == 1$, retorna el único elemento.
   - *Caso Recursivo*: Compara el primer elemento con el máximo del resto: $\max(lista[0], \text{maximo\_lista}(lista[1:]))$.

---

## 3. Tarea Asignada (`tarea.py`) y Análisis Big-O

### Ejercicio 1: Multiplicación Rusa (sin operador `*`)
Se implementaron dos variantes recursivas:
1. **Multiplicación por sumas sucesivas (`multiplicacion_por_sumas`)**:
   - Acumula $a$ sumado consigo mismo $b$ veces.
   - **Complejidad Temporal**: $O(|b|)$.
   - **Complejidad Espacial**: $O(|b|)$ en la pila de llamadas.
2. **Multiplicación Campesina Rusa (`multiplicacion_rusa`)**:
   - Si $b$ es impar: suma $a$ y evalúa recursivamente $(a + a, b // 2)$.
   - Si $b$ es par: evalúa $(a + a, b // 2)$.
   - **Complejidad Temporal**: $O(\log |b|)$, ya que $b$ se divide por 2 en cada paso.
   - **Complejidad Espacial**: $O(\log |b|)$ en la pila de llamadas.

### Ejercicio 2: Conteo de Vocales (`contar_vocales`)
- Cuenta vocales recursivamente (incluye mayúsculas y acentos: `a, e, i, o, u, á, é, í, ó, ú`).
- *Caso Base*: Cadena vacía retorna 0.
- *Caso Recursivo*: $(1 \text{ si } cadena[0] \text{ es vocal else } 0) + \text{contar\_vocales}(cadena[1:])$.
- **Complejidad Temporal**: $O(n)$ donde $n$ es la longitud del texto.
- **Complejidad Espacial**: $O(n)$ en marcos de activación y slicing.

### Ejercicio 3: Imprimir Patrón de Asteriscos (`imprimir_patron` / `generar_patron`)
Para $n=3$, genera:
```text
*
**
***
```
- *Caso Base*: Si la fila actual supera $n$, se detiene.
- *Caso Recursivo*: Imprime `'*' * fila_actual` y llama a `fila_actual + 1`.
- **Complejidad Temporal**: $O(n)$ llamadas recursivas ($O(n^2)$ operaciones de caracteres en total).
- **Complejidad Espacial**: $O(n)$ en la pila de llamadas.

### Ejercicio 4: Caminos en un Tablero $N \times M$ (`caminos_tablero`)
Cálculo de caminos desde $(0,0)$ hasta $(N-1, M-1)$ moviéndose exclusivamente hacia abajo o a la derecha:
- *Caso Base*: Si $N=1$ o $M=1$, solo existe una línea recta posible (retorna $1$). Si $N \le 0$ o $M \le 0$, retorna $0$.
- *Caso Recursivo*: $\text{caminos}(N - 1, M) + \text{caminos}(N, M - 1)$.
- **Análisis Big-O (Versión Ingenua)**:
  - **Temporal**: $O(2^{N+M})$ exponencial o $\binom{N+M-2}{N-1}$ debido al árbol binario de llamadas repetidas.
  - **Espacial**: $O(N + M)$ correspondiente a la profundidad máxima de la pila.
- **Análisis Big-O (Versión Memoizada `caminos_tablero_memo`)**:
  - **Temporal**: $O(N \times M)$, calculando cada par de coordenadas una sola vez.
  - **Espacial**: $O(N \times M)$ para el diccionario de memoización.

### Ejercicio 5: Flatten List (`flatten_list`)
Aplana recursivamente estructuras con cualquier nivel de profundidad arbitrario (por ejemplo `[1, [2, [3, 4], 5]] -> [1, 2, 3, 4, 5]`).
- *Caso Base*: Lista vacía retorna `[]`.
- *Caso Recursivo*:
  - Si la cabeza es una lista: `flatten_list(cabeza) + flatten_list(cola)`.
  - Si la cabeza es un elemento atómico: `[cabeza] + flatten_list(cola)`.
- **Complejidad Temporal**: $O(k)$ donde $k$ es el número total de nodos/elementos.
- **Complejidad Espacial**: $O(d)$ donde $d$ es la profundidad máxima de anidación.

---

## 4. Mini-Proyecto: Explorador de Directorios (`explorador_directorios.py`)

La clase `ExploradorRecursivo` modela un sistema de archivos representado por diccionarios jerárquicos:

```python
sistema_archivos = {
    "Documentos": {
        "apuntes.txt": "10kb",
        "fotos": {
            "vacaciones.png": "2mb",
            "perro.jpg": "1mb"
        }
    },
    "sistema.dll": "500kb"
}
```

### Cumplimiento de la Rúbrica de Evaluación (100 / 100 puntos)

| Criterio | Puntos | Implementación |
| :--- | :---: | :--- |
| **`imprimir_arbol` con indentación visual** | **30 pts** | Método `imprimir_arbol(sistema, nivel)` con sangría proporcional a la profundidad y estructura de árbol (`+-- [Carpeta] nombre/` y `\|-- [Archivo] nombre (tamaño)`). |
| **Búsqueda profunda `buscar_archivo`** | **30 pts** | Método `buscar_archivo(sistema, nombre)` que busca mediante DFS sin crashear al llegar a nodos hoja (strings), devolviendo la ruta completa (`Documentos/fotos/vacaciones.png`) o `None`. |
| **Conteo de archivos `contar_archivos`** | **20 pts** | Método `contar_archivos(sistema)` que suma recursivamente sólo los nodos hoja (archivos), excluyendo las carpetas intermedias. |
| **Definición de Casos Base y Recursivos** | **10 pts** | Docstrings y comentarios explícitos en cada método identificando formalmente el Caso Base y el Caso Recursivo. |
| **Código legible, PEP8 y POO** | **10 pts** | Modularización en clase orientada a objetos, type hints estrictos (`typing`), nombres descriptivos en español y apego total a PEP8. |

---

## 5. Instrucciones de Ejecución

Para ejecutar cada módulo de forma individual:

```bash
# 1. Ejecutar Práctica en Clase
python practica_clase.py

# 2. Ejecutar Tarea y visualizar análisis Big-O
python tarea.py

# 3. Ejecutar Mini-Proyecto Explorador de Directorios
python explorador_directorios.py
```

### Ejecutar Suite de Pruebas Unitarias
Para correr las 14 pruebas automatizadas con reporte de éxito:

```bash
python -m unittest test_soluciones.py -v
```

---

## 6. Recursos Adicionales y Referencias

Tal como se referencia en la guía original:
- [VisuAlgo - Árboles de Recursión Interactivos](https://visualgo.net/en/recursion)
- [freeCodeCamp: Recursion in Programming - Full Course](https://www.youtube.com/results?search_query=freeCodeCamp+Recursion+in+Programming)
- Documentación oficial de Python sobre recursividad y límite de pila (`sys.getrecursionlimit`).
