"""
ejercicio7.py
Ejercicio 7: Escribir un algoritmo que invierta los elementos de una cola.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Demostrar la inversión utilizando una estructura auxiliar tipo Pila (LIFO)
  así como también el enfoque recursivo.
"""

from queue_structure import Queue


def invertir_cola_con_pila(cola: Queue):
    """
    Invierte los elementos de una cola utilizando una pila auxiliar (LIFO).
    Al extraer en orden FIFO e insertar en LIFO, al desapilar se obtiene el orden inverso.
    """
    print(f"\nCola ANTES de invertir: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No hay elementos que invertir.")
        return

    # Si solo tiene un elemento, ya está invertida
    if cola.size() == 1:
        print("[Resultado] La cola solo tiene un elemento. Queda idéntica.")
        return

    pila_auxiliar = []

    # 2. Desencolar todos los elementos y apilarlos (FIFO -> LIFO)
    while not cola.is_empty():
        pila_auxiliar.append(cola.dequeue())

    # 3. Desapilar e insertar nuevamente en la cola
    while len(pila_auxiliar) > 0:
        cola.enqueue(pila_auxiliar.pop())

    print(f"[Resultado] Cola invertida con éxito.")
    print(f"Cola DESPUÉS de invertir: {cola}")


def invertir_cola_recursiva(cola: Queue):
    """
    Invierte la cola utilizando la pila de llamadas de la recursión,
    empleando únicamente métodos públicos de Queue.
    """
    if cola.is_empty():
        return

    # Paso recursivo: sacar el elemento del frente
    elemento = cola.dequeue()

    # Invertir el resto de la cola
    invertir_cola_recursiva(cola)

    # Encolar el elemento al fondo al regresar de la recursión
    cola.enqueue(elemento)


def main():
    print("=" * 65)
    print("      EJERCICIO 7: INVERTIR LOS ELEMENTOS DE UNA COLA")
    print("=" * 65)

    # Caso 1: Varios elementos utilizando Pila auxiliar
    print("\n--- CASO 1: Inversión con estructura auxiliar Pila (LIFO) ---")
    c1 = Queue()
    for item in [1, 2, 3, 4, 5]:
        c1.enqueue(item)
    invertir_cola_con_pila(c1)

    # Caso 2: Inversión con palabras
    print("\n--- CASO 2: Inversión con elementos de texto ---")
    c2 = Queue()
    for palabra in ["Primero", "Segundo", "Tercero", "Cuarto"]:
        c2.enqueue(palabra)
    invertir_cola_con_pila(c2)

    # Caso 3: Demostración con algoritmo recursivo
    print("\n--- CASO 3: Demostración alternativa con algoritmo recursivo ---")
    c3 = Queue()
    for n in [10, 20, 30, 40]:
        c3.enqueue(n)
    print(f"Cola ANTES de recursión: {c3}")
    invertir_cola_recursiva(c3)
    print(f"Cola DESPUÉS de recursión: {c3}")

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    invertir_cola_con_pila(c4)


if __name__ == "__main__":
    main()
