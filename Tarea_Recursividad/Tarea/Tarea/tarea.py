"""
Módulo de Tarea - Unidad 7: Recursividad.

Contiene las soluciones a los 5 ejercicios de la sección 6:
1. Multiplicación Rusa (sin operador `*`) usando únicamente sumas + Análisis Big-O.
2. Conteo de Vocales recursivo.
3. Imprimir Patrón de asteriscos.
4. Caminos en un Tablero (NxM) + Análisis Big-O (Recursivo puro y con Memoización).
5. Flatten List (Aplanar lista anidada a cualquier profundidad).
"""

from typing import Any, Dict, List, Tuple


class TareaRecursividad:
    """Implementación de los ejercicios asignados en la tarea de recursividad."""

    # =========================================================================
    # EJERCICIO 1: Multiplicación sin operador '*'
    # =========================================================================
    @staticmethod
    def multiplicacion_por_sumas(a: int, b: int) -> int:
        """
        Multiplica a * b utilizando únicamente sumas sucesivas de forma recursiva.

        - CASO BASE:
            - Si b == 0, cualquier número multiplicado por 0 es 0.
        - CASO RECURSIVO:
            - Si b > 0: a + multiplicacion_por_sumas(a, b - 1)
            - Si b < 0: -multiplicacion_por_sumas(a, -b)

        ANÁLISIS BIG-O:
        - Complejidad Temporal: O(|b|), ya que realiza |b| llamadas recursivas.
        - Complejidad Espacial: O(|b|) marcos en la pila de llamadas (Call Stack).
        """
        # CASO BASE
        if b == 0 or a == 0:
            return 0

        # Manejo de números negativos
        if b < 0:
            return -TareaRecursividad.multiplicacion_por_sumas(a, -b)

        # CASO RECURSIVO
        return a + TareaRecursividad.multiplicacion_por_sumas(a, b - 1)

    @staticmethod
    def multiplicacion_rusa(a: int, b: int) -> int:
        """
        Multiplicación Rusa (Campesina Rusa) sin operador '*'.
        Utiliza duplicación mediante sumas (a + a) y división entera (b // 2) o desplazamiento.

        Algoritmo:
        - Si b es impar, sumamos a al resultado y procedemos con (a + a, b // 2).
        - Si b es par, solo procedemos con (a + a, b // 2).

        - CASO BASE:
            - Si b == 0, el resultado es 0.
        - CASO RECURSIVO:
            - Si b % 2 == 1: a + multiplicacion_rusa(a + a, b // 2)
            - Si b % 2 == 0: multiplicacion_rusa(a + a, b // 2)

        ANÁLISIS BIG-O:
        - Complejidad Temporal: O(log |b|). En cada paso, b se reduce a la mitad.
        - Complejidad Espacial: O(log |b|) marcos en la pila de llamadas (Call Stack).
        """
        # CASO BASE
        if b == 0 or a == 0:
            return 0

        # Manejo de negativos
        if b < 0:
            return -TareaRecursividad.multiplicacion_rusa(a, -b)

        # CASO RECURSIVO
        if b % 2 == 1:
            return a + TareaRecursividad.multiplicacion_rusa(a + a, b // 2)
        else:
            return TareaRecursividad.multiplicacion_rusa(a + a, b // 2)

    # =========================================================================
    # EJERCICIO 2: Conteo de Vocales
    # =========================================================================
    @staticmethod
    def contar_vocales(cadena: str) -> int:
        """
        Cuenta el número de vocales (incluyendo acentuadas) en una cadena recursivamente.

        - CASO BASE:
            - Si la cadena está vacía (""), retorna 0.
        - CASO RECURSIVO:
            - Evalúa si el primer carácter es vocal (suma 1 o 0)
              más el conteo recursivo del resto de la cadena (cadena[1:]).

        ANÁLISIS BIG-O:
        - Complejidad Temporal: O(n), donde n = len(cadena).
        - Complejidad Espacial: O(n) debido a los marcos de recursión y rebanado (slicing).
        """
        # CASO BASE
        if not cadena:
            return 0

        vocales = "aeiouáéíóúAEIOUÁÉÍÓÚ"
        es_vocal = 1 if cadena[0] in vocales else 0

        # CASO RECURSIVO
        return es_vocal + TareaRecursividad.contar_vocales(cadena[1:])

    # =========================================================================
    # EJERCICIO 3: Imprimir Patrón de Asteriscos
    # =========================================================================
    @staticmethod
    def generar_patron(n: int, fila_actual: int = 1) -> List[str]:
        """
        Genera recursivamente las líneas del patrón de asteriscos para n filas.
        Ejemplo para n = 3:
        *
        **
        ***

        - CASO BASE:
            - Si fila_actual > n, retorna una lista vacía [].
        - CASO RECURSIVO:
            - Retorna ['*' * fila_actual] + generar_patron(n, fila_actual + 1).

        ANÁLISIS BIG-O:
        - Complejidad Temporal: O(n) llamadas recursivas, con O(n^2) construcción total de caracteres.
        - Complejidad Espacial: O(n) en la pila de llamadas.
        """
        # CASO BASE
        if fila_actual > n or n <= 0:
            return []

        # CASO RECURSIVO
        linea = "*" * fila_actual
        return [linea] + TareaRecursividad.generar_patron(n, fila_actual + 1)

    @staticmethod
    def imprimir_patron(n: int, fila_actual: int = 1) -> None:
        """
        Imprime directamente el patrón de asteriscos en la consola recursivamente.
        """
        # CASO BASE
        if fila_actual > n or n <= 0:
            return

        # Imprime la fila actual
        print("*" * fila_actual)

        # CASO RECURSIVO
        TareaRecursividad.imprimir_patron(n, fila_actual + 1)

    # =========================================================================
    # EJERCICIO 4: Caminos en un Tablero (NxM)
    # =========================================================================
    @staticmethod
    def caminos_tablero(n: int, m: int) -> int:
        """
        Calcula el número de caminos posibles desde (0,0) hasta (n-1, m-1)
        en una cuadrícula de NxM, moviéndose únicamente hacia abajo o a la derecha.

        Enfoque recursivo puro (divide y vencerás):

        - CASO BASE:
            - Si n <= 0 o m <= 0: no hay caminos válidos (retorna 0).
            - Si n == 1 o m == 1: solo hay una única línea recta hacia el destino (retorna 1).
        - CASO RECURSIVO:
            - La cantidad de caminos es la suma de moverse hacia abajo (n - 1, m)
              más la de moverse a la derecha (n, m - 1).

        ANÁLISIS BIG-O (Versión Ingenua):
        - Complejidad Temporal: O(2^(N+M)) o formalmente O(C(N+M-2, N-1)). Es exponencial
          porque recalcula subproblemas idénticos muchas veces.
        - Complejidad Espacial: O(N + M) marcos en la pila de llamadas (profundidad del árbol).
        """
        # CASO BASE: dimensiones inválidas
        if n <= 0 or m <= 0:
            return 0

        # CASO BASE: línea recta (frontera del tablero)
        if n == 1 or m == 1:
            return 1

        # CASO RECURSIVO
        return TareaRecursividad.caminos_tablero(n - 1, m) + TareaRecursividad.caminos_tablero(n, m - 1)

    @staticmethod
    def caminos_tablero_memo(n: int, m: int, memo: Dict[Tuple[int, int], int] = None) -> int:
        """
        Calcula el número de caminos posibles optimizado con MEMOIZACIÓN (Programación Dinámica).

        - CASO BASE:
            - Si ya está calculado en el diccionario `memo`: retorna memo[(n, m)].
            - Si n == 1 o m == 1: retorna 1.
        - CASO RECURSIVO:
            - Calcula y almacena en memo: caminos(n-1, m) + caminos(n, m-1).

        ANÁLISIS BIG-O (Versión Memoizada):
        - Complejidad Temporal: O(N * M). Cada par (n, m) se calcula exactamente una sola vez.
        - Complejidad Espacial: O(N * M) para almacenar la tabla/diccionario memo + O(N + M) de pila.
        """
        if memo is None:
            memo = {}

        if n <= 0 or m <= 0:
            return 0
        if n == 1 or m == 1:
            return 1

        clave = (n, m)
        if clave in memo:
            return memo[clave]

        # Almacenar en caché y retornar
        memo[clave] = (
            TareaRecursividad.caminos_tablero_memo(n - 1, m, memo)
            + TareaRecursividad.caminos_tablero_memo(n, m - 1, memo)
        )
        return memo[clave]

    # =========================================================================
    # EJERCICIO 5: Flatten List (Aplanar lista anidada)
    # =========================================================================
    @staticmethod
    def flatten_list(lista: List[Any]) -> List[Any]:
        """
        Dada una lista que puede contener enteros u otras listas de enteros
        anidadas a cualquier nivel, retorna una única lista plana.
        Ejemplo: [1, [2, [3, 4], 5]] -> [1, 2, 3, 4, 5]

        - CASO BASE:
            - Si la lista está vacía ([]), retorna [].
        - CASO RECURSIVO:
            - Se toma el primer elemento (lista[0]):
                * Si es una lista, se aplana recursivamente con flatten_list(lista[0]).
                * Si no es lista (ej. entero), se envuelve en [lista[0]].
            - Se concatena con el aplanado recursivo del resto: flatten_list(lista[1:]).

        ANÁLISIS BIG-O:
        - Complejidad Temporal: O(k), donde k es el número total de elementos atómicos y sublistas.
        - Complejidad Espacial: O(d) marcos de pila donde d es la profundidad máxima de anidación.
        """
        # CASO BASE
        if not lista:
            return []

        cabeza = lista[0]
        cola = lista[1:]

        # CASO RECURSIVO
        if isinstance(cabeza, list):
            return TareaRecursividad.flatten_list(cabeza) + TareaRecursividad.flatten_list(cola)
        else:
            return [cabeza] + TareaRecursividad.flatten_list(cola)


if __name__ == "__main__":
    print("=== Pruebas de la Tarea de Recursividad ===")
    print("1. Multiplicación Rusa (7 * 6):", TareaRecursividad.multiplicacion_rusa(7, 6))
    print("   Multiplicación por Sumas (7 * 6):", TareaRecursividad.multiplicacion_por_sumas(7, 6))
    print("2. Conteo de vocales ('Recursividad en Python'):", TareaRecursividad.contar_vocales("Recursividad en Python"))
    print("3. Patrón n=3:")
    TareaRecursividad.imprimir_patron(3)
    print("4. Caminos en tablero 3x3 (Ingenuo):", TareaRecursividad.caminos_tablero(3, 3))
    print("   Caminos en tablero 10x10 (Memoizado):", TareaRecursividad.caminos_tablero_memo(10, 10))
    print("5. Flatten List [1, [2, [3, 4], 5]]:", TareaRecursividad.flatten_list([1, [2, [3, 4], 5]]))
