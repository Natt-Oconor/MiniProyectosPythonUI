"""
Módulo de Datos Iniciales para el Grafo de Recomendación de Películas.
Provee un catálogo con categorías temáticas (Ciencia Ficción, Crimen/Drama, Animación)
y perfiles de usuarios con intereses definidos para ilustrar los grafos bipartitos.
"""

from graph import GrafoBipartitoRecomendador


def cargar_datos_demo() -> GrafoBipartitoRecomendador:
    """
    Construye y puebla un grafo bipartito con usuarios y películas de ejemplo.
    """
    grafo = GrafoBipartitoRecomendador()

    # Catálogo de Películas (Nodos Ítems)
    peliculas = [
        # Ciencia Ficción
        "The Matrix",
        "Interstellar",
        "Inception",
        
        # Crimen & Acción
        "Pulp Fiction",
        "El Padrino",
        "El Caballero de la Noche",
        
        # Animación & Fantasía
        "Toy Story",
        "Coco",
        "El Viaje de Chihiro"
    ]

    for peli in peliculas:
        grafo.agregar_item(peli)

    # Calificaciones por Usuario (Aristas ponderadas)
    calificaciones = {
        # Alicia: Muy fan de Ciencia Ficción
        "Alicia": {
            "The Matrix": 5.0,
            "Inception": 4.8,
            "Interstellar": 5.0
        },
        # Bob: Conexión entre Sci-Fi y Crimen
        "Bob": {
            "The Matrix": 4.5,
            "Interstellar": 4.0,
            "Pulp Fiction": 5.0,
            "El Caballero de la Noche": 4.8
        },
        # Carlos: Fan de Crimen y Clásicos
        "Carlos": {
            "Pulp Fiction": 4.5,
            "El Padrino": 5.0,
            "El Caballero de la Noche": 4.2
        },
        # Diana: Fan de Animación y Fantasía
        "Diana": {
            "Toy Story": 5.0,
            "Coco": 4.8,
            "El Viaje de Chihiro": 5.0
        },
        # Elena: Gustos mixtos (conecta Animación con Sci-Fi)
        "Elena": {
            "Coco": 4.5,
            "Toy Story": 4.0,
            "Inception": 4.2
        },
        # Fernando: Usuario ideal para pedir recomendaciones de Sci-Fi
        "Fernando": {
            "The Matrix": 5.0,
            "Interstellar": 4.5
        },
        # Sofía: Usuaria que vio solo una de animación
        "Sofía": {
            "Coco": 5.0
        }
    }

    for usuario, ratings in calificaciones.items():
        grafo.agregar_usuario(usuario)
        for peli, rating in ratings.items():
            grafo.agregar_calificacion(usuario, peli, rating)

    return grafo
