"""
Un profesor necesita administrar las calificaciones de sus estudiantes,
calcular promedios, determinar quienes aprueban o reprueban, y generar
un reporte final ordenado por rendimiento.

CONCEPTOS DE PROGRAMACION QUE DEBERAN APLICAR:
- Variables y tipos de datos (str, int, float, bool, list, dict)
- Entrada/salida de datos (input, print)
- Operadores aritméticos, relacionales y logicos
- Estructuras condicionales (if, elif, else)
- Estructuras repetitivas (for, while)
- Funciones (con y sin parametros, con y sin retorno)
- Listas y diccionarios
- Clases y objetos (POO)
- Encapsulamiento, herencia, polimorfismo
- Manejo de excepciones (try, except)
- Módulos y funciones principales (__main__)
========================================================================
"""
# ========================================================================
# 1. CONSTANTES GLOBALES
# ========================================================================
NOTA_MINIMA_APROBACION = 3.0
NOTA_MAXIMA = 5.0
NOTA_MINIMA = 0.0
CANTIDAD_NOTAS = 5

# ========================================================================
# 2. FUNCIONES AUXILIARES (sin retorno, sin parametros)
# ========================================================================
def funcion_mostrar_linea():
    """Imprime una linea de separacion, funcion sin parametros y sin retorno"""
    print("-" * 80)

def funcion_mostrar_encabezado(titulo):
    """Imprime un encabezado, funcion con parametros y sin retorno"""
    funcion_mostrar_linea()
    print(f"{titulo}")
    funcion_mostrar_linea()

def funcion_pausar():
    """Pausa la ejecucion del programa hasta que el usuario presione una tecla, funcion sin parametros"""
    input("Presione una tecla para continuar: ")

# ========================================================================
# 3. FUNCIONES CON RETORNO (operaciones y validaciones)
# ========================================================================
def funcion_leer_texto(mensaje):
    """Lee un texto desde la entrada estandar, funcion con parametros y con retorno"""
    while True:
        texto = input(f"{mensaje}").strip()
        if texto:
            return texto
        print("Advertencia: El texto no puede estar vacio. Intente nuevamente.")

# def funcion_leer_numero(mensaje, minimo, maximo):
#     """Lee un numero flotante y valida un rango"""
#     while True:
#         try:
#             numero = float(input(f"{mensaje}"))
#             if minimo <= numero <= maximo:
#                 return numero
#             else:
#                 print(f"Advertencia: El numero debe estar entre {minimo} y {maximo}. Intente nuevamente.")
#         except ValueError:
#             print("Error: Entrada invalida. Por favor ingrese un numero valido.")

#       def funcion_calcular_promedio(notas):
#         if(len(notas) == 0):
#           return 0.0

# return sum(notas) / len(notas)

# def funcion_determinar_estado(promedio):
#   """Determina el estado del estudiante segun su promedio"""
# if promedio >= NOTA_MINIMA_APROBACION:
#   return "Aprobado"
# else:
#   return "Reprobado"

def funcion_leer_numero(mensaje, minimo, maximo):
    """Lee un número flotante y valida un rango"""
    while True:
        try:
            numero = float(input(mensaje))

            if minimo <= numero <= maximo:
                return numero
            else:
                print(
                    f"Advertencia: El número debe estar entre "
                    f"{minimo} y {maximo}. Intente nuevamente."
                )

        except ValueError:
            print("Error: Entrada inválida. Por favor ingrese un número válido.")


def funcion_calcular_promedio(notas):
    """Calcula el promedio de una lista de notas"""

    if len(notas) == 0:
        return 0.0

    return sum(notas) / len(notas)


def funcion_determinar_estado(promedio):
    """Determina el estado del estudiante según su promedio"""

    if promedio >= NOTA_MINIMA_APROBACION:
        return "Aprobado"
    else:
        return "Reprobado"




def funcion_determinar_estado(promedio):
    """Determina el estado del estudiante según su promedio"""
    if promedio >= NOTA_MINIMA_APROBACION:
        return "Aprobado"
    else:
        return "Reprobado"

def funcion_determinar_mencion(promedio):
    """Determina la mención del estudiante según su promedio"""
    if promedio >= 4.5:
        return "Excelente"
    elif promedio >= 4.0:
        return "Muy Bueno"
    elif promedio >= 3.5:
        return "Bueno"
    elif promedio >= 3.0:
        return "Regular"
    else:
        return "En recuperacion"

#========================================================================
#4 CLASE ESTUDIANTE (POO - encapsulamiento, herencia, polimorfismo)
#========================================================================

class Estudiante:
    """
    Clase que representa a un estudiante con sus atributos y métodos.
    Encapsulamiento: Los atributos son privados y se accede a ellos mediante métodos.
    """

   #Variable de clase
    _cantidad_estudiantes = 0

    def __init__(self, NombreCompleto, edad, grado):
        """
        Inicializa un objeto Estudiante con nombre, apellido y lista de notas.
        Contructor de la clase
        self hace referncia al objeto actual
        """
        Estudiante._cantidad_estudiantes += 1
        self._id = Estudiante._cantidad_estudiantes
        self._NombreCompleto = NombreCompleto
        self._edad = edad
        self._grado = grado
        self._notas = [] #Declaracion de lista vacia que recibe las notas
        self._promedio = 0.0
        self._estado = ""
        self._mencion = ""
        self._rendimiento = ""

#======== GETTERS (Encapsulamiento) ========
@property
def id(self):
    """Devuelve el ID del estudiante"""
    return self._id

@property
def nombreCompleto(self):
    """Devuelve el nombre completo del estudiante"""
    return self._nombreCompleto

@property
def edad(self):
    """Devuelve la edad del estudiante"""
    return self._edad

@property
def grado(self):
    """Devuelve el grado del estudiante"""
    return self._grado

@property
def notas(self):
    """Devuelve el grado del estudiante"""
    return self._notas.copy()

@property
def promedio(self):
    """Devuelve el promedio del estudiante"""
    return self._promedio

@property
def estado(self):
    """Devuelve el estado del estudiante"""
    return self._estado

@property
def mencion(self):
    """Devuelve la mencion del estudiante"""
    return self._mencion

@property
def rendimiento(self):
    """Devuelve el rendimiento del estudiante"""
    return self._rendimiento

#======== SETTERS (modificadores) ========
@edad.setter
def edad(self, valor):
    """Establece la edad del estudiante"""
    if 0 < valor < 65:
        self._edad = valor
    else:
        raise ValueError("La edad debe ser un numero positivo.")