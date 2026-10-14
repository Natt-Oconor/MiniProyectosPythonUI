# -*- coding: utf-8 -*-
"""
Unidad 9: Arboles - Arbol Binario de Busqueda (BST)
Implementacion base (seccion 3 del U9_arboles.md) + metodos de la Tarea (seccion 6).
"""
from collections import deque

# Centinela para distinguir "altura() sin argumento" de "altura(None)"
_RAIZ = object()


class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # ------------------------------------------------------------------
    # Operaciones basicas (seccion 3)
    # ------------------------------------------------------------------
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, valor)
        else:
            # El valor ya existe; por diseno no admitimos duplicados
            pass

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        elif valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, valor)

    # ------------------------------------------------------------------
    # Recorridos de profundidad (seccion 3)
    # ------------------------------------------------------------------
    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo is not None:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    # ------------------------------------------------------------------
    # Utilidades (seccion 3 + practica en clase)
    # ------------------------------------------------------------------
    def min_valor(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo.valor

    def max_valor(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.valor

    def altura(self, nodo=_RAIZ):
        """Ejercicio 2: altura del arbol (-1 si esta vacio)."""
        if nodo is _RAIZ:
            nodo = self.raiz
        if nodo is None:
            return -1
        return 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))

    def contar_hojas(self):
        """Ejercicio 4: numero de hojas."""
        return self._contar_hojas_rec(self.raiz)

    def _contar_hojas_rec(self, nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return self._contar_hojas_rec(nodo.izquierdo) + self._contar_hojas_rec(nodo.derecho)

    def mostrar_arbol(self):
        """Muestra el arbol rotado 90 grados en consola."""
        self._imprimir_nodo(self.raiz, "", True)

    def _imprimir_nodo(self, nodo, prefijo, es_izquierdo):
        if nodo is not None:
            self._imprimir_nodo(nodo.derecho, prefijo + ("|   " if es_izquierdo else "    "), False)
            print(prefijo + ("\\-- " if es_izquierdo else "/-- ") + str(nodo.valor))
            self._imprimir_nodo(nodo.izquierdo, prefijo + ("    " if es_izquierdo else "|   "), True)

    # ==================================================================
    # TAREA / HOMEWORK (seccion 6)
    # ==================================================================
    def eliminar(self, valor):
        """Tarea 1: elimina un valor manejando los 3 casos:
        1) nodo hoja, 2) un hijo, 3) dos hijos (sucesor inorden).
        """
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor)
        else:
            # Caso 1: hoja / Caso 2: un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos -> sucesor inorden (minimo del subarbol derecho)
            sucesor = self._min_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor)
        return nodo

    def _min_nodo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def por_niveles(self):
        """Tarea 2: recorrido BFS (nivel por nivel) usando una Cola."""
        if self.raiz is None:
            return []
        resultado = []
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            if nodo.izquierdo is not None:
                cola.append(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.append(nodo.derecho)
        return resultado

    def suma_elementos(self):
        """Tarea 3: suma de todos los elementos sin modificar el arbol."""
        return self._suma_rec(self.raiz)

    def _suma_rec(self, nodo):
        if nodo is None:
            return 0
        return nodo.valor + self._suma_rec(nodo.izquierdo) + self._suma_rec(nodo.derecho)

    def es_completo(self):
        """Tarea 4: True si todos los nodos internos tienen exactamente dos hijos."""
        return self._es_completo_rec(self.raiz)

    def _es_completo_rec(self, nodo):
        if nodo is None:
            return True
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
        if nodo.izquierdo is not None and nodo.derecho is not None:
            return (self._es_completo_rec(nodo.izquierdo)
                    and self._es_completo_rec(nodo.derecho))
        return False


def _construir_balanceado(valores):
    """Tarea 5: construye un BST balanceado de altura minima a partir de una lista ordenada."""
    if not valores:
        return None
    medio = len(valores) // 2
    nodo = NodoArbol(valores[medio])
    nodo.izquierdo = _construir_balanceado(valores[:medio])
    nodo.derecho = _construir_balanceado(valores[medio + 1:])
    return nodo


def balancear_arbol(bst):
    """Tarea 5: toma un BST (posiblemente degenerado), extrae sus elementos
    y retorna un NUEVO BST balanceado de altura minima."""
    valores = bst.inorden()          # en un BST el inorden ya viene ordenado
    nuevo = ArbolBinarioBusqueda()
    nuevo.raiz = _construir_balanceado(valores)
    return nuevo
