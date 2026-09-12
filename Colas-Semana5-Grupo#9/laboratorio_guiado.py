"""
laboratorio_guiado.py
Resolución de la Actividad 2.1: Implementar y utilizar una cola de números enteros en Python.

Operaciones guiadas:
1. Comprobación básica (inserción, eliminación, front, size, is_empty).
2. Eliminar el fondo.
3. Eliminar la cima o frente.
4. Vaciar la cola.
5. Mover el primer negativo al fondo (conservando el orden de los demás).
6. Mover el número mayor a la cima (conservando el orden de los demás).

Regla: Se utilizan exclusivamente los métodos públicos de Queue (sin acceder a atributos internos).
"""

from queue_structure import Queue


def imprimir_separador(titulo: str):
    """Función auxiliar para dar formato a la salida en consola."""
    print("\n" + "=" * 65)
    print(f"  {titulo}")
    print("=" * 65)


def eliminar_fondo(cola: Queue):
    """
    Elimina y retorna el elemento ubicado al fondo (final) de la cola,
    utilizando una cola auxiliar y conservando el orden de los demás elementos.
    """
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No hay fondo que eliminar.")
        return None

    if cola.size() == 1:
        return cola.dequeue()

    cola_temp = Queue()
    total_elementos = cola.size()

    # Pasamos los primeros (n - 1) elementos a la cola temporal
    for _ in range(total_elementos - 1):
        cola_temp.enqueue(cola.dequeue())

    # El elemento restante es el fondo
    fondo_eliminado = cola.dequeue()

    # Restauramos los elementos a la cola original
    while not cola_temp.is_empty():
        cola.enqueue(cola_temp.dequeue())

    return fondo_eliminado


def eliminar_cima(cola: Queue):
    """
    Elimina y retorna el elemento en la cima (frente) de la cola.
    """
    if cola.is_empty():
        print("[Aviso] La cola está vacía. No hay cima que eliminar.")
        return None
    return cola.dequeue()


def vaciar_cola(cola: Queue):
    """
    Elimina todos los elementos de la cola hasta dejarla vacía.
    """
    if cola.is_empty():
        print("[Aviso] La cola ya se encuentra vacía.")
        return

    elementos_removidos = 0
    while not cola.is_empty():
        cola.dequeue()
        elementos_removidos += 1
    print(f"[Éxito] Se eliminaron {elementos_removidos} elementos. La cola ha sido vaciada.")


def mover_primer_negativo_al_fondo(cola: Queue):
    """
    Busca el primer número negativo en la cola y lo mueve al fondo,
    manteniendo intacto el orden relativo de los demás elementos.
    """
    if cola.is_empty():
        print("[Aviso] La cola está vacía.")
        return

    cola_temp = Queue()
    primer_negativo = None
    encontrado = False

    # Extraemos elementos buscando el primer negativo
    while not cola.is_empty():
        val = cola.dequeue()
        if val < 0 and not encontrado:
            primer_negativo = val
            encontrado = True
        else:
            cola_temp.enqueue(val)

    # Devolvemos los elementos a la cola original
    while not cola_temp.is_empty():
        cola.enqueue(cola_temp.dequeue())

    # Si se encontró un negativo, lo encolamos al final (fondo)
    if encontrado:
        cola.enqueue(primer_negativo)
        print(f"[Resultado] Se movió el número negativo ({primer_negativo}) al fondo de la cola.")
    else:
        print("[Resultado] No se encontró ningún número negativo en la cola.")


def mover_mayor_a_la_cima(cola: Queue):
    """
    Encuentra el número mayor de la cola y lo coloca en la cima (frente),
    manteniendo intacto el orden relativo del resto de elementos.
    """
    if cola.is_empty():
        print("[Aviso] La cola está vacía.")
        return

    # Paso 1: Encontrar el número mayor transfiriendo a una cola temporal
    cola_temp = Queue()
    mayor = cola.front()

    while not cola.is_empty():
        val = cola.dequeue()
        if val > mayor:
            mayor = val
        cola_temp.enqueue(val)

    # Paso 2: Colocamos el mayor primero en la cola original (quedará en la cima/frente)
    cola.enqueue(mayor)

    # Paso 3: Reinsertamos los demás elementos omitiendo la primera ocurrencia del mayor
    omitido = False
    while not cola_temp.is_empty():
        val = cola_temp.dequeue()
        if val == mayor and not omitido:
            omitido = True  # Omitimos reinsertarlo porque ya se colocó al frente
        else:
            cola.enqueue(val)

    print(f"[Resultado] Se movió el número mayor ({mayor}) a la cima (frente) de la cola.")


def main():
    print("=================================================================")
    print("      LABORATORIO GUIADO: OPERACIONES CON COLAS EN PYTHON       ")
    print("=================================================================")

    # 1. Comprobación básica
    imprimir_separador("1. COMPROBACIÓN BÁSICA DE LA COLA")
    cola = Queue()
    print(f"Estado inicial de la cola: {cola}")
    print(f"¿Está vacía?: {cola.is_empty()}")
    print(f"Tamaño actual: {cola.size()}")

    print("\nInsertando elementos iniciales: [15, -4, 8, -20, 42, 7]...")
    for n in [15, -4, 8, -20, 42, 7]:
        cola.enqueue(n)
    print(f"Cola cargada: {cola}")
    print(f"Elemento en el frente (cima): {cola.front()}")
    print(f"Tamaño actual: {cola.size()}")

    # 2. Operación guiada: Eliminar la cima o frente
    imprimir_separador("2. OPERACIÓN: ELIMINAR LA CIMA O FRENTE")
    print(f"Cola ANTES: {cola}")
    eliminado_cima = eliminar_cima(cola)
    print(f"Elemento eliminado de la cima: {eliminado_cima}")
    print(f"Cola DESPUÉS: {cola}")

    # 3. Operación guiada: Eliminar el fondo
    imprimir_separador("3. OPERACIÓN: ELIMINAR EL FONDO")
    print(f"Cola ANTES: {cola}")
    eliminado_fondo = eliminar_fondo(cola)
    print(f"Elemento eliminado del fondo: {eliminado_fondo}")
    print(f"Cola DESPUÉS: {cola}")

    # 4. Operación guiada: Mover el primer negativo al fondo
    imprimir_separador("4. OPERACIÓN: MOVER EL PRIMER NEGATIVO AL FONDO")
    print(f"Cola ANTES: {cola}")
    mover_primer_negativo_al_fondo(cola)
    print(f"Cola DESPUÉS: {cola}")

    # 5. Operación guiada: Mover el número mayor a la cima
    imprimir_separador("5. OPERACIÓN: MOVER EL NÚMERO MAYOR A LA CIMA")
    print(f"Cola ANTES: {cola}")
    mover_mayor_a_la_cima(cola)
    print(f"Cola DESPUÉS: {cola}")

    # 6. Operación guiada: Vaciar la cola
    imprimir_separador("6. OPERACIÓN: VACIAR LA COLA")
    print(f"Cola ANTES: {cola}")
    vaciar_cola(cola)
    print(f"Cola DESPUÉS: {cola}")
    print(f"¿Está vacía?: {cola.is_empty()} (Tamaño: {cola.size()})")

    # 7. Validación con cola vacía
    imprimir_separador("7. PRUEBA DE OPERACIONES SOBRE COLA VACÍA")
    print("Intentando eliminar cima en cola vacía:")
    eliminar_cima(cola)
    print("Intentando eliminar fondo en cola vacía:")
    eliminar_fondo(cola)
    print("Intentando mover mayor a la cima en cola vacía:")
    mover_mayor_a_la_cima(cola)


if __name__ == "__main__":
    main()
