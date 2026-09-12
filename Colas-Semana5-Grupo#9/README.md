# Tarea Semana 5 / Semana 6: Estructura de Datos Cola en Python / Grupo 9
**Base Orientadora de la Acción (BOA)**  
**Universidad Nacional Autónoma de Nicaragua, Managua (UNAN-Managua)**  
**Área de Conocimiento:** Ciencias Básicas y Tecnología  
**Carrera:** Ingeniería en Sistemas de Información (II Año / II Semestre)  
**Componente:** Programación con Estructuras de Datos  

---

## Contenido del Repositorio

| Archivo | Descripción |
| :--- | :--- |
| `queue_structure.py` | Implementación de la clase `Queue` con sus métodos públicos (`enqueue`, `dequeue`, `front`, `is_empty`, `size`, `clone`). |
| `laboratorio_guiado.py` | Resolución de las operaciones guiadas de la Actividad 2.1 (eliminar fondo, eliminar cima, vaciar, mover negativo al fondo, mover mayor a la cima). |
| `ejercicio1.py` | Ejercicio 1: Imprimir el primer elemento de la cola sin modificarla. |
| `ejercicio2.py` | Ejercicio 2: Imprimir la cantidad de elementos de la cola (con `size()` y con cola temporal). |
| `ejercicio3.py` | Ejercicio 3: Colocar en el fondo de la cola el número mayor. |
| `ejercicio4.py` | Ejercicio 4: Colocar en la cima de la cola el número menor. |
| `ejercicio5.py` | Ejercicio 5: Colocar en la cima de la cola el primer nombre que inicie con 'A'. |
| `ejercicio6.py` | Ejercicio 6: Colocar en el fondo de la cola el primer nombre que inicie con 'A'. |
| `ejercicio7.py` | Ejercicio 7: Invertir los elementos de una cola (versión iterativa con Pila LIFO y versión recursiva). |
| `ejercicio8.py` | Ejercicio 8: Sacar todos los ceros de la cola hacia una nueva colección sin modificar la cola original. |
| `ejercicio9.py` | Ejercicio 9: Crear una cola temporal con las raíces cuadradas de los valores sin modificar la original. |
| `integrantes.txt` | Ficha con nombres y carnets de los integrantes del equipo. |

---

## Acción 1: Comprensión de la Estructura de Datos Cola

### 1. Identificación del frente y del final de una cola
- **Frente (o Cima):** Es la posición de la cola por donde **salen** los elementos al ser atendidos (operación `dequeue`). Corresponde al elemento más antiguo que aún permanece en la estructura.
- **Final (o Fondo):** Es la posición por donde **ingresan** los nuevos elementos (operación `enqueue`). Corresponde al elemento agregado más recientemente.

### 2. Explicación del principio FIFO mediante un ejemplo sencillo
**FIFO** son las siglas en inglés de *First In, First Out* ("Primero en entrar, primero en salir").  
- **Ejemplo de la vida cotidiana:** La fila en la ventanilla de un banco o la taquilla de un cine. La primera persona que llega a la fila es la primera en ser atendida y salir. Los nuevos clientes que van llegando se forman al final de la fila y deben esperar a que todos los que llegaron antes que ellos sean atendidos. En ningún caso una persona que recién llega es atendida antes que los que ya estaban esperando (a menos que haya prioridad, lo cual sería otra estructura).

### 3. Diferenciación de las operaciones fundamentales
- `enqueue(elemento)`: Inserta un nuevo elemento al **fondo** de la cola. Incrementa el tamaño de la cola en 1.
- `dequeue()`: Remueve y retorna el elemento ubicado en el **frente** de la cola. Si la cola está vacía, genera un error o mensaje de advertencia. Disminuye el tamaño en 1.
- `front()` (o `peek()`): Devuelve una referencia o copia del elemento situado en el **frente** de la cola **sin removerlo**. Permite inspeccionar quién es el siguiente sin alterar la estructura.
- `is_empty()`: Operación booleana que retorna `True` si la cola no tiene ningún elemento (tamaño 0) y `False` si contiene al menos uno.
- `size()`: Retorna un número entero que representa la cantidad total de elementos almacenados en la cola en ese instante.

### 4. ¿Por qué encapsular la lógica de la cola dentro de una clase `Queue`?
1. **Abstracción:** Oculta los detalles internos de implementación (por ejemplo, si se usa una lista nativa de Python, arreglos estáticos o nodos enlazados). Quien usa la cola solo interactúa mediante operaciones con significado lógico (`enqueue`, `dequeue`, etc.).
2. **Integridad y Protección de Datos:** Evita que el usuario inserte o elimine elementos en posiciones intermedias (por ejemplo, impidiendo llamadas directas como `items.insert(2, x)` o `del items[3]`), garantizando que se cumpla estrictamente el principio FIFO.
3. **Mantenibilidad y Reutilización:** Permite cambiar la implementación interna (por ejemplo, optimizar usando `collections.deque` para $O(1)$) sin necesidad de modificar ni una sola línea del código cliente que utiliza la clase.

---

## Acción 2: Desarrollo del Laboratorio Guiado (`laboratorio_guiado.py`)

El script `laboratorio_guiado.py` implementa paso a paso las operaciones guiadas respetando las siguientes directrices:
- Uso exclusivo de métodos públicos de `Queue`.
- Uso de colas auxiliares para la manipulación y preservación del orden relativo.
- Validación de casos de cola vacía.

Las operaciones demostradas son:
1. `eliminar_cima(cola)`: Extrae directamente el elemento del frente usando `dequeue()`.
2. `eliminar_fondo(cola)`: Transfiere $N-1$ elementos a una cola temporal, extrae el último (fondo) y restaura los $N-1$ elementos a la cola original en su orden original.
3. `mover_primer_negativo_al_fondo(cola)`: Identifica el primer negativo mediante una pasada a una cola temporal, restaura los demás y finalmente encola el negativo al fondo.
4. `mover_mayor_a_la_cima(cola)`: Encuentra el valor máximo, lo inserta primero en la cola (para que sea la cima) y luego reinserta el resto en su orden relativo original omitiendo la ocurrencia reubicada.
5. `vaciar_cola(cola)`: Desencola secuencialmente hasta que `is_empty()` sea verdadero.

---

## Acción 3: Resolución de Ejercicios de Tarea

Todos los ejercicios cumplen con:
- Validación estricta de cola vacía.
- No alteración directa de `items` (encapsulamiento).
- Restauración del orden original cuando el ejercicio solicita no modificar la cola.
- Casos de prueba variados: caso normal, casos especiales (elementos únicos o en extremos) y cola vacía.

---

## Instrucciones de Ejecución

Para ejecutar cualquiera de los ejercicios o el laboratorio, abrir la terminal en esta carpeta y ejecutar con Python:

```bash
# Probar la clase Queue
python queue_structure.py

# Ejecutar el laboratorio guiado
python laboratorio_guiado.py

# Ejecutar los ejercicios individuales
python ejercicio1.py
python ejercicio2.py
python ejercicio3.py
python ejercicio4.py
python ejercicio5.py
python ejercicio6.py
python ejercicio7.py
python ejercicio8.py
python ejercicio9.py
```
