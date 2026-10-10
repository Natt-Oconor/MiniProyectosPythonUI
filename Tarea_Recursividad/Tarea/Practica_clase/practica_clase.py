"""
Módulo de Práctica en Clase - Unidad 7: Recursividad.

Contiene las soluciones a los 5 ejercicios de práctica en clase:
1. Cuenta regresiva (countdown)
2. Invertir cadena
3. Potencia (a^b)
4. Palíndromo
5. Número máximo en una lista
"""

from typing import List, Union


class PracticaClase:
    """Implementación orientada a objetos de los ejercicios prácticos de clase."""

    @staticmethod
    def cuenta_regresiva(n: int, salida: List[str] = None) -> List[str]:
        """
        Ejercicio 1:
        Cuenta hacia atrás desde n e imprime / registra '¡Despegue!' al llegar a cero.

        - CASO BASE: Si n <= 0, se imprime / agrega '¡Despegue!' y finaliza la recursión.
        - CASO RECURSIVO: Se registra el número actual n y se invoca la función con n - 1.
        """
        if salida is None:
            salida = []

        # CASO BASE
        if n <= 0:
            salida.append("¡Despegue!")
            return salida

        # CASO RECURSIVO
        salida.append(str(n))
        return PracticaClase.cuenta_regresiva(n - 1, salida)

    @staticmethod
    def invertir_cadena(cadena: str) -> str:
        """
        Ejercicio 2:
        Invierte una cadena de texto de forma recursiva.

        - CASO BASE: Si la longitud de la cadena es 0 o 1, ya está invertida.
        - CASO RECURSIVO: Invertir el resto de la cadena (desde el índice 1)
                          y concatenar el primer carácter al final.
        """
        # CASO BASE
        if len(cadena) <= 1:
            return cadena

        # CASO RECURSIVO
        return PracticaClase.invertir_cadena(cadena[1:]) + cadena[0]

    @staticmethod
    def potencia(a: Union[int, float], b: int) -> Union[int, float]:
        """
        Ejercicio 3:
        Calcula a elevado a b (a^b) recursivamente.
        Soporta exponentes positivos, cero y negativos.

        - CASO BASE 1: b == 0 -> todo número elevado a 0 es 1 (excepto 0^0 definido convencionalmente como 1).
        - CASO BASE 2: Manejo de exponentes negativos: a^(-b) = 1 / (a^b).
        - CASO RECURSIVO: a * potencia(a, b - 1).
        """
        # Manejo de exponente negativo
        if b < 0:
            if a == 0:
                raise ZeroDivisionError("No se puede elevar 0 a un exponente negativo.")
            return 1 / PracticaClase.potencia(a, -b)

        # CASO BASE
        if b == 0:
            return 1

        # CASO RECURSIVO
        return a * PracticaClase.potencia(a, b - 1)

    @staticmethod
    def es_palindromo(palabra: str) -> bool:
        """
        Ejercicio 4:
        Verifica si una palabra o frase es un palíndromo de forma recursiva.
        Normaliza quitando espacios y pasando a minúsculas.

        - CASO BASE: Si la longitud es 0 o 1, es palíndromo (True).
        - CASO RECURSIVO: El primer y último carácter deben ser iguales,
                          y el sub-string interno debe ser también palíndromo.
        """
        # Limpieza previa de caracteres no alfanuméricos y mayúsculas
        texto = "".join(caracter.lower() for caracter in palabra if caracter.isalnum())

        def _verificar(cad: str) -> bool:
            # CASO BASE
            if len(cad) <= 1:
                return True
            # CASO RECURSIVO
            if cad[0] != cad[-1]:
                return False
            return _verificar(cad[1:-1])

        return _verificar(texto)

    @staticmethod
    def maximo_lista(lista: List[Union[int, float]]) -> Union[int, float]:
        """
        Ejercicio 5:
        Encuentra el número máximo en una lista recursivamente.

        - CASO BASE: Si la lista tiene un único elemento, ese es el máximo.
        - CASO RECURSIVO: Comparar el primer elemento con el máximo del resto de la lista.
        """
        if not lista:
            raise ValueError("La lista no puede estar vacía.")

        # CASO BASE
        if len(lista) == 1:
            return lista[0]

        # CASO RECURSIVO
        max_resto = PracticaClase.maximo_lista(lista[1:])
        return lista[0] if lista[0] > max_resto else max_resto


if __name__ == "__main__":
    print("=== Pruebas de Práctica en Clase ===")
    print("1. Countdown(3):", PracticaClase.cuenta_regresiva(3))
    print("2. Invertir 'recursividad':", PracticaClase.invertir_cadena("recursividad"))
    print("3. Potencia 2^5:", PracticaClase.potencia(2, 5))
    print("4. ¿'anita lava la tina' es palíndromo?:", PracticaClase.es_palindromo("anita lava la tina"))
    print("5. Máximo en [4, 9, 2, 15, 3]:", PracticaClase.maximo_lista([4, 9, 2, 15, 3]))
