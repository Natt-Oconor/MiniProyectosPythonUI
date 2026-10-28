"""
Programa Principal del Sistema de Recomendación con Grafos Bipartitos.
Provee una interfaz de consola interactiva y un modo demostración guiado.
"""

import sys
import os
from data import cargar_datos_demo
from visualizer import dibujar_grafo_recomendador


def mostrar_encabezado():
    print("=" * 65)
    print("      SISTEMA DE RECOMENDACIÓN BASADO EN GRAFOS BIPARTITOS      ")
    print("=" * 65)


def mostrar_resumen_grafo(grafo):
    print("\n--- RESUMEN DE LA ESTRUCTURA DEL GRAFO ---")
    print(f"• Total de Nodos de Usuarios (Conjunto U): {len(grafo.usuarios)}")
    print(f"  {', '.join(sorted(grafo.usuarios))}")
    print(f"• Total de Nodos de Películas (Conjunto V): {len(grafo.items)}")
    print(f"  {', '.join(sorted(grafo.items))}")
    
    total_aristas = sum(len(ratings) for ratings in grafo.adj.values()) // 2
    max_posibles_aristas = len(grafo.usuarios) * len(grafo.items)
    densidad = (total_aristas / max_posibles_aristas) if max_posibles_aristas > 0 else 0
    
    print(f"• Aristas (Calificaciones U ↔ V): {total_aristas}")
    print(f"• Densidad de la red bipartita: {densidad:.2%}")
    print("-" * 45)


def consultar_perfil_usuario(grafo):
    print("\nUsuarios disponibles:", ", ".join(sorted(grafo.usuarios)))
    nombre = input("Ingresa el nombre del usuario: ").strip()
    if nombre not in grafo.usuarios:
        print(f"El usuario '{nombre}' no existe.")
        return

    ratings = grafo.obtener_items_usuario(nombre)
    print(f"\nHistorial de calificaciones de [{nombre}] ({len(ratings)} películas):")
    for item, r in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        estrellas = "★" * int(r) + ("½" if r % 1 >= 0.5 else "")
        print(f"  - {item:<28} | {r:.1f} {estrellas}")


def consultar_recomendaciones(grafo):
    print("\nUsuarios disponibles:", ", ".join(sorted(grafo.usuarios)))
    nombre = input("¿Para qué usuario deseas generar recomendaciones?: ").strip()
    if nombre not in grafo.usuarios:
        print(f"El usuario '{nombre}' no existe.")
        return

    print("\nCalculando similitudes vectoriales (Coseno en el grafo)...")
    similares = grafo.obtener_usuarios_similares(nombre, k=3)
    if not similares:
        print(f"No hay usuarios con películas en común suficientes para comparar con {nombre}.")
        return

    print("\nVecinos más afines en la red:")
    for vecino, sim in similares:
        print(f"  • {vecino:<12} (Similitud: {sim:.3f} | {sim*100:.1f}%)")

    recomendaciones = grafo.recomendar_items(nombre, k_vecinos=3, top_n=3)

    if not recomendaciones:
        print(f"\nNo se encontraron recomendaciones nuevas (el usuario ya vio todo o no hay vecinos afines).")
        return

    print(f"\n{'='*20} RECOMENDACIONES PARA {nombre.upper()} {'='*20}")
    for idx, rec in enumerate(recomendaciones, 1):
        item = rec["item"]
        score = rec["score_estimado"]
        print(f"\n{idx}. {item} (Rating proyectado: {score:.2f}★)")
        
        # Explicación de caminos
        caminos = rec["caminos_grafo"]
        if caminos:
            print("   Razón (Caminos de longitud 3 en el grafo):")
            for c in caminos[:2]:
                _, peli_comun, vecino, _ = c
                print(f"     * Te gustó '{peli_comun}' ↔ a '{vecino}' también ↔ '{vecino}' calificó '{item}'")

    opcion_graficar = input("\n¿Deseas generar el gráfico visual con estas recomendaciones? (s/n): ").strip().lower()
    if opcion_graficar in ["s", "si", "y", "yes"]:
        archivo_png = f"recomendacion_{nombre}.png"
        ruta = dibujar_grafo_recomendador(
            grafo,
            usuario_objetivo=nombre,
            recomendaciones=recomendaciones,
            ruta_salida=archivo_png
        )
        print(f"Gráfico generado exitosamente en: {ruta}")


def registrar_nuevo_rating(grafo):
    print("\n--- REGISTRAR NUEVA CALIFICACIÓN ---")
    usuario = input("Nombre del usuario (existente o nuevo): ").strip()
    if not usuario:
        return

    print("Películas en catálogo:", ", ".join(sorted(grafo.items)))
    pelicula = input("Nombre de la película (existente o nueva): ").strip()
    if not pelicula:
        return

    try:
        calificacion = float(input("Calificación (1.0 a 5.0): ").strip())
        grafo.agregar_calificacion(usuario, pelicula, calificacion)
        print(f"¡Calificación guardada: {usuario} calificó '{pelicula}' con {calificacion:.1f}★!")
    except ValueError as e:
        print(f"Error: {e}")


def exportar_grafico_general(grafo):
    archivo_png = "grafo_completo.png"
    ruta = dibujar_grafo_recomendador(
        grafo,
        ruta_salida=archivo_png
    )
    print(f"\nGrafo completo exportado a imagen: {ruta}")


def ejecutar_demostracion_guiada(grafo):
    """Ejecuta un recorrido didáctico automático paso a paso."""
    print("\n" + "=" * 65)
    print("          DEMOSTRACIÓN DIDÁCTICA GUIADA")
    print("=" * 65)
    print("1. Analizaremos al usuario de prueba: 'Fernando'")
    vistas = grafo.obtener_items_usuario("Fernando")
    print(f"   Películas vistas por Fernando: {vistas}")

    print("\n2. Identificamos sus vecinos más cercanos en el grafo:")
    similares = grafo.obtener_usuarios_similares("Fernando", k=3)
    for vecino, sim in similares:
        print(f"   - {vecino}: similitud = {sim:.3f}")

    print("\n3. Calculamos recomendaciones proyectadas:")
    recs = grafo.recomendar_items("Fernando", k_vecinos=3, top_n=2)
    for r in recs:
        print(f"   -> Sugerencia: {r['item']} (Score estimado: {r['score_estimado']})")
        for c in r["caminos_grafo"]:
            print(f"      Explicación: Fernando -> {c[1]} -> {c[2]} -> {c[3]}")

    print("\n4. Generando visualización gráfica de alta resolución...")
    ruta = dibujar_grafo_recomendador(
        grafo,
        usuario_objetivo="Fernando",
        recomendaciones=recs,
        ruta_salida="demo_fernando_recomendaciones.png"
    )
    print(f"   ¡Listo! Imagen generada en: {ruta}")
    print("=" * 65 + "\n")


def menu():
    grafo = cargar_datos_demo()

    # Si se pasa argumento --demo desde consola, se ejecuta la demo directamente
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        ejecutar_demostracion_guiada(grafo)
        return

    while True:
        mostrar_encabezado()
        print("1. Ver catálogo y métricas del grafo bipartito")
        print("2. Ver historial de un usuario")
        print("3. Pedir recomendaciones de películas para un usuario")
        print("4. Agregar usuario o nueva calificación (nueva arista)")
        print("5. Exportar imagen del grafo completo (PNG)")
        print("6. Ejecutar Demostración Didáctica Guiada")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción [0-6]: ").strip()

        if opcion == "1":
            mostrar_resumen_grafo(grafo)
        elif opcion == "2":
            consultar_perfil_usuario(grafo)
        elif opcion == "3":
            consultar_recomendaciones(grafo)
        elif opcion == "4":
            registrar_nuevo_rating(grafo)
        elif opcion == "5":
            exportar_grafico_general(grafo)
        elif opcion == "6":
            ejecutar_demostracion_guiada(grafo)
        elif opcion == "0":
            print("\n¡Gracias por usar el Recomendador de Grafos Bipartitos! Hasta pronto.")
            break
        else:
            print("\nOpción inválida. Intenta nuevamente.")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    menu()
