"""
Módulo de Visualización Gráfica para el Grafo Bipartito de Recomendaciones.
Utiliza NetworkX para el modelado y Matplotlib para renderizar
estéticamente los nodos bipartitos, aristas ponderadas y caminos de recomendación.
Compatible con exportación de archivos PNG y embedding en interfaces gráficas (Tkinter/CustomTkinter).
"""

from typing import List, Optional
import os
import matplotlib.pyplot as plt
import networkx as nx

from graph import GrafoBipartitoRecomendador


def crear_figura_grafo(
    grafo: GrafoBipartitoRecomendador,
    usuario_objetivo: Optional[str] = None,
    recomendaciones: Optional[List[dict]] = None,
    figsize=(11, 7),
    dpi=100,
    modo_oscuro: bool = False
) -> plt.Figure:
    """
    Crea y retorna un objeto matplotlib.figure.Figure con el grafo bipartito renderizado.
    Soporta modo claro y oscuro, ideal para embeber en CustomTkinter.
    """
    G = grafo.exportar_networkx()

    bg_color = "#1E1E2E" if modo_oscuro else "#FAFAFA"
    text_color = "#CDD6F4" if modo_oscuro else "#2C3E50"
    box_bg = "#313244" if modo_oscuro else "#FFFFFF"
    box_edge = "#45475A" if modo_oscuro else "#D5D8DC"

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    titulo = "Grafo Bipartito de Calificaciones"
    if usuario_objetivo:
        titulo += f" - Caminos de {usuario_objetivo}"
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=20, color=text_color)

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
        alpha=0.15 if not modo_oscuro else 0.22,
        edge_color="#A6ADC8" if modo_oscuro else "#7F8C8D"
    )

    # 2. Aristas de Caminos Destacados
    aristas_destacadas = [e for e in G.edges() if e in aristas_camino]
    if aristas_destacadas:
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=aristas_destacadas,
            width=3.0,
            alpha=0.9,
            edge_color="#F38BA8" if modo_oscuro else "#E74C3C"
        )

    # 3. Nodos de Usuarios Normales
    nodos_u_normales = [u for u in usuarios if u != usuario_objetivo]
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        nodelist=nodos_u_normales,
        node_color="#89B4FA" if modo_oscuro else "#3498DB",
        node_size=650,
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
            node_color="#CBA6F7" if modo_oscuro else "#8E44AD",
            node_size=1000,
            node_shape="o",
            edgecolors="#B4BEFE" if modo_oscuro else "#2C3E50",
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
        node_color="#A6E3A1" if modo_oscuro else "#2ECC71",
        node_size=650,
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
            node_color="#F9E2AF" if modo_oscuro else "#F39C12",
            node_size=1000,
            node_shape="s",
            edgecolors="#FAB387" if modo_oscuro else "#D35400",
            linewidths=2.5,
            label="Películas Recomendadas ★"
        )

    # 5. Etiquetas de Texto ordenadas fuera de los nodos
    for u in usuarios:
        font_weight = "bold" if u == usuario_objetivo else "normal"
        color = ("#CBA6F7" if modo_oscuro else "#6C3483") if u == usuario_objetivo else text_color
        x, y = pos_labels_u[u]
        ax.text(
            x, y, u,
            ha="right", va="center",
            fontsize=9, fontweight=font_weight, color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=box_bg, edgecolor=box_edge, alpha=0.95)
        )

    for it in items:
        es_rec = it in items_rec_set
        font_weight = "bold" if es_rec else "normal"
        color = ("#F9E2AF" if modo_oscuro else "#B7950B") if es_rec else text_color
        x, y = pos_labels_i[it]
        prefijo = "★ " if es_rec else ""
        ax.text(
            x, y, f"{prefijo}{it}",
            ha="left", va="center",
            fontsize=9, fontweight=font_weight, color=color,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="#45475A" if (modo_oscuro and es_rec) else ("#FEF9E7" if es_rec else box_bg),
                edgecolor=("#FAB387" if modo_oscuro else "#F39C12") if es_rec else box_edge,
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
            font_color="#F38BA8" if modo_oscuro else "#900C3F",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="#313244" if modo_oscuro else "#FDEDEC",
                edgecolor="#F38BA8" if modo_oscuro else "#F5B7B1",
                alpha=0.95
            )
        )

    ax.set_xlim(-0.55, 2.3)
    ax.set_ylim(-0.1, 1.1)
    ax.axis("off")

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=4,
        frameon=True,
        facecolor=box_bg,
        edgecolor=box_edge,
        labelcolor=text_color,
        fontsize=8
    )

    plt.tight_layout()
    return fig


def dibujar_grafo_recomendador(
    grafo: GrafoBipartitoRecomendador,
    usuario_objetivo: Optional[str] = None,
    recomendaciones: Optional[List[dict]] = None,
    ruta_salida: str = "grafo_recomendaciones.png",
    mostrar_interactivo: bool = False
) -> str:
    """Exporta el grafo a una imagen PNG y opcionalmente lo muestra."""
    fig = crear_figura_grafo(
        grafo=grafo,
        usuario_objetivo=usuario_objetivo,
        recomendaciones=recomendaciones,
        figsize=(15, 9),
        dpi=200,
        modo_oscuro=False
    )

    ruta_absoluta = os.path.abspath(ruta_salida)
    fig.savefig(ruta_absoluta, bbox_inches="tight", facecolor=fig.get_facecolor())
    
    if mostrar_interactivo:
        try:
            plt.show()
        except Exception:
            pass

    plt.close(fig)
    return ruta_absoluta
