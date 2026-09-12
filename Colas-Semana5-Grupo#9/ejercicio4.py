"""
ejercicio4.py
Ejercicio 4: Colocar en la cima de la cola el número menor de la cola.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Utilizar colas temporales para la reorganización.
- Mantener intacto el orden relativo de los elementos restantes.
"""

from queue_structure import Queue


def colocar_menor_en_cima(cola: Queue):
    """
    Encuentra el menor valor de la cola y lo coloca en la cima (frente),
    manteniendo intacto el orden relativo de todos los demás elementos.
    """
    print(f"\nCola ANTES de la operación: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No es posible realizar la operación.")
        return

    # Si solo tiene un elemento, ya está en la cima
    if cola.size() == 1:
        print(f"[Resultado] La cola solo tiene un elemento ({cola.front()}). Permanece igual.")
        return

    cola_temp = Queue()

    # 2. Encontrar el número menor transfiriendo elementos a la cola temporal
    menor = cola.front()
    while not cola.is_empty():
        val = cola.dequeue()
        if val < menor:
            menor = val
        cola_temp.enqueue(val)

    # 3. Encolamos el menor primero en la cola original para que sea la CIMA (frente)
    cola.enqueue(menor)

    # 4. Encolamos los demás elementos omitiendo la ocurrencia del menor ya insertada
    omitido = False
    while not cola_temp.is_empty():
        val = cola_temp.dequeue()
        if val == menor and not omitido:
            omitido = True
        else:
            cola.enqueue(val)

    print(f"[Resultado] Se colocó el número menor ({menor}) en la cima (frente).")
    print(f"Cola DESPUÉS de la operación: {cola}")


def main():
    print("=" * 65)
    print("  EJERCICIO 4: COLOCAR EN LA CIMA EL NÚMERO MENOR")
    print("=" * 65)

    # Caso 1: Menor en medio de la cola
    print("\n--- CASO 1: Menor en el medio ---")
    c1 = Queue()
    for n in [34, 18, 4, 52, 9]:
        c1.enqueue(n)
    colocar_menor_en_cima(c1)

    # Caso 2: Menor al fondo de la cola
    print("\n--- CASO 2: Menor ubicado en el fondo ---")
    c2 = Queue()
    for n in [50, 40, 30, 20, 10]:
        c2.enqueue(n)
    colocar_menor_en_cima(c2)

    # Caso 3: Menor ya está en la cima
    print("\n--- CASO 3: Menor ya ubicado en la cima ---")
    c3 = Queue()
    for n in [2, 15, 28, 70]:
        c3.enqueue(n)
    colocar_menor_en_cima(c3)

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    colocar_menor_en_cima(c4)


if __name__ == "__main__":
    main()
