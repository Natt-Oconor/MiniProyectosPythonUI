"""
ejercicio5.py
Ejercicio 5: Colocar en la cima de la cola el primer nombre que inicie con 'A'.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Utilizar colas temporales para la reorganización.
- Conservar el orden relativo de los demás elementos.
- Manejar casos donde ningún nombre comience con 'A'.
"""

from queue_structure import Queue


def colocar_primer_nombre_con_a_en_cima(cola: Queue):
    """
    Busca el primer nombre que inicie con la letra 'A' (o 'a') y lo ubica
    en la cima (frente) de la cola, manteniendo intacto el orden de los demás.
    """
    print(f"\nCola ANTES de la operación: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No es posible realizar la operación.")
        return

    cola_temp = Queue()
    primer_nombre_a = None
    encontrado = False

    # 2. Extraer buscando el primer nombre que empiece con 'A'
    while not cola.is_empty():
        nombre = cola.dequeue()
        if (not encontrado and isinstance(nombre, str) and 
                nombre.strip().upper().startswith("A")):
            primer_nombre_a = nombre
            encontrado = True
        else:
            cola_temp.enqueue(nombre)

    # 3. Si se encontró, se coloca primero en la cima y luego el resto
    if encontrado:
        cola.enqueue(primer_nombre_a)
        while not cola_temp.is_empty():
            cola.enqueue(cola_temp.dequeue())
        print(f"[Resultado] Se colocó '{primer_nombre_a}' en la cima (frente) de la cola.")
    else:
        # Si no había ningún nombre con 'A', se restaura el orden original
        while not cola_temp.is_empty():
            cola.enqueue(cola_temp.dequeue())
        print("[Resultado] No se encontró ningún nombre que inicie con 'A'. La cola queda intacta.")

    print(f"Cola DESPUÉS de la operación: {cola}")


def main():
    print("=" * 65)
    print("  EJERCICIO 5: COLOCAR EN LA CIMA EL PRIMER NOMBRE CON 'A'")
    print("=" * 65)

    # Caso 1: Nombre con 'A' en medio de la cola
    print("\n--- CASO 1: Nombre con 'A' en medio de la cola ---")
    c1 = Queue()
    for nom in ["Carlos", "Beatriz", "Alejandro", "Daniela", "Ana"]:
        c1.enqueue(nom)
    colocar_primer_nombre_con_a_en_cima(c1)

    # Caso 2: El primer nombre ya inicia con 'A'
    print("\n--- CASO 2: Primer nombre ya inicia con 'A' ---")
    c2 = Queue()
    for nom in ["Andrea", "Marcos", "Lucía"]:
        c2.enqueue(nom)
    colocar_primer_nombre_con_a_en_cima(c2)

    # Caso 3: Ningún nombre inicia con 'A'
    print("\n--- CASO 3: Ningún nombre inicia con 'A' ---")
    c3 = Queue()
    for nom in ["Pedro", "María", "José", "Sofía"]:
        c3.enqueue(nom)
    colocar_primer_nombre_con_a_en_cima(c3)

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    colocar_primer_nombre_con_a_en_cima(c4)


if __name__ == "__main__":
    main()
