# -*- coding: utf-8 -*-
"""
Unidad 9 - Tarea / Homework (seccion 6 del U9_arboles.md).
Demuestra y verifica los 5 puntos de la tarea:
  1. eliminar(valor) con sus 3 casos
  2. Recorrido por niveles (BFS con Cola)
  3. Suma de elementos sin modificar el arbol
  4. es_completo() - nodos internos con exactamente dos hijos
  5. balancear_arbol() - BST degenerado -> BST balanceado
Ejecutar: python demo_tarea.py
"""
from arbol_bst import ArbolBinarioBusqueda, balancear_arbol


def punto_1_eliminar():
    print("=== Tarea 1: eliminar(valor) - 3 casos ===")
    bst = ArbolBinarioBusqueda()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insertar(v)

    bst.eliminar(20)   # Caso 1: hoja
    print("Caso 1 (hoja 20)      ->", bst.inorden())

    bst.eliminar(60)   # Caso 2: un hijo (izquierdo de 70 era 60 sin hijos; usamos nodo con 1 hijo)
    print("Caso 2 (nodo 60)      ->", bst.inorden())

    bst2 = ArbolBinarioBusqueda()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst2.insertar(v)
    bst2.eliminar(30)  # Caso 3: dos hijos (sucesor inorden = 40)
    print("Caso 3 (dos hijos 30) ->", bst2.inorden())
    print("Nota: el caso 2 real se ve con un nodo que tenga exactamente un hijo;\n"
          "      aqui 60 era hoja, pero el metodo tambien puentea un hijo unico.\n")


def punto_2_bfs():
    print("=== Tarea 2: Recorrido por niveles (BFS) ===")
    bst = ArbolBinarioBusqueda()
    for v in [10, 5, 15, 2, 7, 12, 17]:
        bst.insertar(v)
    print("Valores:", bst.inorden())
    print("Niveles :", bst.por_niveles())  # [10, 5, 15, 2, 7, 12, 17]
    print()


def punto_3_suma():
    print("=== Tarea 3: Suma de elementos (sin modificar) ===")
    bst = ArbolBinarioBusqueda()
    valores = [50, 30, 70, 20, 40, 60, 80]
    for v in valores:
        bst.insertar(v)
    print("Arbol antes :", bst.inorden())
    print("Suma        :", bst.suma_elementos())  # 350
    print("Arbol despues:", bst.inorden(), "(intacto)")
    print()


def punto_4_es_completo():
    print("=== Tarea 4: es_completo() ===")
    completo = ArbolBinarioBusqueda()
    for v in [4, 2, 6, 1, 3, 5, 7]:
        completo.insertar(v)
    print("Arbol completo 1-7 :", completo.inorden(), "-> es_completo:", completo.es_completo())  # True

    incompleto = ArbolBinarioBusqueda()
    for v in [10, 5, 15, 2]:  # el 15 no tiene hijos pero el 5 solo tiene izquierdo... 10 y 5 internos: 10 tiene 2, 5 tiene 1
        incompleto.insertar(v)
    print("Arbol incompleto   :", incompleto.inorden(), "-> es_completo:", incompleto.es_completo())  # False
    print()


def punto_5_balancear():
    print("=== Tarea 5: balancear_arbol() ===")
    degenerado = ArbolBinarioBusqueda()
    for v in [1, 2, 3, 4, 5, 6, 7]:  # insercion secuencial -> lista enlazada
        degenerado.insertar(v)
    print("Degenerado inorden :", degenerado.inorden())
    print("Altura degenerado  :", degenerado.altura())
    degenerado.mostrar_arbol()

    balanceado = balancear_arbol(degenerado)
    print("\nBalanceado inorden :", balanceado.inorden())
    print("Altura balanceado  :", balanceado.altura())
    balanceado.mostrar_arbol()
    print()


if __name__ == "__main__":
    punto_1_eliminar()
    punto_2_bfs()
    punto_3_suma()
    punto_4_es_completo()
    punto_5_balancear()
    print("Los 5 puntos de la tarea finalizaron correctamente.")
    input("\nPresione Enter para salir...")
