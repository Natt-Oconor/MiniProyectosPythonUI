"""
Módulo de Visualización Gráfica para el Grafo Bipartito de Recomendaciones.
Utiliza NetworkX para el modelado y Matplotlib para renderizar
estéticamente los nodos bipartitos, aristas ponderadas y caminos de recomendación.
"""

from typing import List, Optional
import os
import matplotlib.pyplot as plt
import networkx as nx

from graph import GrafoBipartitoRecomendador


def dibujar_grafo_recomendador(
    grafo: GrafoBipartitoRecomendador,
    usuario_objetivo: Optional[str] = None,
    recomendaciones: Optional[List[dict]] = None,
    ruta_salida: str = "grafo_recomendaciones.png",
    mostrar_interactivo: bool = False
) -> str:
    """
    Dibuja el grafo bipartito organizado en dos columnas:
    - Izquierda (x=0): Nodos de Usuarios (con etiquetas a la izquierda)
    - Derecha (x=1.6): Nodos de Películas (con etiquetas a la derecha)
    
    Resalta al usuario objetivo, películas recomendadas y caminos explicativos.
    """
    G = grafo.exportar_networkx()

    fig, ax = plt.subplots(figsize=(15, 9), dpi=200)
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    titulo = "Sistema de Recomendación - Grafo Bipartito"
    if usuario_objetivo:
        titulo += f" (Caminos de Recomendación para: {usuario_objetivo})"
    ax.set_title(titulo, fontsize=16, fontweight="bold", pad=25, color="#2C3E50")

    usuarios = sorted(list(grafo.usuarios))
    items = sorted(list(grafo.items))

    pos = {}
    pos_labels_u = {}
    pos_labels_i = {}

    # Columna Izquierda: Usuarios
    n_u = len(usuarios)
    for idx, u in enumerate(usuarios):
        y = (n_u - 1 - idx) / max(1, n_u - 1) if n_u > 1 else 0.5
        pos[u] = (0.0, y)
        pos_labels_u[u] = (-0.06, y)

    # Columna Derecha: Películas
    n_i = len(items)
    for idx, it in enumerate(items):
        y = (n_i - 1 - idx) / max(1, n_i - 1) if n_i > 1 else 0.5
        pos[it] = (1.6, y)
        pos_labels_i[it] = (1.66, y)

    # Identificar ítems recomendados y caminos explicativos
    items_rec_set = set()
    aristas_camino = set()

    if usuario_objetivo and recomendaciones:
        for rec in recomendaciones:
            item_rec = rec["item"]
            items_rec_set.add(item_rec)
            for camino in rec.get("caminos_grafo", []):
                u_obj, it_com, vec, it_final = camino
                aristas_camino.add((u_obj, it_com))
                aristas_camino.add((it_com, u_obj))
                aristas_camino.add((it_com, vec))
                aristas_camino.add((vec, it_com))
                aristas_camino.add((vec, it_final))
                aristas_camino.add((it_final, vec))

    # 1. Aristas Normales (Fondo)
    aristas_normales = [e for e in G.edges() if e not in aristas_camino]
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edgelist=aristas_normales,
        width=1.0,
        alpha=0.18,
        edge_color="#7F8C8D"
    )

    # 2. Aristas de Caminos Destacados
    aristas_destacadas = [e for e in G.edges() if e in aristas_camino]
    if aristas_destacadas:
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=aristas_destacadas,
            width=3.2,
            alpha=0.88,
            edge_color="#E74C3C"
        )

    # 3. Nodos de Usuarios Normales
    nodos_u_normales = [u for u in usuarios if u != usuario_objetivo]
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        nodelist=nodos_u_normales,
        node_color="#3498DB",
        node_size=800,
        node_shape="o",
        label="Otros Usuarios"
    )

    # Usuario Objetivo
    if usuario_objetivo and usuario_objetivo in G:
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            nodelist=[usuario_objetivo],
            node_color="#8E44AD",
            node_size=1200,
            node_shape="o",
            edgecolors="#2C3E50",
            linewidths=2.5,
            label=f"Usuario Objetivo ({usuario_objetivo})"
        )

    # 4. Nodos de Películas Normales
    items_normales = [it for it in items if it not in items_rec_set]
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        nodelist=items_normales,
        node_color="#2ECC71",
        node_size=800,
        node_shape="s",
        label="Películas en Catálogo"
    )

    # Películas Recomendadas
    if items_rec_set:
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            nodelist=list(items_rec_set),
            node_color="#F39C12",
            node_size=1200,
            node_shape="s",
            edgecolors="#D35400",
            linewidths=2.5,
            label="Películas Recomendadas ★"
        )

    # 5. Etiquetas de Texto ordenadas (fuera de los nodos para máxima legibilidad)
    for u in usuarios:
        font_weight = "bold" if u == usuario_objetivo else "normal"
        color = "#6C3483" if u == usuario_objetivo else "#2C3E50"
        x, y = pos_labels_u[u]
        ax.text(
            x, y, u,
            ha="right", va="center",
            fontsize=10, fontweight=font_weight, color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#D5D8DC", alpha=0.9)
        )

    for it in items:
        es_rec = it in items_rec_set
        font_weight = "bold" if es_rec else "normal"
        color = "#B7950B" if es_rec else "#2C3E50"
        x, y = pos_labels_i[it]
        prefijo = "★ " if es_rec else ""
        ax.text(
            x, y, f"{prefijo}{it}",
            ha="left", va="center",
            fontsize=10, fontweight=font_weight, color=color,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="#FEF9E7" if es_rec else "white",
                edgecolor="#F39C12" if es_rec else "#D5D8DC",
                alpha=0.95
            )
        )

    # 6. Etiquetas de Ratings en las aristas destacadas
    if aristas_destacadas:
        edge_labels = {
            (u, v): f"{G[u][v]['weight']}★"
            for u, v in aristas_destacadas
        }
        nx.draw_networkx_edge_labels(
            G,
            pos,
            ax=ax,
            edge_labels=edge_labels,
            font_size=8,
            font_color="#900C3F",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="#FDEDEC", edgecolor="#F5B7B1", alpha=0.95)
        )

    # Ajustar límites de los ejes para dar margen al texto exterior
    ax.set_xlim(-0.55, 2.3)
    ax.set_ylim(-0.1, 1.1)
    ax.axis("off")

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=4,
        frameon=True,
        facecolor="white",
        edgecolor="#D5D8DC",
        fontsize=9
    )

    plt.tight_layout()

    ruta_absoluta = os.path.abspath(ruta_salida)
    plt.savefig(ruta_absoluta, bbox_inches="tight", facecolor=fig.get_facecolor())
    
    if mostrar_interactivo:
        try:
            plt.show()
        except Exception:
            pass

    plt.close(fig)
    return ruta_absoluta
