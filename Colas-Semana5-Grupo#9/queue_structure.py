"""
queue_structure.py
Módulo que define la estructura de datos Cola (Queue) utilizando el principio FIFO
(First In, First Out).

Asignatura: Programación con Estructuras de Datos
Carrera: Ingeniería en Sistemas de Información - UNAN-Managua
"""

class Queue:
    """
    Representación de una estructura de datos Cola (FIFO).
    Los elementos se agregan al final (fondo) y se extraen del inicio (frente o cima).
    """

    def __init__(self):
        """Inicializa una cola vacía."""
        self._items = []

    def enqueue(self, item):
        """
        Inserta un elemento al fondo (final) de la cola.
        
        :param item: Elemento a insertar en la cola.
        """
        self._items.append(item)

    def dequeue(self):
        """
        Elimina y retorna el elemento ubicado en el frente (cima) de la cola.
        
        :return: El elemento del frente.
        :raises IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("Error: No se puede realizar dequeue en una cola vacía.")
        return self._items.pop(0)

    def front(self):
        """
        Retorna el elemento en el frente de la cola sin eliminarlo.
        
        :return: El elemento del frente.
        :raises IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("Error: No se puede consultar el frente de una cola vacía.")
        return self._items[0]

    def is_empty(self) -> bool:
        """
        Verifica si la cola se encuentra vacía.
        
        :return: True si no contiene elementos, False en caso contrario.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Retorna la cantidad actual de elementos presentes en la cola.
        
        :return: Número entero con la longitud de la cola.
        """
        return len(self._items)

    def clone(self):
        """
        Crea y retorna una copia independiente de la cola actual respetando la interfaz pública.
        
        :return: Una nueva instancia de Queue con los mismos elementos en el mismo orden.
        """
        copia = Queue()
        temp = Queue()
        while not self.is_empty():
            elem = self.dequeue()
            copia.enqueue(elem)
            temp.enqueue(elem)
        while not temp.is_empty():
            self.enqueue(temp.dequeue())
        return copia

    def __str__(self) -> str:
        """
        Representación en cadena de texto de la cola para facilitar su visualización.
        Formato: [Frente/Cima] elem1 -> elem2 -> ... [Fondo]
        """
        if self.is_empty():
            return "Cola vacía: []"
        elementos_str = " -> ".join(str(elem) for elem in self._items)
        return f"[Frente/Cima] {elementos_str} [Fondo]"


# Prueba unitaria y verificación rápida de la estructura
if __name__ == "__main__":
    print("=== Comprobación de la clase Queue ===")
    cola_prueba = Queue()
    print(f"¿La cola está vacía inicialmente?: {cola_prueba.is_empty()}")
    print(f"Tamaño inicial: {cola_prueba.size()}")
    
    print("\nEncolando elementos: 10, 20, 30...")
    cola_prueba.enqueue(10)
    cola_prueba.enqueue(20)
    cola_prueba.enqueue(30)
    print(f"Estado de la cola: {cola_prueba}")
    print(f"Frente de la cola: {cola_prueba.front()}")
    print(f"Tamaño actual: {cola_prueba.size()}")
    
    print("\nDesencolando un elemento...")
    atendido = cola_prueba.dequeue()
    print(f"Elemento atendido (dequeue): {atendido}")
    print(f"Estado tras dequeue: {cola_prueba}")
    print(f"Nuevo frente: {cola_prueba.front()}")
    print("Prueba completada con éxito.")
