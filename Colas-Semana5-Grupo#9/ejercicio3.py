"""
ejercicio3.py
Ejercicio 3: Colocar en el fondo de la cola el número mayor de la cola.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Utilizar colas temporales para realizar la reorganización.
- Garantizar que los elementos no seleccionados conserven su orden relativo original.
"""

from queue_structure import Queue


def colocar_mayor_al_fondo(cola: Queue):
    """
    Encuentra el valor máximo de la cola y lo mueve al fondo (final),
    manteniendo el orden relativo de todos los demás elementos.
    """
    print(f"\nCola ANTES de la operación: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No es posible realizar la operación.")
        return

    # Si solo tiene un elemento, ya se encuentra en el fondo
    if cola.size() == 1:
        print(f"[Resultado] La cola solo tiene un elemento ({cola.front()}). Permanece igual.")
        return

    cola_temp = Queue()

    # 2. Encontrar el número mayor mientras transferimos a la cola temporal
    mayor = cola.front()
    while not cola.is_empty():
        val = cola.dequeue()
        if val > mayor:
            mayor = val
        cola_temp.enqueue(val)

    # 3. Transferir de vuelta a la cola original omitiendo la primera ocurrencia del mayor
    omitido = False
    while not cola_temp.is_empty():
        val = cola_temp.dequeue()
        if val == mayor and not omitido:
            omitido = True  # Omitimos insertarlo aquí para colocarlo al final
        else:
            cola.enqueue(val)

    # 4. Encolar el número mayor al fondo de la cola
    cola.enqueue(mayor)

    print(f"[Resultado] Se movió el número mayor ({mayor}) al fondo.")
    print(f"Cola DESPUÉS de la operación: {cola}")


def main():
    print("=" * 65)
    print("  EJERCICIO 3: COLOCAR EN EL FONDO EL NÚMERO MAYOR")
    print("=" * 65)

    # Caso 1: Mayor en medio de la cola
    print("\n--- CASO 1: Mayor en el medio ---")
    c1 = Queue()
    for n in [14, 88, 23, 5, 41]:
        c1.enqueue(n)
    colocar_mayor_al_fondo(c1)

    # Caso 2: Mayor ya se encuentra al inicio (cima)
    print("\n--- CASO 2: Mayor en la cima (frente) ---")
    c2 = Queue()
    for n in [99, 10, 20, 30]:
        c2.enqueue(n)
    colocar_mayor_al_fondo(c2)

    # Caso 3: Mayor ya se encuentra al fondo
    print("\n--- CASO 3: Mayor ya en el fondo ---")
    c3 = Queue()
    for n in [10, 20, 30, 99]:
        c3.enqueue(n)
    colocar_mayor_al_fondo(c3)

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    colocar_mayor_al_fondo(c4)


if __name__ == "__main__":
    main()
