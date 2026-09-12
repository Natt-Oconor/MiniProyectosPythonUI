"""
ejercicio8.py
Ejercicio 8: Escribir un algoritmo que saque de la cola a todos los elementos ceros,
sin modificar la cola original.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de Queue.
- Cuando el enunciado indique que la cola no debe modificarse, restaure su contenido
  y orden original mediante colas temporales.
- Generar y retornar una cola resultante sin los ceros, reportando cuántos ceros fueron sacados.
"""

from queue_structure import Queue


def sacar_ceros_sin_modificar_cola(cola: Queue):
    """
    Identifica y extrae todos los elementos con valor 0 de la cola hacia una nueva
    cola de resultados, restaurando completamente la cola original a su estado y orden inicial.
    
    :param cola: Cola original a analizar.
    :return: Nueva cola sin elementos ceros.
    """
    print(f"\nCola original ANTES: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No hay elementos que procesar.")
        return Queue()

    cola_temp_restauracion = Queue()
    cola_sin_ceros = Queue()
    cantidad_ceros = 0

    # 2. Recorremos desencolando: separamos los no ceros y guardamos copia para restaurar
    while not cola.is_empty():
        val = cola.dequeue()
        cola_temp_restauracion.enqueue(val)  # Para restaurar la cola original
        
        if val == 0:
            cantidad_ceros += 1
        else:
            cola_sin_ceros.enqueue(val)

    # 3. Restauramos la cola original a su contenido y orden exacto
    while not cola_temp_restauracion.is_empty():
        cola.enqueue(cola_temp_restauracion.dequeue())

    print(f"[Resultado] Se detectaron y extrajeron {cantidad_ceros} cero(s).")
    print(f"[Cola resultante (sin ceros)]: {cola_sin_ceros}")
    print(f"Cola original DESPUÉS: {cola} (Comprobado: permanece idéntica)")

    return cola_sin_ceros


def main():
    print("=" * 65)
    print("  EJERCICIO 8: SACAR ELEMENTOS CEROS SIN MODIFICAR LA COLA")
    print("=" * 65)

    # Caso 1: Varios ceros intercalados
    print("\n--- CASO 1: Varios ceros intercalados ---")
    c1 = Queue()
    for n in [5, 0, 12, 0, 0, 8, 9, 0]:
        c1.enqueue(n)
    sacar_ceros_sin_modificar_cola(c1)

    # Caso 2: Cola sin ningún cero
    print("\n--- CASO 2: Cola sin ceros ---")
    c2 = Queue()
    for n in [10, 20, 30, 40]:
        c2.enqueue(n)
    sacar_ceros_sin_modificar_cola(c2)

    # Caso 3: Cola compuesta exclusivamente por ceros
    print("\n--- CASO 3: Cola solo con ceros ---")
    c3 = Queue()
    for n in [0, 0, 0]:
        c3.enqueue(n)
    sacar_ceros_sin_modificar_cola(c3)

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    sacar_ceros_sin_modificar_cola(c4)


if __name__ == "__main__":
    main()
