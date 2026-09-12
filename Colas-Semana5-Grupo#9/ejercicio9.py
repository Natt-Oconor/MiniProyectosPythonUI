"""
ejercicio9.py
Ejercicio 9: Asumir la existencia de una cola de enteros y crear una cola temporal con
las raíces cuadradas de todos los valores contenidos en la cola, sin modificar la cola original.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- No modificar la cola original; restaurar su contenido y orden original.
- Calcular la raíz cuadrada de cada número y almacenarla en una nueva cola.
"""

import math
from queue_structure import Queue


def crear_cola_raices_cuadradas(cola_original: Queue):
    """
    Genera y retorna una cola temporal con las raíces cuadradas de todos los valores
    contenidos en la cola original, garantizando que la cola original quede intacta.
    
    :param cola_original: Cola de números enteros.
    :return: Nueva cola con las raíces cuadradas calculadas.
    """
    print(f"\nCola original ANTES del cálculo: {cola_original}")

    # 1. Validación de cola vacía
    if cola_original.is_empty():
        print("[Aviso] La cola original está vacía. No hay raíces que calcular.")
        return Queue()

    cola_temp_restauracion = Queue()
    cola_raices = Queue()

    # 2. Recorremos desencolando cada elemento
    while not cola_original.is_empty():
        val = cola_original.dequeue()
        cola_temp_restauracion.enqueue(val)  # Para restaurar la cola original

        # Validación matemática para números enteros no negativos
        if val >= 0:
            raiz = math.sqrt(val)
            # Formato entero si la raíz es exacta, de lo contrario redondeado a 2 decimales
            raiz_formateada = int(raiz) if raiz.is_integer() else round(raiz, 2)
            cola_raices.enqueue(raiz_formateada)
        else:
            print(f"[Advertencia] El número {val} es negativo, no posee raíz cuadrada real.")
            cola_raices.enqueue(None)

    # 3. Restauramos íntegramente la cola original
    while not cola_temp_restauracion.is_empty():
        cola_original.enqueue(cola_temp_restauracion.dequeue())

    print(f"[Cola temporal con raíces cuadradas]: {cola_raices}")
    print(f"Cola original DESPUÉS: {cola_original} (Comprobado: permanece idéntica)")

    return cola_raices


def main():
    print("=" * 65)
    print("  EJERCICIO 9: COLA TEMPORAL CON RAÍCES CUADRADAS SIN MODIFICAR")
    print("=" * 65)

    # Caso 1: Cuadrados perfectos
    print("\n--- CASO 1: Cuadrados perfectos (4, 9, 16, 25, 100) ---")
    c1 = Queue()
    for n in [4, 9, 16, 25, 100]:
        c1.enqueue(n)
    crear_cola_raices_cuadradas(c1)

    # Caso 2: Números enteros mixtos
    print("\n--- CASO 2: Números enteros mixtos (2, 8, 20, 49, 50) ---")
    c2 = Queue()
    for n in [2, 8, 20, 49, 50]:
        c2.enqueue(n)
    crear_cola_raices_cuadradas(c2)

    # Caso 3: Cola vacía
    print("\n--- CASO 3: Cola vacía ---")
    c3 = Queue()
    crear_cola_raices_cuadradas(c3)


if __name__ == "__main__":
    main()
