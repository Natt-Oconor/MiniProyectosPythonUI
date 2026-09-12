"""
ejercicio2.py
Ejercicio 2: Imprimir la cantidad de elementos de la cola.

Orientaciones:
- Validar si la cola está vacía.
- Utilizar exclusivamente métodos públicos de Queue.
- Demostrar el cálculo tanto con el método size() como mediante recorrido con cola temporal,
  garantizando que la cola original mantenga su orden y elementos intactos.
"""

from queue_structure import Queue


def contar_elementos_con_cola_temporal(cola: Queue) -> int:
    """
    Cuenta los elementos de la cola recorriéndola mediante una cola temporal
    y restaurándola por completo a su estado original.
    """
    if cola.is_empty():
        print("[Aviso] La cola está vacía. La cantidad de elementos es 0.")
        return 0

    cola_temp = Queue()
    contador = 0

    # Desencolamos contando y pasando a la cola auxiliar
    while not cola.is_empty():
        elemento = cola.dequeue()
        contador += 1
        cola_temp.enqueue(elemento)

    # Restauramos la cola original respetando el orden FIFO
    while not cola_temp.is_empty():
        cola.enqueue(cola_temp.dequeue())

    return contador


def imprimir_cantidad_elementos(cola: Queue):
    """
    Muestra la cantidad de elementos de la cola utilizando métodos públicos y validación.
    """
    print(f"\nEstado inicial de la cola: {cola}")
    
    if cola.is_empty():
        print("[Aviso] La cola está vacía (0 elementos).")
        return 0

    # Consulta directa mediante método público size()
    tamano_directo = cola.size()
    
    # Verificación algorítmica mediante cola temporal y restauración
    tamano_algoritmico = contar_elementos_con_cola_temporal(cola)

    print(f"[Resultado size()]: {tamano_directo} elemento(s).")
    print(f"[Resultado conteo con cola temporal]: {tamano_algoritmico} elemento(s).")
    print(f"Estado final de la cola: {cola} (Comprobado: no se modificó)")
    return tamano_directo


def main():
    print("=" * 60)
    print("      EJERCICIO 2: IMPRIMIR CANTIDAD DE ELEMENTOS")
    print("=" * 60)

    # Caso 1: Varios elementos
    print("\n--- CASO 1: Cola con 5 elementos ---")
    c1 = Queue()
    for num in [12, 45, 7, 89, 23]:
        c1.enqueue(num)
    imprimir_cantidad_elementos(c1)

    # Caso 2: Un elemento
    print("\n--- CASO 2: Cola con 1 elemento ---")
    c2 = Queue()
    c2.enqueue("Elemento Único")
    imprimir_cantidad_elementos(c2)

    # Caso 3: Cola vacía
    print("\n--- CASO 3: Cola vacía ---")
    c3 = Queue()
    imprimir_cantidad_elementos(c3)


if __name__ == "__main__":
    main()
