# -*- coding: utf-8 -*-
"""
Unidad 9 - Ejemplos resueltos (seccion 4 del U9_arboles.md).
Ejecutar: python ejemplos.py
"""
from arbol_bst import ArbolBinarioBusqueda


def ejemplo_1():
    print("=== Ejemplo 1: BST y propiedad inorden ===")
    bst = ArbolBinarioBusqueda()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insertar(val)
    print("Recorrido Inorden:", bst.inorden())
    print("Salida esperada : [20, 30, 40, 50, 60, 70, 80] -> ordenado\n")


def ejemplo_2():
    print("=== Ejemplo 2: Visualizando el arbol ===")
    bst = ArbolBinarioBusqueda()
    for val in [10, 5, 15, 2, 7, 12, 17]:
        bst.insertar(val)
    bst.mostrar_arbol()
    print()


def ejemplo_3():
    print("=== Ejemplo 3: Minimos y maximos ===")
    bst = ArbolBinarioBusqueda()
    for val in [42, 16, 8, 100, 23, 50]:
        bst.insertar(val)
    print("El valor mas pequeno es:", bst.min_valor())  # 8
    print("El valor mas grande es :", bst.max_valor())  # 100
    print()


def ejemplo_4():
    print("=== Ejemplo 4: Busqueda rapida ===")
    bst = ArbolBinarioBusqueda()
    for x in range(1, 1000, 2):  # impares del 1 al 999
        bst.insertar(x)
    print("Esta el 500?", bst.buscar(500))  # False
    print("Esta el 501?", bst.buscar(501))  # True
    print()


if __name__ == "__main__":
    ejemplo_1()
    ejemplo_2()
    ejemplo_3()
    ejemplo_4()
    print("Todos los ejemplos finalizaron correctamente.")
    input("\nPresione Enter para salir...")
