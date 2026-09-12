"""
ejercicio6.py
Ejercicio 6: Colocar en el fondo de la cola el primer nombre que inicie con 'A'.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Utilizar colas temporales para la reorganización.
- Mantener el orden relativo de los elementos restantes.
- Manejar casos donde ningún nombre comience con 'A'.
"""

from queue_structure import Queue


def colocar_primer_nombre_con_a_en_fondo(cola: Queue):
    """
    Busca el primer nombre que inicie con la letra 'A' (o 'a') y lo traslada
    al fondo (final) de la cola, manteniendo el orden de los demás.
    """
    print(f"\nCola ANTES de la operación: {cola}")

    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No es posible realizar la operación.")
        return

    cola_temp = Queue()
    primer_nombre_a = None
    encontrado = False

    # 2. Extraer buscando el primer nombre que inicie con 'A'
    while not cola.is_empty():
        nombre = cola.dequeue()
        if (not encontrado and isinstance(nombre, str) and 
                nombre.strip().upper().startswith("A")):
            primer_nombre_a = nombre
            encontrado = True
        else:
            cola_temp.enqueue(nombre)

    # 3. Devolver los demás elementos a la cola original en su orden
    while not cola_temp.is_empty():
        cola.enqueue(cola_temp.dequeue())

    # 4. Si se encontró, se encola al final (fondo)
    if encontrado:
        cola.enqueue(primer_nombre_a)
        print(f"[Resultado] Se movió '{primer_nombre_a}' al fondo de la cola.")
    else:
        print("[Resultado] No se encontró ningún nombre que inicie con 'A'. La cola queda intacta.")

    print(f"Cola DESPUÉS de la operación: {cola}")


def main():
    print("=" * 65)
    print("  EJERCICIO 6: COLOCAR EN EL FONDO EL PRIMER NOMBRE CON 'A'")
    print("=" * 65)

    # Caso 1: Nombre con 'A' al frente
    print("\n--- CASO 1: Primer nombre con 'A' está al frente ---")
    c1 = Queue()
    for nom in ["Ana", "Bernardo", "Carlos", "Diana"]:
        c1.enqueue(nom)
    colocar_primer_nombre_con_a_en_fondo(c1)

    # Caso 2: Nombre con 'A' en el medio
    print("\n--- CASO 2: Primer nombre con 'A' en el medio ---")
    c2 = Queue()
    for nom in ["Mateo", "Luisa", "Alberto", "Esteban", "Adriana"]:
        c2.enqueue(nom)
    colocar_primer_nombre_con_a_en_fondo(c2)

    # Caso 3: Ningún nombre inicia con 'A'
    print("\n--- CASO 3: Ningún nombre inicia con 'A' ---")
    c3 = Queue()
    for nom in ["Felipe", "Gloria", "Hugo"]:
        c3.enqueue(nom)
    colocar_primer_nombre_con_a_en_fondo(c3)

    # Caso 4: Cola vacía
    print("\n--- CASO 4: Cola vacía ---")
    c4 = Queue()
    colocar_primer_nombre_con_a_en_fondo(c4)


if __name__ == "__main__":
    main()
