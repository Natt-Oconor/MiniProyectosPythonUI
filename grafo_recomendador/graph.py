"""
Módulo de Estructura de Datos de Grafo Bipartito para Recomendaciones.
Implementa desde cero la representación del grafo mediante listas de adyacencia
y algoritmos de recomendación basados en similitud de nodos y caminos en el grafo.
"""

from __future__ import annotations
import math
from typing import Dict, List, Set, Tuple, Optional


class GrafoBipartitoRecomendador:
    """
    Grafo Bipartito G = (U, V, E)
    donde:
      - U es el conjunto de nodos de Usuarios.
      - V es el conjunto de nodos de Ítems (películas, libros, etc.).
      - E es el conjunto de aristas ponderadas (calificación o rating de U en V).
      
    Propiedad Bipartita: Una arista solo puede conectar un nodo de U con un nodo de V.
    No existen aristas entre nodos del mismo conjunto (U-U ni V-V).
    """

    def __init__(self):
        # Conjuntos disjuntos de nodos
        self.usuarios: Set[str] = set()
        self.items: Set[str] = set()
        
        # Lista de adyacencia ponderada:
        # self.adj[nodo] = {vecino: peso_rating}
        self.adj: Dict[str, Dict[str, float]] = {}

    def agregar_usuario(self, nombre_usuario: str) -> None:
        """Registra un nuevo nodo de usuario en el grafo."""
        nombre_usuario = nombre_usuario.strip()
        if not nombre_usuario:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if nombre_usuario in self.items:
            raise ValueError(f"Conflicto de nombres: '{nombre_usuario}' ya está registrado como ítem.")
        if nombre_usuario not in self.usuarios:
            self.usuarios.add(nombre_usuario)
            self.adj[nombre_usuario] = {}

    def agregar_item(self, nombre_item: str) -> None:
        """Registra un nuevo nodo de ítem (película) en el grafo."""
        nombre_item = nombre_item.strip()
        if not nombre_item:
            raise ValueError("El nombre del ítem no puede estar vacío.")
        if nombre_item in self.usuarios:
            raise ValueError(f"Conflicto de nombres: '{nombre_item}' ya está registrado como usuario.")
        if nombre_item not in self.items:
            self.items.add(nombre_item)
            self.adj[nombre_item] = {}

    def agregar_calificacion(self, usuario: str, item: str, rating: float) -> None:
        """
        Crea una arista no dirigida ponderada entre un usuario y un ítem.
        Valida que el grafo preserve su propiedad bipartita.
        """
        if usuario not in self.usuarios:
            self.agregar_usuario(usuario)
        if item not in self.items:
            self.agregar_item(item)
            
        if not (1.0 <= rating <= 5.0):
            raise ValueError("La calificación debe estar entre 1.0 y 5.0.")

        # Conexión bidireccional en la lista de adyacencia
        self.adj[usuario][item] = float(rating)
        self.adj[item][usuario] = float(rating)

    def obtener_items_usuario(self, usuario: str) -> Dict[str, float]:
        """Retorna el diccionario de {item: rating} calificados por el usuario."""
        if usuario not in self.usuarios:
            raise KeyError(f"El usuario '{usuario}' no existe en el grafo.")
        return dict(self.adj[usuario])

    def obtener_usuarios_item(self, item: str) -> Dict[str, float]:
        """Retorna el diccionario de {usuario: rating} que calificaron el ítem."""
        if item not in self.items:
            raise KeyError(f"El ítem '{item}' no existe en el grafo.")
        return dict(self.adj[item])

    def grado_nodo(self, nodo: str) -> int:
        """Grado del nodo: cantidad de vecinos directos conectados."""
        return len(self.adj.get(nodo, {}))

    # =========================================================================
    # ALGORITMOS DE GRAFOS: SIMILITUD ENTRE USUARIOS (Proyección Bipartita)
    # =========================================================================

    def similitud_jaccard(self, u1: str, u2: str) -> float:
        """
        Coeficiente de Jaccard entre dos usuarios basado en la intersección de vecinos:
        J(u1, u2) = |Vecinos(u1) ∩ Vecinos(u2)| / |Vecinos(u1) ∪ Vecinos(u2)|
        """
        if u1 not in self.usuarios or u2 not in self.usuarios:
            return 0.0
        if u1 == u2:
            return 1.0

        items_u1 = set(self.adj[u1].keys())
        items_u2 = set(self.adj[u2].keys())

        union = items_u1 | items_u2
        if not union:
            return 0.0

        interseccion = items_u1 & items_u2
        return len(interseccion) / len(union)

    def similitud_coseno(self, u1: str, u2: str) -> float:
        """
        Similitud Coseno de Pearson/Vectorial tomando en cuenta los pesos (ratings):
        cos(u1, u2) = (v_1 · v_2) / (||v_1|| * ||v_2||)
        sobre las películas en común.
        """
        if u1 not in self.usuarios or u2 not in self.usuarios:
            return 0.0
        if u1 == u2:
            return 1.0

        ratings_1 = self.adj[u1]
        ratings_2 = self.adj[u2]

        items_comunes = set(ratings_1.keys()) & set(ratings_2.keys())
        if not items_comunes:
            return 0.0

        # Producto punto
        dot_product = sum(ratings_1[it] * ratings_2[it] for it in items_comunes)
        
        # Normas euclidianas de los vectores
        norm_1 = math.sqrt(sum(r ** 2 for r in ratings_1.values()))
        norm_2 = math.sqrt(sum(r ** 2 for r in ratings_2.values()))

        if norm_1 == 0 or norm_2 == 0:
            return 0.0

        return dot_product / (norm_1 * norm_2)

    def obtener_usuarios_similares(
        self, usuario: str, k: int = 3, metodo: str = "coseno"
    ) -> List[Tuple[str, float]]:
        """
        Encuentra los 'k' usuarios más similares a un usuario objetivo.
        Retorna [(otro_usuario, score_similitud), ...] ordenados de mayor a menor.
        """
        if usuario not in self.usuarios:
            raise KeyError(f"El usuario '{usuario}' no existe.")

        fn_sim = self.similitud_coseno if metodo == "coseno" else self.similitud_jaccard
        similares = []

        for otro in self.usuarios:
            if otro == usuario:
                continue
            sim = fn_sim(usuario, otro)
            if sim > 0:
                similares.append((otro, sim))

        # Ordenar por similitud descendente
        similares.sort(key=lambda x: x[1], reverse=True)
        return similares[:k]

    # =========================================================================
    # SISTEMA DE RECOMENDACIÓN BASADO EN CAMINOS Y VECINOS
    # =========================================================================

    def recomendar_items(
        self,
        usuario: str,
        k_vecinos: int = 3,
        top_n: int = 3,
        metodo_sim: str = "coseno"
    ) -> List[Dict]:
        """
        Genera recomendaciones para el usuario mediante filtrado colaborativo basado en grafos.
        Calcula un rating predicho ponderado por la similitud de los vecinos:
        
        score(item) = sum(sim(u, v) * rating(v, item)) / sum(sim(u, v))
        
        Retorna una lista de diccionarios con el ítem, score estimado, y la explicación de los caminos.
        """
        if usuario not in self.usuarios:
            raise KeyError(f"Usuario '{usuario}' no registrado.")

        items_vistos = set(self.adj[usuario].keys())
        vecinos_similares = self.obtener_usuarios_similares(usuario, k=k_vecinos, metodo=metodo_sim)

        if not vecinos_similares:
            return []

        # Acumuladores de predicción para ítems candidatos
        puntajes_acumulados: Dict[str, float] = {}
        pesos_acumulados: Dict[str, float] = {}
        quienes_recomiendan: Dict[str, List[Tuple[str, float, float]]] = {}

        for vecino, sim in vecinos_similares:
            for item, rating in self.adj[vecino].items():
                if item not in items_vistos:
                    puntajes_acumulados[item] = puntajes_acumulados.get(item, 0.0) + (sim * rating)
                    pesos_acumulados[item] = pesos_acumulados.get(item, 0.0) + sim
                    if item not in quienes_recomiendan:
                        quienes_recomiendan[item] = []
                    quienes_recomiendan[item].append((vecino, sim, rating))

        recomendaciones = []
        for item, puntaje_total in puntajes_acumulados.items():
            peso_total = pesos_acumulados[item]
            score_predicho = puntaje_total / peso_total if peso_total > 0 else 0.0
            
            # Buscar caminos explicativos de longitud 3:
            # Usuario -> Item_En_Comun -> Vecino -> Item_Recomendado
            caminos = self.encontrar_caminos_explicacion(usuario, item, quienes_recomiendan[item])

            recomendaciones.append({
                "item": item,
                "score_estimado": round(score_predicho, 2),
                "recomendado_por": quienes_recomiendan[item],
                "caminos_grafo": caminos
            })

        # Ordenar por el score estimado de forma descendente
        recomendaciones.sort(key=lambda x: x["score_estimado"], reverse=True)
        return recomendaciones[:top_n]

    def encontrar_caminos_explicacion(
        self, usuario: str, item_objetivo: str, recomendadores: List[Tuple[str, float, float]]
    ) -> List[Tuple[str, str, str, str]]:
        """
        Encuentra caminos de longitud 3 en el grafo bipartito que justifican la recomendación:
        (Usuario -> Película_Común -> Vecino -> Ítem_Recomendado)
        """
        caminos = []
        items_usuario = set(self.adj[usuario].keys())

        for vecino, _, _ in recomendadores:
            items_vecino = set(self.adj[vecino].keys())
            comunes = items_usuario & items_vecino
            for com in comunes:
                caminos.append((usuario, com, vecino, item_objetivo))

        return caminos

    # =========================================================================
    # EXPORTACIÓN A NETWORKX PARA ANÁLISIS Y DIBUJO
    # =========================================================================

    def exportar_networkx(self):
        """
        Convierte el grafo propio a una instancia de networkx.Graph
        con metadatos de bipartición (bipartite: 0 para usuarios, 1 para items).
        """
        import networkx as nx

        G = nx.Graph()

        for u in self.usuarios:
            G.add_node(u, tipo="usuario", bipartite=0)

        for it in self.items:
            G.add_node(it, tipo="item", bipartite=1)

        for u in self.usuarios:
            for it, rating in self.adj[u].items():
                G.add_edge(u, it, weight=rating)

        return G
