"""
Interfaz Gráfica de Escritorio Moderna para el Sistema de Recomendación con Grafos.
Construida con CustomTkinter y Matplotlib. Permite interactuar visualmente con el grafo
bipartito, seleccionar usuarios, ver recomendaciones explicadas y añadir calificaciones.
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from graph import GrafoBipartitoRecomendador
from data import cargar_datos_demo
from visualizer import crear_figura_grafo


class ModalNuevaCalificacion(ctk.CTkToplevel):
    """Ventana modal para registrar un nuevo rating o nuevo usuario/película."""

    def __init__(self, parent, grafo: GrafoBipartitoRecomendador, al_guardar_callback):
        super().__init__(parent)
        self.grafo = grafo
        self.al_guardar_callback = al_guardar_callback

        self.title("Añadir Nueva Calificación")
        self.geometry("420x430")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # Contenedor
        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="➕ Registrar Conexión en el Grafo",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 15))

        # Campo Usuario
        ctk.CTkLabel(frame, text="Usuario (existente o nuevo):", anchor="w").pack(fill="x", padx=15)
        self.entry_usuario = ctk.CTkComboBox(
            frame,
            values=sorted(list(self.grafo.usuarios)),
            width=300
        )
        self.entry_usuario.pack(padx=15, pady=(2, 10))

        # Campo Película
        ctk.CTkLabel(frame, text="Película / Ítem (existente o nuevo):", anchor="w").pack(fill="x", padx=15)
        self.entry_item = ctk.CTkComboBox(
            frame,
            values=sorted(list(self.grafo.items)),
            width=300
        )
        self.entry_item.pack(padx=15, pady=(2, 10))

        # Slider Calificación
        ctk.CTkLabel(frame, text="Calificación (1.0 a 5.0 ★):", anchor="w").pack(fill="x", padx=15)
        self.label_rating_valor = ctk.CTkLabel(
            frame,
            text="5.0 ★",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F1C40F"
        )
        self.label_rating_valor.pack()

        self.slider_rating = ctk.CTkSlider(
            frame,
            from_=1.0,
            to=5.0,
            number_of_steps=8,
            command=self._actualizar_slider
        )
        self.slider_rating.set(5.0)
        self.slider_rating.pack(fill="x", padx=25, pady=(0, 20))

        # Botón Guardar
        btn_guardar = ctk.CTkButton(
            frame,
            text="Guardar en el Grafo",
            command=self._guardar,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            font=ctk.CTkFont(weight="bold")
        )
        btn_guardar.pack(fill="x", padx=25, pady=5)

    def _actualizar_slider(self, valor):
        self.label_rating_valor.configure(text=f"{valor:.1f} ★")

    def _guardar(self):
        u = self.entry_usuario.get().strip()
        it = self.entry_item.get().strip()
        r = float(self.slider_rating.get())

        if not u or not it:
            messagebox.showwarning("Atención", "Por favor completa tanto el usuario como la película.", parent=self)
            return

        try:
            self.grafo.agregar_calificacion(u, it, r)
            self.al_guardar_callback(u)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class AppRecomendadorGrafos(ctk.CTk):
    """Ventana principal de la aplicación con visualización de grafos."""

    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Sistema de Recomendación con Grafos Bipartitos - Python UI")
        self.geometry("1300x820")
        self.minsize(1050, 700)

        # Tema CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Cargar Grafo
        self.grafo = cargar_datos_demo()
        self.usuario_seleccionado = "Fernando"
        self.recomendaciones_actuales = []
        self.canvas_matplotlib = None
        self.figura_actual = None

        self._crear_interfaz()
        self._actualizar_analisis_usuario("Fernando")

    def _crear_interfaz(self):
        # Grid principal (columna 0: panel lateral, columna 1: visualizador del grafo)
        self.grid_columnconfigure(0, weight=0, minsize=380)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # PANEL LATERAL IZQUIERDO (Controles y Diagnóstico del Grafo)
        # =====================================================================
        self.panel_izquierdo = ctk.CTkFrame(self, corner_radius=0, width=380)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.panel_izquierdo.grid_rowconfigure(4, weight=1)

        # Encabezado
        lbl_titulo = ctk.CTkLabel(
            self.panel_izquierdo,
            text="🎬 Grafo Recomendador",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        lbl_titulo.pack(pady=(18, 2), padx=20, anchor="w")

        lbl_subtitulo = ctk.CTkLabel(
            self.panel_izquierdo,
            text="Filtrado Colaborativo y Grafos Bipartitos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        lbl_subtitulo.pack(pady=(0, 15), padx=20, anchor="w")

        # Selector de Usuario
        lbl_sel = ctk.CTkLabel(
            self.panel_izquierdo,
            text="Seleccionar Usuario Objetivo:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl_sel.pack(padx=20, anchor="w")

        self.combo_usuarios = ctk.CTkComboBox(
            self.panel_izquierdo,
            values=sorted(list(self.grafo.usuarios)),
            command=self._on_usuario_cambiado,
            width=340
        )
        self.combo_usuarios.set("Fernando")
        self.combo_usuarios.pack(padx=20, pady=(4, 12))

        # Botonera de Acciones
        frame_botones = ctk.CTkFrame(self.panel_izquierdo, fg_color="transparent")
        frame_botones.pack(fill="x", padx=20, pady=(0, 12))

        btn_nueva_calif = ctk.CTkButton(
            frame_botones,
            text="➕ Nueva Calificación",
            command=self._abrir_modal_calificacion,
            fg_color="#2980B9",
            hover_color="#1F618D",
            width=160
        )
        btn_nueva_calif.pack(side="left", padx=(0, 5))

        btn_ver_todo = ctk.CTkButton(
            frame_botones,
            text="🌐 Ver Completo",
            command=self._mostrar_grafo_completo,
            fg_color="#34495E",
            hover_color="#2C3E50",
            width=160
        )
        btn_ver_todo.pack(side="right", padx=(5, 0))

        # Tarjetas de Detalles (Scrollable Frame)
        self.scroll_info = ctk.CTkScrollableFrame(self.panel_izquierdo, corner_radius=8)
        self.scroll_info.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        # Tarjeta 1: Historial del Usuario
        self.lbl_card_historial = ctk.CTkLabel(
            self.scroll_info,
            text="Películas Vistas:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.lbl_card_historial.pack(fill="x", pady=(5, 2))

        self.txt_historial = ctk.CTkTextbox(self.scroll_info, height=90, font=ctk.CTkFont(size=11))
        self.txt_historial.pack(fill="x", pady=(0, 10))

        # Tarjeta 2: Vecinos Similares (Coseno)
        self.lbl_card_vecinos = ctk.CTkLabel(
            self.scroll_info,
            text="Vecinos Más Cercanos (Similitud Coseno):",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.lbl_card_vecinos.pack(fill="x", pady=(5, 2))

        self.txt_vecinos = ctk.CTkTextbox(self.scroll_info, height=75, font=ctk.CTkFont(size=11))
        self.txt_vecinos.pack(fill="x", pady=(0, 10))

        # Tarjeta 3: Recomendaciones y Caminos Explicativos
        self.lbl_card_recs = ctk.CTkLabel(
            self.scroll_info,
            text="Recomendaciones y Caminos (L=3):",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.lbl_card_recs.pack(fill="x", pady=(5, 2))

        self.txt_recs = ctk.CTkTextbox(self.scroll_info, height=140, font=ctk.CTkFont(size=11))
        self.txt_recs.pack(fill="x", pady=(0, 5))

        # Selector de Tema al pie del panel
        frame_tema = ctk.CTkFrame(self.panel_izquierdo, fg_color="transparent")
        frame_tema.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(frame_tema, text="Tema:", font=ctk.CTkFont(size=11)).pack(side="left")
        self.switch_tema = ctk.CTkSwitch(
            frame_tema,
            text="Modo Oscuro",
            command=self._cambiar_tema,
            onvalue=1,
            offvalue=0
        )
        self.switch_tema.select()
        self.switch_tema.pack(side="right")

        # =====================================================================
        # PANEL DERECHO: ÁREA DEL GRAFO MATPLOTLIB
        # =====================================================================
        self.panel_derecho = ctk.CTkFrame(self, corner_radius=12)
        self.panel_derecho.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.panel_derecho.grid_rowconfigure(1, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)

        # Barra superior del visor
        frame_toolbar_top = ctk.CTkFrame(self.panel_derecho, fg_color="transparent")
        frame_toolbar_top.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))

        self.lbl_status_grafo = ctk.CTkLabel(
            frame_toolbar_top,
            text="Visualización Interactiva del Grafo Bipartito",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_status_grafo.pack(side="left")

        btn_guardar_png = ctk.CTkButton(
            frame_toolbar_top,
            text="💾 Guardar PNG",
            command=self._guardar_imagen_grafo,
            width=120,
            fg_color="#8E44AD",
            hover_color="#7D3C98"
        )
        btn_guardar_png.pack(side="right")

        # Contenedor para el Canvas
        self.frame_canvas = ctk.CTkFrame(self.panel_derecho, fg_color="transparent")
        self.frame_canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    # =========================================================================
    # LÓGICA DE ACTUALIZACIÓN Y RENDERIZADO
    # =========================================================================

    def _on_usuario_cambiado(self, usuario):
        self._actualizar_analisis_usuario(usuario)

    def _actualizar_analisis_usuario(self, usuario):
        self.usuario_seleccionado = usuario
        self.lbl_status_grafo.configure(text=f"Visualización: Caminos de Recomendación para '{usuario}'")

        # 1. Historial de películas vistas
        vistas = self.grafo.obtener_items_usuario(usuario)
        self.txt_historial.delete("1.0", "end")
        for peli, r in sorted(vistas.items(), key=lambda x: x[1], reverse=True):
            self.txt_historial.insert("end", f"• {peli:<22} {r:.1f} ★\n")

        # 2. Vecinos Similares (Coseno en el Grafo)
        similares = self.grafo.obtener_usuarios_similares(usuario, k=3)
        self.txt_vecinos.delete("1.0", "end")
        if similares:
            for vec, sim in similares:
                self.txt_vecinos.insert("end", f"• {vec:<14} Similitud: {sim:.3f} ({sim*100:.1f}%)\n")
        else:
            self.txt_vecinos.insert("end", "Sin vecinos con películas en común.")

        # 3. Recomendaciones y Caminos
        recs = self.grafo.recomendar_items(usuario, k_vecinos=3, top_n=3)
        self.recomendaciones_actuales = recs

        self.txt_recs.delete("1.0", "end")
        if recs:
            for idx, r in enumerate(recs, 1):
                self.txt_recs.insert("end", f"{idx}. ★ {r['item']} (Score: {r['score_estimado']}★)\n")
                for c in r.get("caminos_grafo", [])[:2]:
                    _, peli_c, vecino, _ = c
                    self.txt_recs.insert("end", f"   ↳ {usuario} -> {peli_c} -> {vecino} -> {r['item']}\n")
                self.txt_recs.insert("end", "\n")
        else:
            self.txt_recs.insert("end", "No hay películas nuevas sugeridas.")

        # 4. Redibujar Canvas Matplotlib
        self._renderizar_canvas(usuario_objetivo=usuario, recomendaciones=recs)

    def _mostrar_grafo_completo(self):
        self.usuario_seleccionado = None
        self.recomendaciones_actuales = []
        self.lbl_status_grafo.configure(text="Visualización: Grafo Bipartito Completo (Todas las conexiones)")
        self._renderizar_canvas(usuario_objetivo=None, recomendaciones=None)

    def _renderizar_canvas(self, usuario_objetivo=None, recomendaciones=None):
        """Renderiza la figura de Matplotlib embebida directamente en el Frame de Tkinter."""
        es_oscuro = (ctk.get_appearance_mode() == "Dark")

        # Limpiar canvas previo si existe
        if self.canvas_matplotlib is not None:
            self.canvas_matplotlib.get_tk_widget().destroy()

        self.figura_actual = crear_figura_grafo(
            grafo=self.grafo,
            usuario_objetivo=usuario_objetivo,
            recomendaciones=recomendaciones,
            figsize=(9.5, 6.5),
            dpi=110,
            modo_oscuro=es_oscuro
        )

        self.canvas_matplotlib = FigureCanvasTkAgg(self.figura_actual, master=self.frame_canvas)
        self.canvas_matplotlib.draw()
        self.canvas_matplotlib.get_tk_widget().pack(fill="both", expand=True)

    def _cambiar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

        # Redibujar con el nuevo esquema de color
        self._renderizar_canvas(
            usuario_objetivo=self.usuario_seleccionado,
            recomendaciones=self.recomendaciones_actuales
        )

    def _abrir_modal_calificacion(self):
        def al_guardar(usuario_afectado):
            # Actualizar dropdown de usuarios
            self.combo_usuarios.configure(values=sorted(list(self.grafo.usuarios)))
            self.combo_usuarios.set(usuario_afectado)
            self._actualizar_analisis_usuario(usuario_afectado)

        ModalNuevaCalificacion(self, self.grafo, al_guardar)

    def _guardar_imagen_grafo(self):
        if not self.figura_actual:
            return

        nombre_defecto = f"grafo_{self.usuario_seleccionado or 'completo'}.png"
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png"), ("Todos los archivos", "*.*")],
            initialfile=nombre_defecto
        )
        if ruta:
            self.figura_actual.savefig(ruta, bbox_inches="tight", facecolor=self.figura_actual.get_facecolor())
            messagebox.showinfo("Guardado", f"El gráfico se guardó exitosamente en:\n{ruta}")


if __name__ == "__main__":
    app = AppRecomendadorGrafos()
    app.mainloop()
