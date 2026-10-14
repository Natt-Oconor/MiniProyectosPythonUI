# -*- coding: utf-8 -*-
"""
Unidad 9 - Mini-Proyecto: Diccionario Inteligente (seccion 7 del U9_arboles.md).
BST de objetos Palabra (texto + definicion, orden alfabetico).
Funciones: busqueda exacta, busqueda por prefijo (autocompletado) e interfaz de consola.
Ejecutar: python diccionario_inteligente.py
"""
import os
from arbol_bst import NodoArbol, ArbolBinarioBusqueda

RUTA_PALABRAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palabras.txt")

PALABRAS_FALLBACK = [
    ("arbol", "Conjunto de nodos conectados de forma jerarquica."),
    ("algoritmo", "Conjunto finito de instrucciones para resolver un problema."),
    ("auto", "Vehiculo de motor con cuatro ruedas."),
    ("autonomia", "Capacidad de una persona o cosa para obrar por si misma."),
    ("aurora", "Luz que aparece en el horizonte antes de salir el sol."),
    ("balance", "Estado de equilibrio entre fuerzas o pesos."),
    ("busqueda", "Accion y efecto de buscar algo."),
    ("clase", "Conjunto de objetos que comparten atributos y metodos."),
    ("codigo", "Conjunto de instrucciones escritas en un lenguaje de programacion."),
    ("cola", "Estructura de datos FIFO: primero en entrar, primero en salir."),
    ("dato", "Representacion simbolica de un hecho o idea."),
    ("diccionario", "Repertorio ordenado de palabras de una lengua con sus definiciones."),
    ("grafo", "Estructura de datos formada por vertices y aristas."),
    ("hash", "Transformacion de datos en un valor de longitud fija."),
    ("heap", "Arbol binario completo usado en colas de prioridad."),
    ("inorden", "Recorrido: izquierda, raiz, derecha."),
    ("java", "Lenguaje de programacion orientado a objetos."),
    ("json", "Formato ligero de intercambio de datos."),
    ("lista", "Estructura de datos lineal de elementos ordenados."),
    ("modulo", "Unidad independiente de codigo reutilizable."),
    ("nodo", "Elemento de una estructura de datos que contiene un dato."),
    ("objeto", "Instancia de una clase en programacion orientada a objetos."),
    ("pila", "Estructura de datos LIFO: ultimo en entrar, primero en salir."),
    ("postorden", "Recorrido: izquierda, derecha, raiz."),
    ("preorden", "Recorrido: raiz, izquierda, derecha."),
    ("python", "Lenguaje de programacion interpretado y orientado a objetos."),
    ("queue", "Cola de datos (ingues) en estructuras de datos."),
    ("recursion", "Tecnica en la que una funcion se llama a si misma."),
    ("raiz", "Nodo superior de un arbol; no tiene padre."),
    ("arista", "Linea que conecta dos vertices en un grafo."),
    ("servidor", "Computadora que ofrece recursos a otras computers en red."),
    ("tabla", "Estructura de datos que almacena pares clave-valor."),
    ("template", "Plantilla reutilizable de codigo o documento."),
    ("usuario", "Persona que utiliza un sistema o programa."),
    ("valor", "Dato asignado a una variable o nodo."),
    ("variable", "Nombre que hace referencia a un valor en memoria."),
    ("vector", "Arreglo de una dimension con operaciones dinamicas."),
    ("while", "Bucle que repite mientras una condicion sea verdadera."),
    ("xml", "Lenguaje de marcado para estructurar datos."),
    ("archivo", "Conjunto de datos almacenados en un dispositivo."),
    ("binario", "Sistema de numeracion base 2 o relacion con dos elementos."),
    ("compilar", "Traducir codigo fuente a codigo ejecutable."),
    ("depurar", "Encontrar y corregir errores en un programa."),
    ("enlace", "Conexion entre dos nodos o paginas."),
    ("funcion", "Bloque de codigo que realiza una tarea especifica."),
    ("grafo_dirigido", "Grafo cuyas aristas tienen direccion."),
    ("herencia", "Mecanismo OOP donde una clase recibe atributos de otra."),
    ("iteracion", "Repeticion de un proceso un numero determinado de veces."),
    (" jerarquia", "Organizacion de elementos en niveles o rangos."),
    ("lenguaje", "Sistema de signos para comunicarse o programar."),
    ("metodo", "Funcion definida dentro de una clase."),
    ("objetivo", "Meta que se desea alcanzar con un proceso."),
    ("operacion", "Accion matematica o logica sobre datos."),
    ("puntero", "Variable que almacena la direccion de memoria de otro dato."),
    ("recorrido", "Forma de visitar todos los nodos de una estructura."),
    ("subarbol", "Arbol formado por un nodo y todos sus descendientes."),
    ("tiempo", "Duracion de una ejecucion o proceso."),
    ("vertex", "Vertice de un grafo (ingues)."),
    ("arreglo", "Coleccion de elementos del mismo tipo indexados."),
    ("buscar", "Accion de localizar un elemento en una estructura."),
    ("cadena", "Secuencia de caracteres de texto."),
    ("conjunto", "Agrupacion de elementos sin orden ni repeticion."),
    ("depuracion", "Proceso de encontrar errores en un programa."),
]


class Palabra:
    """Objeto que guarda una palabra y su definicion."""

    def __init__(self, texto, definicion):
        self.texto = texto.strip()
        self.definicion = definicion.strip()

    def __lt__(self, otro):
        return self.clave() < otro.clave()

    def __eq__(self, otro):
        return self.clave() == otro.clave()

    def __str__(self):
        return f"{self.texto}: {self.definicion}"

    def clave(self):
        return self.texto.lower()


class DiccionarioBST:
    """BST ordenado alfabeticamente que almacena objetos Palabra."""

    def __init__(self):
        self._arbol = ArbolBinarioBusqueda()
        self._cantidad = 0

    def __len__(self):
        return self._cantidad

    def insertar(self, palabra):
        nuevo = NodoArbol(palabra)
        if self._arbol.raiz is None:
            self._arbol.raiz = nuevo
            self._cantidad += 1
            return
        actual = self._arbol.raiz
        while True:
            if palabra.clave() < actual.valor.clave():
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    self._cantidad += 1
                    return
                actual = actual.izquierdo
            elif palabra.clave() > actual.valor.clave():
                if actual.derecho is None:
                    actual.derecho = nuevo
                    self._cantidad += 1
                    return
                actual = actual.derecho
            else:
                # palabra duplicada: actualiza la definicion
                actual.valor.definicion = palabra.definicion
                return

    def cargar_desde_archivo(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or "=" not in linea:
                    continue
                texto, definicion = linea.split("=", 1)
                self.insertar(Palabra(texto, definicion))
        return self._cantidad

    def buscar_exacta(self, texto):
        """2. Busqueda exacta de una palabra -> devuelve su definicion o None."""
        objetivo = texto.strip().lower()
        nodo = self._arbol.raiz
        while nodo is not None:
            clave = nodo.valor.clave()
            if objetivo == clave:
                return nodo.valor
            elif objetivo < clave:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho
        return None

    def buscar_por_prefijo(self, prefijo):
        """3. Retorna la lista de palabras que comienzan con el prefijo."""
        p = prefijo.strip().lower()
        if not p:
            return []
        resultado = []
        self._prefijo_rec(self._arbol.raiz, p, resultado)
        return resultado

    def _prefijo_rec(self, nodo, prefijo, resultado):
        if nodo is None:
            return
        clave = nodo.valor.clave()
        # Si el nodo actual es mayor al prefijo, hay que explorar la izquierda
        if clave >= prefijo:
            self._prefijo_rec(nodo.izquierdo, prefijo, resultado)
        # Nodo candidato
        if clave.startswith(prefijo):
            resultado.append(nodo.valor)
        # Si el nodo es menor al prefijo, el prefijo puede estar a la derecha;
        # si es mayor o igual tambien puede haber mas coincidencias a la derecha
        if clave <= prefijo or clave.startswith(prefijo):
            self._prefijo_rec(nodo.derecho, prefijo, resultado)
        elif clave > prefijo and not clave.startswith(prefijo):
            # el subarbol derecho tambien puede contener palabras >= prefijo
            self._prefijo_rec(nodo.derecho, prefijo, resultado)

    def listar_diccionario(self):
        """Diccionario completo en orden alfabetico (inorden)."""
        return self._arbol.inorden()

    def raiz_arbol(self):
        return self._arbol.raiz


def cargar_diccionario():
    dic = DiccionarioBST()
    if os.path.exists(RUTA_PALABRAS):
        total = dic.cargar_desde_archivo(RUTA_PALABRAS)
        print(f"Diccionario cargado desde palabras.txt ({total} palabras).")
    else:
        for texto, defi in PALABRAS_FALLBACK:
            dic.insertar(Palabra(texto, defi))
        print(f"AVISO: no se encontro palabras.txt; se usaron {len(dic)} palabras de respaldo.")
    return dic


def mostrar_lista(palabras, mensaje):
    print(f"\n{mensaje} ({len(palabras)}):")
    if not palabras:
        print("  (sin resultados)")
        return
    for p in palabras:
        print(f"  {p}")


def interfaz():
    print("=" * 60)
    print("  MINI-PROYECTO: DICCIONARIO INTELIGENTE (BST)")
    print("  Autocompletado y busqueda de palabras")
    print("=" * 60)
    dic = cargar_diccionario()

    acciones = {
        "1": lambda: buscar_exacta(dic),
        "2": lambda: buscar_prefijo(dic),
        "3": lambda: ver_diccionario(dic),
        "4": lambda: ver_estadisticas(dic),
    }

    while True:
        print("\n---------------- MENU ----------------")
        print(" 1. Buscar palabra exacta")
        print(" 2. Autocompletar por prefijo")
        print(" 3. Ver diccionario completo (A-Z)")
        print(" 4. Ver estadisticas del arbol")
        print(" 5. Salir")
        opcion = input("Seleccione una opcion [1-5]: ").strip()
        if opcion == "5":
            print("Hasta luego.")
            break
        if opcion in acciones:
            acciones[opcion]()
        else:
            print("Opcion no valida.")


def buscar_exacta(dic):
    texto = input("Palabra a buscar: ").strip()
    if not texto:
        return
    resultado = dic.buscar_exacta(texto)
    if resultado:
        print(f"\nSI existe: {resultado}")
    else:
        # sugerencias por prefijo (las 3 primeras letras)
        sugerencias = dic.buscar_por_prefijo(texto[:3])[:5] if len(texto) >= 3 else []
        print(f"\nNO se encontro '{texto}'.")
        if sugerencias:
            print("Quizas quisiste decir:")
            for s in sugerencias:
                print(f"  - {s.texto}")


def buscar_prefijo(dic):
    prefijo = input("Prefijo (ej: au): ").strip()
    if not prefijo:
        return
    mostrar_lista(dic.buscar_por_prefijo(prefijo), f"Palabras que empiezan con '{prefijo}'")


def ver_diccionario(dic):
    palabras = dic.listar_diccionario()
    mostrar_lista(palabras, "Diccionario completo en orden alfabetico")


def ver_estadisticas(dic):
    raiz = dic.raiz_arbol()
    print(f"\nPalabras cargadas : {len(dic)}")
    print(f"Altura del arbol  : {dic._arbol.altura()}")
    print(f"Minima palabra    : {dic._arbol.min_valor()}")
    print(f"Maxima palabra    : {dic._arbol.max_valor()}")
    if raiz is not None:
        print(f"Raiz (mediana)    : {raiz.valor}")


if __name__ == "__main__":
    try:
        interfaz()
    except (KeyboardInterrupt, EOFError):
        print("\nSesion terminada.")
