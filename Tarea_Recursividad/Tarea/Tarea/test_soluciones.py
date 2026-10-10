"""
Módulo de Pruebas Unitarias Automatizadas.
Valida todas las soluciones de la Unidad 7 (Práctica, Tarea y Mini-Proyecto).
"""

import unittest
from practica_clase import PracticaClase
from tarea import TareaRecursividad
from explorador_directorios import ExploradorRecursivo


class TestPracticaClase(unittest.TestCase):
    def test_cuenta_regresiva(self):
        resultado = PracticaClase.cuenta_regresiva(3)
        self.assertEqual(resultado, ["3", "2", "1", "¡Despegue!"])
        self.assertEqual(PracticaClase.cuenta_regresiva(0), ["¡Despegue!"])

    def test_invertir_cadena(self):
        self.assertEqual(PracticaClase.invertir_cadena("recursividad"), "dadivisrucer")
        self.assertEqual(PracticaClase.invertir_cadena("a"), "a")
        self.assertEqual(PracticaClase.invertir_cadena(""), "")

    def test_potencia(self):
        self.assertEqual(PracticaClase.potencia(2, 0), 1)
        self.assertEqual(PracticaClase.potencia(2, 5), 32)
        self.assertEqual(PracticaClase.potencia(5, 3), 125)
        self.assertEqual(PracticaClase.potencia(2, -2), 0.25)
        with self.assertRaises(ZeroDivisionError):
            PracticaClase.potencia(0, -1)

    def test_es_palindromo(self):
        self.assertTrue(PracticaClase.es_palindromo("radar"))
        self.assertTrue(PracticaClase.es_palindromo("anita lava la tina"))
        self.assertTrue(PracticaClase.es_palindromo("A"))
        self.assertTrue(PracticaClase.es_palindromo(""))
        self.assertFalse(PracticaClase.es_palindromo("recursivo"))

    def test_maximo_lista(self):
        self.assertEqual(PracticaClase.maximo_lista([4, 9, 2, 15, 3]), 15)
        self.assertEqual(PracticaClase.maximo_lista([-5, -1, -10]), -1)
        self.assertEqual(PracticaClase.maximo_lista([42]), 42)
        with self.assertRaises(ValueError):
            PracticaClase.maximo_lista([])


class TestTareaRecursividad(unittest.TestCase):
    def test_multiplicacion_por_sumas(self):
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(6, 7), 42)
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(5, 0), 0)
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(0, 10), 0)
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(-4, 5), -20)
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(4, -5), -20)
        self.assertEqual(TareaRecursividad.multiplicacion_por_sumas(-3, -3), 9)

    def test_multiplicacion_rusa(self):
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(6, 7), 42)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(18, 23), 414)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(0, 50), 0)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(50, 0), 0)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(-7, 8), -56)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(7, -8), -56)
        self.assertEqual(TareaRecursividad.multiplicacion_rusa(-5, -5), 25)

    def test_contar_vocales(self):
        self.assertEqual(TareaRecursividad.contar_vocales("recursivo"), 4)
        self.assertEqual(TareaRecursividad.contar_vocales("Murciélago"), 5)
        self.assertEqual(TareaRecursividad.contar_vocales("xyz"), 0)
        self.assertEqual(TareaRecursividad.contar_vocales(""), 0)
        self.assertEqual(TareaRecursividad.contar_vocales("Árbol Épico"), 5)

    def test_patron_asteriscos(self):
        patron_3 = TareaRecursividad.generar_patron(3)
        self.assertEqual(patron_3, ["*", "**", "***"])
        self.assertEqual(TareaRecursividad.generar_patron(1), ["*"])
        self.assertEqual(TareaRecursividad.generar_patron(0), [])

    def test_caminos_tablero(self):
        # En una matriz 1x1, 1xM o Nx1 hay exactamente 1 camino (línea recta)
        self.assertEqual(TareaRecursividad.caminos_tablero(1, 1), 1)
        self.assertEqual(TareaRecursividad.caminos_tablero(1, 5), 1)
        self.assertEqual(TareaRecursividad.caminos_tablero(5, 1), 1)
        # Matriz 2x2 -> 2 caminos (abajo-derecha, derecha-abajo)
        self.assertEqual(TareaRecursividad.caminos_tablero(2, 2), 2)
        # Matriz 3x3 -> 6 caminos (C(4, 2) = 6)
        self.assertEqual(TareaRecursividad.caminos_tablero(3, 3), 6)
        # Comparación versión memoizada
        self.assertEqual(TareaRecursividad.caminos_tablero_memo(3, 3), 6)
        self.assertEqual(TareaRecursividad.caminos_tablero_memo(10, 10), 48620)

    def test_flatten_list(self):
        entrada = [1, [2, [3, 4], 5]]
        esperado = [1, 2, 3, 4, 5]
        self.assertEqual(TareaRecursividad.flatten_list(entrada), esperado)
        self.assertEqual(TareaRecursividad.flatten_list([]), [])
        self.assertEqual(TareaRecursividad.flatten_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(TareaRecursividad.flatten_list([[[[7]]]]), [7])
        self.assertEqual(TareaRecursividad.flatten_list([[1, 2], [3, [4, [5]]]]), [1, 2, 3, 4, 5])


class TestExploradorRecursivo(unittest.TestCase):
    def setUp(self):
        self.sistema = {
            "Documentos": {
                "apuntes.txt": "10kb",
                "fotos": {
                    "vacaciones.png": "2mb",
                    "perro.jpg": "1mb",
                },
            },
            "sistema.dll": "500kb",
        }

    def test_contar_archivos(self):
        # Hay 4 archivos en total: apuntes.txt, vacaciones.png, perro.jpg, sistema.dll
        total = ExploradorRecursivo.contar_archivos(self.sistema)
        self.assertEqual(total, 4)
        self.assertEqual(ExploradorRecursivo.contar_archivos({}), 0)

    def test_buscar_archivo(self):
        # Archivo en la raíz
        self.assertEqual(
            ExploradorRecursivo.buscar_archivo(self.sistema, "sistema.dll"),
            "sistema.dll"
        )
        # Archivo en primer subdirectorio
        self.assertEqual(
            ExploradorRecursivo.buscar_archivo(self.sistema, "apuntes.txt"),
            "Documentos/apuntes.txt"
        )
        # Archivo anidado profundamente
        self.assertEqual(
            ExploradorRecursivo.buscar_archivo(self.sistema, "vacaciones.png"),
            "Documentos/fotos/vacaciones.png"
        )
        # Archivo que no existe
        self.assertIsNone(ExploradorRecursivo.buscar_archivo(self.sistema, "fantasma.iso"))

    def test_obtener_arbol_como_texto(self):
        lineas = ExploradorRecursivo.obtener_arbol_como_texto(self.sistema)
        self.assertTrue(any("[Carpeta] Documentos/" in l for l in lineas))
        self.assertTrue(any("[Carpeta] fotos/" in l for l in lineas))
        self.assertTrue(any("vacaciones.png" in l for l in lineas))
        self.assertTrue(any("sistema.dll" in l for l in lineas))


if __name__ == "__main__":
    unittest.main()
