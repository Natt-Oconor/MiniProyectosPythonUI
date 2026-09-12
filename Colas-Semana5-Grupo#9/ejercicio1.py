"""
ejercicio1.py
Ejercicio 1: Imprimir el primer elemento de la cola sin modificarla.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de la clase Queue.
- Demostrar que la cola conserva intactos sus elementos y orden original.
"""

from queue_structure import Queue


def imprimir_primer_elemento(cola: Queue):
    """
    Obtiene e imprime el primer elemento (frente/cima) de la cola sin modificarla.
    """
    print(f"\nEstado actual de la cola: {cola}")
    
    # 1. Validación de cola vacía
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No tiene ningún elemento en el frente.")
        return None

    # 2. Consulta del frente mediante el método público front()
    primer_elemento = cola.front()
    print(f"[Resultado] El primer elemento de la cola es: {primer_elemento}")
    
    # 3. Comprobación de que la cola no fue modificada
    print(f"Estado tras la operación: {cola} (Sin cambios)")
    return primer_elemento


def main():
    print("=" * 60)
    print("  EJERCICIO 1: IMPRIMIR PRIMER ELEMENTO SIN MODIFICAR LA COLA")
    print("=" * 60)

    # Caso 1: Cola con varios elementos
    print("\n--- CASO 1: Cola con varios elementos ---")
    c1 = Queue()
    for val in ["Python", "Java", "C++", "JavaScript"]:
        c1.enqueue(val)
    imprimir_primer_elemento(c1)

    # Caso 2: Cola con un solo elemento
    print("\n--- CASO 2: Cola con un solo elemento ---")
    c2 = Queue()
    c2.enqueue(999)
    imprimir_primer_elemento(c2)

    # Caso 3: Cola vacía
    print("\n--- CASO 3: Cola vacía ---")
    c3 = Queue()
    imprimir_primer_elemento(c3)


if __name__ == "__main__":
    main()
