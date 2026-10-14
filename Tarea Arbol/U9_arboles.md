# Unidad 9: Árboles

## 1. Objetivos de Aprendizaje
* Entender la naturaleza jerárquica y no lineal de la estructura de datos Árbol.
* Dominar la terminología básica (raíz, hoja, hijo, padre, nivel, altura).
* Implementar un Árbol Binario de Búsqueda (BST) desde cero usando Programación Orientada a Objetos.
* Comprender y aplicar los recorridos de profundidad (DFS: Preorden, Inorden, Postorden) y anchura (BFS: Nivel por Nivel).
* Analizar la complejidad temporal de inserción, búsqueda y eliminación en árboles balanceados vs. degenerados.

## 2. Conceptos Teóricos (Semana 1)

### Teoría General de Árboles
A diferencia de las listas o arreglos que son estructuras *lineales*, los árboles son estructuras de datos **jerárquicas** o **no lineales**.

**Terminología:**
* **Nodo:** Cada elemento del árbol que contiene un dato y referencias a sus hijos.
* **Raíz:** El nodo superior del árbol. No tiene padre.
* **Hijo / Padre:** Un nodo apuntado por otro es su hijo. El nodo que apunta es el padre.
* **Hoja:** Un nodo que no tiene hijos (está al final de una rama).
* **Nivel / Profundidad:** La distancia desde la raíz hasta un nodo. La raíz está en el nivel 0.
* **Altura:** La longitud del camino más largo desde la raíz hasta una hoja.
* **Subárbol:** Cualquier nodo junto con todos sus descendientes.

**Tipos de Árboles:**
* **Árbol General:** Un nodo puede tener cualquier cantidad de hijos.
* **Árbol Binario:** Cada nodo tiene como MÁXIMO dos hijos (izquierdo y derecho).
* **Árbol Binario de Búsqueda (BST):** Un árbol binario ordenado.
* **Árbol AVL / Red-Black:** Árboles binarios que se auto-balancean para garantizar O(log n).
* **B-Tree:** Usado en bases de datos, nodos con muchos hijos para minimizar lecturas de disco.
* **Heap (Montículo):** Árbol binario completo usado para colas de prioridad.

**Diagrama ASCII de un Árbol Binario:**
```text
          ( 50 )          <- Raíz (Nivel 0)
         /      \
      ( 30 )  ( 70 )      <- Nodos Internos (Nivel 1)
      /    \      \
   ( 20 )( 40 ) ( 80 )    <- Hojas (Nivel 2)

Altura del árbol = 2
```

**¿Por qué usar árboles?**
Proveen la rapidez de búsqueda de un arreglo ordenado (O(log n)), combinada con la rapidez de inserción/eliminación de una lista enlazada (O(log n)). Además, representan jerarquías naturales (sistema de archivos, organigramas, DOM HTML).

### Árbol Binario de Búsqueda - BST (Semana 2)

**Propiedad Fundamental:**
Para CUALQUIER nodo `N`:
* Todos los valores en su subárbol **IZQUIERDO** son **MENORES** que el valor de `N`.
* Todos los valores en su subárbol **DERECHO** son **MAYORES** que el valor de `N`.

**Operaciones:**
* **Búsqueda:** Bajas por el árbol; si el valor es menor, vas a la izquierda, si es mayor, a la derecha. O(log n) promedio.
* **Inserción:** Igual que la búsqueda, hasta encontrar un espacio vacío (llegar a `None`), y se inserta como hoja nueva.
* **Eliminación:** Tiene 3 casos:
  1. El nodo es hoja (sin hijos) -> Se elimina directamente.
  2. El nodo tiene 1 hijo -> Se puentea al nodo con su único hijo.
  3. El nodo tiene 2 hijos -> Se reemplaza el valor con su sucesor inorden (el mínimo del subárbol derecho) y se elimina el sucesor.

**Recorridos:**
* **Inorden (In-order):** Izquierda -> Raíz -> Derecha. (En un BST, esto imprime los datos ordenados).
* **Preorden (Pre-order):** Raíz -> Izquierda -> Derecha. (Útil para copiar un árbol).
* **Postorden (Post-order):** Izquierda -> Derecha -> Raíz. (Útil para eliminar un árbol desde las hojas).
* **Niveles (BFS):** Imprime nivel por nivel de arriba a abajo, de izquierda a derecha.

## 3. Implementación en Python (OOP)

```python
class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None
        
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
            
    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, valor)
        else:
            # El valor ya existe, por diseño no admitimos duplicados
            pass
            
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)
        
    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        elif valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, valor)

    # Recorridos
    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado
        
    def _inorden_rec(self, nodo, resultado):
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)
            
    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo is not None:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    # Utilidades
    def min_valor(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo.valor

    def max_valor(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.valor
        
    def mostrar_arbol(self):
        """Muestra el árbol de forma gráfica en consola rotado 90 grados"""
        self._imprimir_nodo(self.raiz, "", True)

    def _imprimir_nodo(self, nodo, prefijo, es_izquierdo):
        if nodo is not None:
            self._imprimir_nodo(nodo.derecho, prefijo + ("|   " if es_izquierdo else "    "), False)
            print(prefijo + ("\\-- " if es_izquierdo else "/-- ") + str(nodo.valor))
            self._imprimir_nodo(nodo.izquierdo, prefijo + ("    " if es_izquierdo else "|   "), True)
```

## 4. Ejemplos Resueltos

**Ejemplo 1: Creando un BST y comprobando propiedad inorden**
```python
bst = ArbolBinarioBusqueda()
for val in [50, 30, 70, 20, 40, 60, 80]:
    bst.insertar(val)
print("Recorrido Inorden:", bst.inorden())
# Salida esperada: [20, 30, 40, 50, 60, 70, 80] -> ¡Ordenado!
```

**Ejemplo 2: Visualizando el árbol**
```python
bst = ArbolBinarioBusqueda()
for val in [10, 5, 15, 2, 7, 12, 17]:
    bst.insertar(val)
bst.mostrar_arbol()
# Salida:
#     /-- 17
# /-- 15
# |   \-- 12
# \-- 10
#     |   /-- 7
#     \-- 5
#         \-- 2
```

**Ejemplo 3: Extrayendo mínimos y máximos**
```python
bst = ArbolBinarioBusqueda()
valores = [42, 16, 8, 100, 23, 50]
for val in valores:
    bst.insertar(val)
print("El valor más pequeño es:", bst.min_valor()) # Output: 8
print("El valor más grande es:", bst.max_valor())  # Output: 100
```

**Ejemplo 4: Búsqueda rápida**
```python
bst = ArbolBinarioBusqueda()
for x in range(1, 1000, 2):  # Impares del 1 al 999
    bst.insertar(x)

print("¿Está el 500?", bst.buscar(500)) # Output: False (rápido, sin recorrer todo)
print("¿Está el 501?", bst.buscar(501)) # Output: True
```

## 5. Práctica en Clase

**Ejercicio 1:** 
Dado un árbol binario de búsqueda donde se insertaron secuencialmente los elementos: `1, 2, 3, 4, 5`. Dibuja el árbol y comenta su altura.
*Solución:* 
```text
( 1 )
   \
   ( 2 )
      \
      ( 3 )
         \
         ( 4 )
            \
            ( 5 )
```
Es un árbol degenerado (lista enlazada). Altura = 4. Complejidad = O(n).

**Ejercicio 2:** 
Implementa el método `altura(self, nodo)` que retorne la altura del árbol.
*Solución:*
```python
def altura(self, nodo):
    if nodo is None:
        return -1
    return 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
```

**Ejercicio 3:**
Explica qué imprimiría un recorrido Postorden del árbol del Ejemplo 2.
*Solución:* [2, 7, 5, 12, 17, 15, 10]

**Ejercicio 4:**
Implementa el método `contar_hojas(self)` recursivamente.
*Solución:*
```python
def contar_hojas(self):
    return self._contar_hojas_rec(self.raiz)

def _contar_hojas_rec(self, nodo):
    if nodo is None:
        return 0
    if nodo.izquierdo is None and nodo.derecho is None:
        return 1
    return self._contar_hojas_rec(nodo.izquierdo) + self._contar_hojas_rec(nodo.derecho)
```

## 6. Tarea / Homework

1. Implementa el método `eliminar(valor)` en la clase `ArbolBinarioBusqueda`. Asegúrate de manejar los 3 casos descritos en la teoría.
2. Implementa el recorrido por niveles (BFS - Breadth First Search) utilizando una Cola (`queue`).
3. Escribe una función que tome un árbol BST y retorne la suma de todos sus elementos sin modificar el árbol original.
4. Escribe un método `es_completo()` que valide si todos los nodos internos de un BST tienen exactamente dos hijos.
5. Crea una función `balancear_arbol()` que tome un BST potencialmente degenerado, extraiga sus elementos y construya un nuevo BST balanceado de altura mínima.

## 7. Mini-Proyecto

**Enunciado: Diccionario Inteligente**
Desarrolla un sistema de autocompletado y diccionario utilizando un Árbol Binario de Búsqueda. En este caso, el BST almacenará Objetos `Palabra`, los cuales contienen el texto de la palabra y su definición. 
Deberás:
1. Cargar al menos 50 palabras en el BST desde un archivo de texto o lista inicial. El ordenamiento en el árbol debe ser alfabético.
2. Permitir al usuario buscar una palabra exacta para obtener su definición.
3. Crear un método `buscar_por_prefijo(prefijo)` que retorne una lista con todas las palabras en el árbol que comiencen con ese prefijo (ej: "au" -> "auto", "autonomía", "aurora").
4. Generar una pequeña interfaz por consola donde el usuario pueda interactuar con el sistema (buscar, ver diccionario completo en orden, salir).

**Rúbrica (100 pts):**
* Implementación del BST orientada a objetos adaptada a strings (25 pts)
* Funcionalidad de Búsqueda Exacta (15 pts)
* Funcionalidad de Autocompletar / Búsqueda por prefijo (30 pts)
* Interfaz de consola interactiva amigable (20 pts)
* Código limpio, comentado y PEP8 (10 pts)

## 8. Recursos Adicionales
* VisuAlgo: Binary Search Tree (https://visualgo.net/en/bst)
* Python OOP Documentation
* Tree Traversals Visualization
