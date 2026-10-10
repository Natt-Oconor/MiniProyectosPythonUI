# Unidad 7: Recursividad

## 1. Objetivos de Aprendizaje
- Entender profundamente el concepto de recursividad y cómo difiere de la iteración.
- Identificar y definir correctamente el "Caso Base" y el "Caso Recursivo".
- Visualizar y comprender cómo funciona la Pila de Llamadas (Call Stack).
- Identificar errores comunes de recursividad como el Stack Overflow.
- Aplicar técnicas como Memoización para optimizar soluciones recursivas redundantes.

## 2. Conceptos Teóricos

### ¿Qué es la Recursividad?
La recursividad ocurre cuando una función se llama a sí misma para resolver una versión más pequeña del mismo problema.
**Analogías**:
- **Muñecas Rusas (Matrioshkas)**: Abres una muñeca y dentro hay otra igual pero más pequeña, y así hasta encontrar la más pequeña que ya no se puede abrir (el caso base).
- **Espejos infinitos**: Si pones dos espejos frente a frente, ves reflejos dentro de reflejos. (¡Cuidado, esto no tiene caso base!).
- **Fractales**: Formas geométricas donde cada parte es una versión a escala reducida del todo.

### Las dos partes esenciales
Para que la recursión no sea infinita, SIEMPRE debe tener dos partes:
1. **Caso Base (Base Case)**: La condición de parada. La versión más simple del problema que se puede resolver directamente sin más llamadas recursivas.
2. **Caso Recursivo**: Donde la función se llama a sí misma con un problema modificado (acercándose al caso base).

### La Pila de Llamadas (Call Stack)
Cuando llamas a una función, la computadora pone esa ejecución "en pausa" si esta llama a otra función, guardando el estado en la pila de llamadas (una estructura LIFO: Last In, First Out).

```ascii
Llamada a factorial(3)
|-------------------|
| factorial(1) -> 1 |  <- ¡Caso Base alcanzado!
| factorial(2)      |  <- Esperando a factorial(1)
| factorial(3)      |  <- Esperando a factorial(2)
|-------------------|
Base de la memoria
```
Una vez que el tope de la pila se resuelve, devuelve su valor y se elimina, permitiendo que la llamada anterior continúe.

### Recursividad vs Iteración
Cualquier problema recursivo se puede resolver iterativamente (con bucles `while` o `for`), y viceversa.
- **Usa Recursividad cuando**: El problema se divide naturalmente en subproblemas similares (árboles, grafos, algoritmos de "divide y vencerás"). El código suele ser más limpio y fácil de leer.
- **Usa Iteración cuando**: El rendimiento y el uso de memoria son críticos.

### Problemas comunes
- **Stack Overflow**: Si olvidas el caso base o no te acercas a él, la pila de llamadas crecerá infinitamente hasta llenar la memoria y el programa crasheará.
- **Redundancia de cálculos**: A veces, la recursión ingenua resuelve el mismo problema varias veces (ej. Fibonacci).
- **Solución: Memoización**: Guardar los resultados de llamadas previas en un diccionario (caché) para reutilizarlos en lugar de volver a calcularlos.

## 3. Implementación en Python

```python
class Recursivo:
    """Clase utilitaria para agrupar métodos recursivos."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calcula el factorial de n recursivamente."""
        # CASO BASE
        if n == 0 or n == 1:
            return 1
        # CASO RECURSIVO
        return n * Recursivo.factorial(n - 1)
```

## 4. Ejemplos Resueltos

### Ejemplo 1: Factorial (y traza)
Calcula `n!`.
```python
print(Recursivo.factorial(4)) # 24
# Traza:
# fact(4) = 4 * fact(3)
# fact(3) = 3 * fact(2)
# fact(2) = 2 * fact(1)
# fact(1) = 1 (Retorna hacia atrás multiplicando: 1->2->6->24)
```

### Ejemplo 2: Fibonacci (Recursivo vs Memoización)
Secuencia: 0, 1, 1, 2, 3, 5, 8...

```python
class FibonacciSolver:
    @staticmethod
    def ingenuo(n: int) -> int:
        """O(2^n) - Muy lento para n grandes."""
        if n <= 0: return 0
        if n == 1: return 1
        return FibonacciSolver.ingenuo(n-1) + FibonacciSolver.ingenuo(n-2)
        
    @staticmethod
    def con_memoizacion(n: int, memo: dict = None) -> int:
        """O(n) - Ultra rápido."""
        if memo is None:
            memo = {}
            
        if n in memo:
            return memo[n]
            
        if n <= 0: return 0
        if n == 1: return 1
        
        # Guardar en el diccionario antes de retornar
        memo[n] = FibonacciSolver.con_memoizacion(n-1, memo) + FibonacciSolver.con_memoizacion(n-2, memo)
        return memo[n]

print(FibonacciSolver.con_memoizacion(50)) # 12586269025
```

### Ejemplo 3: Suma de Dígitos
Suma todos los dígitos de un número entero.

```python
class SumaDigitos:
    @staticmethod
    def sumar(n: int) -> int:
        if n == 0:
            return 0
        # n % 10 obtiene el último dígito
        # n // 10 quita el último dígito
        return (n % 10) + SumaDigitos.sumar(n // 10)

assert SumaDigitos.sumar(1234) == 10 # 1+2+3+4
```

### Ejemplo 4: Torres de Hanói
El clásico puzzle de mover discos.

```python
class Hanoi:
    @staticmethod
    def resolver(n: int, origen: str, destino: str, auxiliar: str):
        if n == 1:
            print(f"Mover disco 1 de {origen} a {destino}")
            return
            
        Hanoi.resolver(n-1, origen, auxiliar, destino)
        print(f"Mover disco {n} de {origen} a {destino}")
        Hanoi.resolver(n-1, auxiliar, destino, origen)

Hanoi.resolver(3, 'A', 'C', 'B')
```

### Ejemplo 5: Búsqueda Binaria Recursiva
Encuentra un elemento en una lista ordenada dividiendo a la mitad recursivamente.

```python
class BusquedaBinaria:
    @staticmethod
    def buscar(lista: list, objetivo: int, inicio: int, fin: int) -> int:
        # Caso base: no se encontró
        if inicio > fin:
            return -1
            
        medio = (inicio + fin) // 2
        
        # Caso base: lo encontramos
        if lista[medio] == objetivo:
            return medio
            
        # Casos recursivos
        if lista[medio] > objetivo:
            return BusquedaBinaria.buscar(lista, objetivo, inicio, medio - 1)
        else:
            return BusquedaBinaria.buscar(lista, objetivo, medio + 1, fin)

arreglo = [1, 3, 5, 7, 9, 11]
assert BusquedaBinaria.buscar(arreglo, 7, 0, len(arreglo)-1) == 3
```

## 5. Práctica en Clase
**Ejercicio 1**: Implementa una función recursiva que cuente hacia atrás (countdown) desde `n` e imprima "Despegue!" al llegar a cero.
*Solución Guiada*: Caso base: n == 0 (print). Recursivo: print(n), llamada a(n-1).

**Ejercicio 2**: Invierte una cadena recursivamente.
*Solución*: Caso base cadena vacía. Recursivo: `invertir(cadena[1:]) + cadena[0]`.

**Ejercicio 3**: Calcula `a` elevado a `b` recursivamente (a^b).
*Solución*: Caso base b == 0 (return 1). Recursivo: `a * potencia(a, b-1)`.

**Ejercicio 4**: Verifica si una palabra es un palíndromo recursivamente.
*Solución*: Caso base len <= 1 (True). Recursivo: `palabra[0] == palabra[-1] and es_palindromo(palabra[1:-1])`.

**Ejercicio 5**: Encuentra el número máximo en una lista recursivamente.
*Solución*: Compara el primer elemento con el máximo del resto de la lista `max(lista[0], recursivo(lista[1:]))`.

## 6. Tarea
1. **Multiplicación Rusa (sin operador `*`)**: Implementa una función recursiva que multiplique dos números `a` y `b` usando únicamente sumas. *Acompaña con análisis Big-O.*
2. **Conteo de Vocales**: Cuenta el número de vocales en un string recursivamente.
3. **Imprimir Patrón**: Dado un número `n`, imprime usando recursividad un patrón de asteriscos. Ejemplo para n=3:
   *
   **
   ***
4. **Caminos en un Tablero**: Escribe una función recursiva que calcule el número de caminos posibles desde la esquina superior izquierda (0,0) hasta la inferior derecha de una matriz NxM, asumiendo que solo puedes moverte hacia abajo o a la derecha. *Acompaña con análisis Big-O.*
5. **Flatten List**: Dada una lista que puede contener enteros u otras listas de enteros anidadas a cualquier nivel, retorna una única lista plana. Ej: `[1, [2, [3, 4], 5]] -> [1, 2, 3, 4, 5]`.

## 7. Mini-Proyecto: Explorador de Directorios
**Enunciado**:
Vas a simular un script que recorre el sistema de archivos (el cual representaremos como un diccionario anidado en Python).
Ejemplo de estructura:
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
Debes implementar una clase `ExploradorRecursivo` que contenga métodos recursivos para:
1. `imprimir_arbol(sistema, nivel)`: Que muestre gráficamente la estructura con indentaciones visuales.
2. `buscar_archivo(sistema, nombre)`: Que busque a qué ruta pertenece un archivo específico.
3. `contar_archivos(sistema)`: Retorna la cantidad total de archivos (las carpetas no cuentan).

**Rúbrica (100 puntos):**
- [30 pts] Implementación correcta de `imprimir_arbol` con indentación según el nivel recursivo.
- [30 pts] Búsqueda profunda correcta, sin crashear al llegar a las "hojas" del árbol.
- [20 pts] Conteo correcto de nodos hoja (archivos).
- [10 pts] Definición clara de los casos base y recursivos en comentarios.
- [10 pts] Código legible, estilo PEP8 y orientación a objetos.

## 8. Recursos Adicionales
- [VisuAlgo - Recursion Tree](https://visualgo.net/en/recursion)
- YouTube: "Recursion in Programming - Full Course" (freeCodeCamp).
- Artículo: "Understanding Call Stack and Recursion".
