"""
Mini-Proyecto: Explorador de Directorios - Unidad 7: Recursividad.

Implementación de la clase `ExploradorRecursivo` que simula la navegación
e inspección de un sistema de archivos representado mediante diccionarios anidados.

Rúbrica de Evaluación (100 puntos):
- [30 pts] Implementación correcta de `imprimir_arbol` con indentación según el nivel.
- [30 pts] Búsqueda profunda correcta (`buscar_archivo`), sin crashear en hojas.
- [20 pts] Conteo correcto de nodos hoja / archivos (`contar_archivos`).
- [10 pts] Definición clara de los casos base y recursivos en comentarios.
- [10 pts] Código legible, estilo PEP8 y orientación a objetos.
"""

from typing import Any, Dict, List, Optional, Union


class ExploradorRecursivo:
    """
    Clase utilitaria orientada a objetos para explorar, visualizar y analizar
    estructuras jerárquicas de sistemas de archivos simulados con diccionarios.
    """

    # =========================================================================
    # 1. IMPRIMIR ÁRBOL DE DIRECTORIOS (30 pts)
    # =========================================================================
    @staticmethod
    def imprimir_arbol(sistema: Dict[str, Any], nivel: int = 0) -> None:
        """
        Muestra gráficamente en consola la estructura del sistema de archivos
        con indentaciones visuales acordes a la profundidad del nivel recursivo.

        - CASO BASE:
            - Un elemento cuyo contenido no es un diccionario (nodo hoja / archivo).
              Se imprime con sangría correspondiente indicando su nombre y tamaño.
        - CASO RECURSIVO:
            - Un elemento cuyo contenido es un diccionario (directorio / carpeta).
              Se imprime el directorio y se invoca recursivamente `imprimir_arbol`
              sobre su contenido con nivel + 1.
        """
        if not isinstance(sistema, dict):
            return

        sangria = "    " * nivel

        for clave, valor in sistema.items():
            if isinstance(valor, dict):
                # CASO RECURSIVO: Es una carpeta / subdirectorio
                print(f"{sangria}+-- [Carpeta] {clave}/")
                ExploradorRecursivo.imprimir_arbol(valor, nivel + 1)
            else:
                # CASO BASE: Es un archivo (hoja del árbol)
                print(f"{sangria}|-- [Archivo] {clave} ({valor})")

    @staticmethod
    def obtener_arbol_como_texto(sistema: Dict[str, Any], nivel: int = 0) -> List[str]:
        """
        Genera recursivamente una lista de líneas de texto con la representación visual
        del árbol de directorios (útil para pruebas unitarias y registros).
        """
        lineas: List[str] = []
        if not isinstance(sistema, dict):
            return lineas

        sangria = "    " * nivel

        for clave, valor in sistema.items():
            if isinstance(valor, dict):
                # CASO RECURSIVO
                lineas.append(f"{sangria}+-- [Carpeta] {clave}/")
                lineas.extend(ExploradorRecursivo.obtener_arbol_como_texto(valor, nivel + 1))
            else:
                # CASO BASE
                lineas.append(f"{sangria}|-- [Archivo] {clave} ({valor})")

        return lineas

    # =========================================================================
    # 2. BÚSQUEDA PROFUNDA DE UN ARCHIVO (30 pts)
    # =========================================================================
    @staticmethod
    def buscar_archivo(
        sistema: Dict[str, Any], nombre: str, ruta_actual: str = ""
    ) -> Optional[str]:
        """
        Busca a qué ruta pertenece un archivo específico en el sistema de archivos.
        Retorna la ruta completa (ejemplo: 'Documentos/fotos/vacaciones.png') o None si no existe.

        - CASO BASE 1 (Archivo encontrado):
            - Si la clave coincide con `nombre` y su valor NO es un diccionario,
              hemos alcanzado la hoja objetivo y se retorna la ruta acumulada.
        - CASO BASE 2 (No encontrado en rama):
            - Si el nodo no contiene subcarpetas ni el archivo, el flujo termina sin éxito.
        - CASO RECURSIVO:
            - Para cada clave cuyo valor sea un diccionario (carpeta), se realiza
              una llamada recursiva explorando esa subcarpeta, agregando el nombre de
              la carpeta a la ruta acumulada (`ruta_actual / clave`).
        """
        if not isinstance(sistema, dict):
            return None

        for clave, valor in sistema.items():
            # Construcción de la ruta para el elemento actual
            ruta_elemento = f"{ruta_actual}/{clave}" if ruta_actual else clave

            # CASO BASE 1: Encontramos el archivo buscado
            if clave == nombre and not isinstance(valor, dict):
                return ruta_elemento

            # CASO RECURSIVO: Es una carpeta, buscamos en profundidad
            if isinstance(valor, dict):
                resultado = ExploradorRecursivo.buscar_archivo(valor, nombre, ruta_elemento)
                if resultado is not None:
                    return resultado

        # CASO BASE 2: No se encontró en este nivel ni en sus subdirectorios
        return None

    # =========================================================================
    # 3. CONTEO TOTAL DE ARCHIVOS (20 pts)
    # =========================================================================
    @staticmethod
    def contar_archivos(sistema: Dict[str, Any]) -> int:
        """
        Retorna la cantidad total de archivos en el sistema.
        Las carpetas o directorios intermedios no se cuentan, solo las hojas.

        - CASO BASE:
            - Para cada clave cuyo valor NO sea un diccionario (nodo hoja/archivo),
              se aporta exactamente 1 unidad al conteo.
        - CASO RECURSIVO:
            - Si el valor ES un diccionario (subcarpeta), se suma el resultado de
              invocar recursivamente `contar_archivos(valor)`.
        """
        if not isinstance(sistema, dict):
            return 0

        total_archivos = 0

        for valor in sistema.values():
            if isinstance(valor, dict):
                # CASO RECURSIVO: Entrar a la subcarpeta y sumar sus archivos
                total_archivos += ExploradorRecursivo.contar_archivos(valor)
            else:
                # CASO BASE: Es un archivo individual (hoja)
                total_archivos += 1

        return total_archivos

    # =========================================================================
    # MÉTODO AUXILIAR: Listar todos los archivos con su tamaño
    # =========================================================================
    @staticmethod
    def listar_archivos(
        sistema: Dict[str, Any], ruta_actual: str = ""
    ) -> List[Dict[str, str]]:
        """
        Recorre recursivamente el árbol y retorna una lista plana de diccionarios
        con la ruta completa y el tamaño de cada archivo.
        """
        if not isinstance(sistema, dict):
            return []

        archivos: List[Dict[str, str]] = []

        for clave, valor in sistema.items():
            ruta_elemento = f"{ruta_actual}/{clave}" if ruta_actual else clave

            if isinstance(valor, dict):
                # CASO RECURSIVO
                archivos.extend(ExploradorRecursivo.listar_archivos(valor, ruta_elemento))
            else:
                # CASO BASE
                archivos.append({"ruta": ruta_elemento, "tamano": str(valor)})

        return archivos


# =============================================================================
# Demostración y Ejecución Principal
# =============================================================================
if __name__ == "__main__":
    # Estructura de prueba del enunciado
    sistema_archivos_demo = {
        "Documentos": {
            "apuntes.txt": "10kb",
            "fotos": {
                "vacaciones.png": "2mb",
                "perro.jpg": "1mb",
            },
        },
        "sistema.dll": "500kb",
    }

    print("=" * 60)
    print("MINI-PROYECTO: EXPLORADOR DE DIRECTORIOS")
    print("=" * 60)

    print("\n1. Visualización del Árbol de Directorios:")
    ExploradorRecursivo.imprimir_arbol(sistema_archivos_demo)

    print("\n2. Conteo Total de Archivos:")
    total = ExploradorRecursivo.contar_archivos(sistema_archivos_demo)
    print(f"Total de archivos detectados (hojas): {total}")

    print("\n3. Búsqueda de Archivos:")
    pruebas_busqueda = ["vacaciones.png", "sistema.dll", "apuntes.txt", "inexistente.pdf"]
    for archivo in pruebas_busqueda:
        ruta = ExploradorRecursivo.buscar_archivo(sistema_archivos_demo, archivo)
        if ruta:
            print(f"  [OK] Archivo '{archivo}' encontrado en: {ruta}")
        else:
            print(f"  [X] Archivo '{archivo}' no encontrado en el sistema.")

    print("\n4. Lista Plana de Archivos y Tamaños:")
    for arch in ExploradorRecursivo.listar_archivos(sistema_archivos_demo):
        print(f"  - {arch['ruta']} -> {arch['tamano']}")
