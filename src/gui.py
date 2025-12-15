import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
import csv
import sys, os
import time
import os
import gps

class StartScreen(tk.Frame):
    def __init__(self, parent, app, handlers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.handlers = handlers

        # Colores base
        BG_MAIN   = "#f5f7fb"   # gris muy claro
        CARD_BG   = "#ffffff"   # blanco
        TEXT_DARK = "#111827"   # casi negro
        TEXT_MUTED = "#6b7280"  # gris texto secundario
        ACCENT    = "#3b82f6"   # azul
        HOVER_BG  = "#eef2ff"   # azul muy clarito al hover

        self.configure(bg=BG_MAIN)

        # ---------- HEADER (icono + título) ----------
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(pady=40)

        icon_label = tk.Label(
            header,
            text="📍",
            font=("Segoe UI Emoji", 40),  # si en tu SO no se ve bien puedes cambiar la fuente
            bg=BG_MAIN
        )
        icon_label.pack()

        title_label = tk.Label(self,text="Whale Tracking System",font=("Arial", 16, "bold"),bg=BG_MAIN, fg=TEXT_DARK)
        title_label.pack(pady=(10, 0))

        # ---------- CONTENEDOR DE TARJETAS ----------
        cards_frame = tk.Frame(self, bg=BG_MAIN)
        cards_frame.pack(pady=40)

        # Para que las tarjetas no se encojan
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)

        # Tarjeta 1: Start Tracking
        start_card = self._create_card(
            cards_frame,
            title="Start Tracking",
            subtitle="Start new tracking",
            BG_MAIN=BG_MAIN,
            CARD_BG=CARD_BG,
            TEXT_DARK=TEXT_DARK,
            TEXT_MUTED=TEXT_MUTED,
            ACCENT=ACCENT,
            HOVER_BG=HOVER_BG,
            command=self._go_to_tracking,
            icon_text="▶"  # pseudo-icono
        )
        start_card.grid(row=0, column=0, padx=20)

        # Tarjeta 2: View Logs
        logs_card = self._create_card(
            cards_frame,
            title="View Logs",
            subtitle="Tracking history",
            BG_MAIN=BG_MAIN,
            CARD_BG=CARD_BG,
            TEXT_DARK=TEXT_DARK,
            TEXT_MUTED=TEXT_MUTED,
            ACCENT=ACCENT,
            HOVER_BG=HOVER_BG,
            command=self._view_logs,
            icon_text="⟳"
        )
        logs_card.grid(row=0, column=1, padx=20)

        # Tarjeta 3: Configure GPS (placeholder)
        gps_card = self._create_card(
            cards_frame,
            title="Configure GPS",
            subtitle="Device settings",
            BG_MAIN=BG_MAIN,
            CARD_BG=CARD_BG,
            TEXT_DARK=TEXT_DARK,
            TEXT_MUTED=TEXT_MUTED,
            ACCENT=ACCENT,
            HOVER_BG=HOVER_BG,
            command=self._configure_gps,
            icon_text="⚙"
        )
        gps_card.grid(row=0, column=2, padx=20)

        # ---------- FOOTER ----------
        footer = tk.Label(
            self,
            text="v1.0.0  -  Whale Tracking System",
            font=("Arial", 9),
            bg=BG_MAIN,
            fg=TEXT_MUTED
        )
        footer.pack(side="bottom", pady=10)

    # ---------- Helpers internos ----------

    def _create_card(
        self, parent, title, subtitle,
        BG_MAIN, CARD_BG, TEXT_DARK, TEXT_MUTED,
        ACCENT, HOVER_BG, command, icon_text=""
    ):
        """Crea una 'tarjeta' clickable estilo botón grande."""
        card = tk.Frame(
            parent,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#e5e7eb"  # gris borde suave
        )
        card.configure(width=220, height=140)
        card.pack_propagate(False)  # que no se encoja al contenido

        # Icono arriba (texto grande simulando icono)
        icon_lbl = tk.Label(
            card,
            text=icon_text,
            font=("Arial", 24),
            bg=CARD_BG,
            fg=ACCENT
        )
        icon_lbl.pack(pady=(15, 5))

        # Título
        title_lbl = tk.Label(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            bg=CARD_BG,
            fg=TEXT_DARK
        )
        title_lbl.pack()

        # Subtítulo
        subtitle_lbl = tk.Label(
            card,
            text=subtitle,
            font=("Arial", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_lbl.pack(pady=(5, 0))

        # Hacer que toda la tarjeta actúe como botón
        def on_click(event=None):
            if command:
                command()

        def on_enter(event=None):
            card.config(bg=HOVER_BG)
            icon_lbl.config(bg=HOVER_BG)
            title_lbl.config(bg=HOVER_BG)
            subtitle_lbl.config(bg=HOVER_BG)

        def on_leave(event=None):
            card.config(bg=CARD_BG)
            icon_lbl.config(bg=CARD_BG)
            title_lbl.config(bg=CARD_BG)
            subtitle_lbl.config(bg=CARD_BG)

        for widget in (card, icon_lbl, title_lbl, subtitle_lbl):
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        return card

    # ---------- Acciones de las tarjetas ----------

    def _go_to_tracking(self):
        """Ir a la pantalla de tracking principal."""
        self.app.show_screen("tracking")

    def _view_logs(self):
        """Ir a la pantalla del historial"""
        self.app.show_screen("logs")

    def _configure_gps(self):
        """Ir a la pantalla de configuración."""
        self.app.show_screen("config")

class TrackingScreen(tk.Frame):
    def __init__(self, parent, app, handlers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.handlers = handlers
    
        # Crear un marco exterior con borde gris y margen interior
        outer_frame = tk.Frame(self, bd=0.5, relief="solid", bg="white")  # Borde gris claro
        outer_frame.pack(padx=20, pady=20)  # Margen interior de 20 píxeles
    
        # ------  Lógica para rastreo de tiempo por ballena --------------#
        # Labels (columns)
        columns = [
            "ID", "M-C", "Init Pos", "Init Time", "Final Pos", "Final Time", "Surface Time", "# Sightings",
            "Behavior", "# Blows", "First Blow",
            "# Whales", "Individual (letter)", "Initial Distance", "Angle",
            "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
            "Feces", "# Feces", "# Boats", "Boat Speed",
            "WW-Whale Distance", "Engine On",
            "# Visibility", "Hydrophone", "Observations"
        ]
        # índices útiles
        IDX_INIT_POS  = columns.index("Init Pos")
        IDX_INIT_TIME  = columns.index("Init Time")
        IDX_FINAL_POS = columns.index("Final Pos")
        IDX_FINAL_TIME  = columns.index("Final Time")
        IDX_TIME      = columns.index("Surface Time")

        # diccionario para guardar el momento en que se presionó Start por ballena
        start_times = {
            "A": None,
            "B": None,
            "C": None,
        }

        def format_elapsed(seconds):
            seconds = int(seconds)
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            if h:
                return f"{h:02d}:{m:02d}:{s:02d}"
            return f"{m:02d}:{s:02d}"

        def get_whale_row(whale_id):
            if whale_id == "A":
                return whale_row_A
            elif whale_id == "B":
                return whale_row_B
            else:
                return whale_row_C

        # funciones para cambiar de estado el label
        def set_status_tracking(whale_id):
            lbl = status_labels[whale_id]
            lbl.config(text="Tracking", bg="orange", fg="black")

        start_times = {}        # whale_id -> t0 (float) o None
        stop_snapshot = {}      # whale_id -> {"elapsed": float, "final_time": str, "final_pos": str} o None
        def on_start_whale(whale_id):
            """
            Start: guarda hora de inicio y escribe Init Pos automáticamente.
            """
            set_status_tracking(whale_id)
            row = get_whale_row(whale_id)

            # 1) guardar la hora actual
            start_times[whale_id] = time.time()
            stop_snapshot[whale_id] = None   # nuevo start invalida cualquier stop anterior

            # 2) obtener posición actual (aquí decides de dónde sale)
            #    Por ahora:
            # pos = ""
            if "get_current_position" in handlers:
                # si tienes un handler en main que devuelve la posición
                pos = handlers["get_current_position"](whale_id)
            else:
                # placeholder si aún no tienes lógica real de posición
                pos = "AUTO_POS"

            # 3) escribir en Init Pos
            widget_init = row[IDX_INIT_POS]
            if isinstance(widget_init, tk.StringVar):
                widget_init.set(pos)
            else:
                widget_init.delete(0, "end")
                widget_init.insert(0, pos)

            # 4) Escribir en Init Time la hora actual
            init_time = time.strftime("%H:%M:%S", time.localtime())  # Formato: "YYYY-MM-DD HH:MM:SS"
            widget_init_time = row[IDX_INIT_TIME]  # Asumimos que IDX_INIT_TIME es el índice correcto para el campo de Init Time
            if isinstance(widget_init_time, tk.StringVar):
                widget_init_time.set(init_time)
            else:
                widget_init_time.delete(0, "end")
                widget_init_time.insert(0, init_time)

            # (opcional) limpiar Final Pos y Time
            widget_final = row[IDX_FINAL_POS]
            widget_time  = row[IDX_TIME]
            widget_final_time = row[IDX_FINAL_TIME]

            for w, val in [(widget_final, ""), (widget_time, ""), (widget_final_time, "")]:
                if isinstance(w, tk.StringVar):
                    w.set(val)
                else:
                    w.delete(0, "end")
            
            stop_gone_counter(whale_id)
        
        def on_stop_whale(whale_id):
            """
            Stop: calcula tiempo desde Start, y escribe Final Pos y Time.
            """
            row = get_whale_row(whale_id)

            t0 = start_times.get(whale_id)
            if t0 is None:
                messagebox.showwarning(
                    "Sin inicio",
                    f"Primero presiona 'Start' para la ballena {whale_id}."
                )
                return

            elapsed = time.time() - t0

            # 1) Final Pos
            # pos = ""
            if "get_current_position" in handlers:
                pos = handlers["get_current_position"](whale_id)
            else:
                pos = "AUTO_POS_END"

            final_time = time.strftime("%H:%M:%S", time.localtime())

            # >>> guardar el ÚLTIMO STOP (freeze)
            stop_snapshot[whale_id] = {"elapsed": elapsed, "final_time": final_time, "final_pos": pos}

            widget_final = row[IDX_FINAL_POS]
            if isinstance(widget_final, tk.StringVar):
                widget_final.set(pos)
            else:
                widget_final.delete(0, "end")
                widget_final.insert(0, pos)

            # 2) Time (duración)
            time_str = format_elapsed(elapsed)
            widget_time = row[IDX_TIME]
            if isinstance(widget_time, tk.StringVar):
                widget_time.set(time_str)
            else:
                widget_time.delete(0, "end")
                widget_time.insert(0, time_str)

            # 3) Escribir la hora de finalización (Final Time)
            final_time = time.strftime("%H:%M:%S", time.localtime())  # Hora de finalización
            widget_final_time = row[IDX_FINAL_TIME]  # Asumimos que IDX_FINAL_TIME es el índice correcto para Final Time

            if isinstance(widget_final_time, tk.StringVar):
                widget_final_time.set(final_time)
            else:
                widget_final_time.delete(0, "end")
                widget_final_time.insert(0, final_time)

            start_gone_counter(whale_id)

        # ------------- lógica para llevar el estado del tracking ---------#
        def set_status_available(whale_id):
            lbl = status_labels[whale_id]
            lbl.config(text="Available", bg="green", fg="white")

        # se espera confirmacion del main de datos correctos para cambiar el estado a available
        handlers["status_available"] = set_status_available
        ###------------------------SECCIÓN 1 - TITULOS Y BOTONES DE STATUS Y TRACKING---------------------###
        # Crear un canvas para dibujar la línea
        canvas = tk.Canvas(outer_frame, width=1200, height=650, bg="white")
        canvas.pack()  # Margen interior de 20 píxeles

        # Dibujar la línea horizontal en la altura de la primera sección
        line_height = 610 // 6  # Dividir la altura total en 4 partes
        canvas.create_line(0, line_height, 1160, line_height, fill="black", width=1)

        line_height = line_height // 2  
        canvas.create_line(0, line_height, 1160, line_height, fill="black", width=1)

        # linea vertical que separa whale A de B
        line_x = 1160 // 3  
        canvas.create_line(line_x, 52, line_x, 100, fill="black", width=1)
        line_x2 = 774  
        canvas.create_line(line_x2, 52, line_x2, 100, fill="black", width=1)

        # Añadir las etiquetas y botones para "Whale A" y "Whale B"
        # Fila 1: Whale A
        whale_a_label = tk.Label(outer_frame, text="Whale A", font=("Arial", 14), bg="white")
        whale_a_label.place(x=10, y=65)

        # Rectángulo informativo para "Available" (verde)
        status_whale_a = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
        status_whale_a.place(x=100, y=65, width=80, height=25)  

        start_button_whale_a = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=lambda: on_start_whale("A"))
        start_button_whale_a.place(x=190, y=65, width=80, height=25)

        stop_button_whale_a = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=lambda: on_stop_whale("A"))
        stop_button_whale_a.place(x=280, y=65, width=80, height=25)

        # Fila 2: Whale B
        whale_b_label = tk.Label(outer_frame, text="Whale B", font=("Arial", 14), bg="white")
        whale_b_label.place(x=397, y=65, width=80, height=25)

        # Rectángulo informativo para "Available" (verde)
        status_whale_b = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
        status_whale_b.place(x=490, y=65, width=80, height=25) 

        start_button_whale_b = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=lambda: on_start_whale("B"))
        start_button_whale_b.place(x=580, y=65, width=80, height=25)

        stop_button_whale_b = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=lambda: on_stop_whale("B"))
        stop_button_whale_b.place(x=670, y=65, width=80, height=25)

        # Fila 3: Whale C
        whale_c_label = tk.Label(outer_frame, text="Whale C", font=("Arial", 14), bg="white")
        whale_c_label.place(x=783, y=65, width=80, height=25)

        # Rectángulo informativo para "Available" (verde)
        status_whale_c = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
        status_whale_c.place(x=873, y=65, width=80, height=25) 

        start_button_whale_c = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=lambda: on_start_whale("C"))
        start_button_whale_c.place(x=963, y=65, width=80, height=25)

        stop_button_whale_c = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=lambda: on_stop_whale("C"))
        stop_button_whale_c.place(x=1053, y=65, width=80, height=25)

        # Botón Back (volver a la pantalla de inicio)
        back_btn = tk.Button(
            outer_frame,
            text="← Back",
            font=("Arial", 10),
            bg="#6B7280",
            fg="white",
            command=lambda: self.app.show_screen("start")
        )
        back_btn.place(x=540, y=583, width=80, height=20)

        # Añadir textos real time tracking y general tracking
        real_time_label = tk.Label(outer_frame, text="Real Time Tracking", font=("Arial", 14), bg="white")
        real_time_label.place(x=30, y=10)

        general_route_label = tk.Label(outer_frame, text="General Route", font=("Arial", 14), bg="white")
        general_route_label.place(x=750, y=10)

        # ------- General Route (tracking global) ---
        self.start_button_general_tracking = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=self.start_general_tracking)
        self.start_button_general_tracking.place(x=910, y=10, width=100, height=25)

        self.stop_button_general_tracking = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=self.stop_general_tracking)
        self.stop_button_general_tracking.place(x=1030, y=10, width=100, height=25)

        # Estado del tracking general
        self.general_tracking_active = False
        self.general_tracking_job = None   # id del after()
        self.general_route_file = None     # ruta del CSV
        self.general_interval_min = 5      # valor por defecto (n minutos)

        # diccionario para llevar el estado del tracking
        status_labels = {
            "A": status_whale_a,
            "B": status_whale_b,
            "C": status_whale_c,
        }

        ###--------------------------------SECCIÓN 2 - FORMULARIO DE REGISTRO--------------------------------###
        # Colores y fuentes
        HEADER_BG = "#f5f5f7"
        FORM_BG   = "white"
        TEXT_GRAY = "#555555"

        new_record_label = tk.Label(
            outer_frame,
            text="Enter new record",
            font=("Arial", 10, "bold"),
            bg=FORM_BG,
            fg=TEXT_GRAY
        )
        new_record_label.place(x=10, y=105)

        def create_whale_form(frame, whale_id_letter, row_index):
            """Create one row of column titles + input widgets inside `frame`."""

            labels = [
                "ID", "M-C", "Init Pos","Init Time", "Final Pos", "Final Time", "Surface Time", "# Sightings",
                "Behavior", "# Blows", "First Blow",
                "# Whales", "Individual (letter)", "Initial Distance", "Angle",
                "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
                "Feces", "# Feces", "# Boats", "Boat Speed",
                "WW-Whale Distance", "Engine On",
                "# Visibility", "Hydrophone", "Observations"
            ]
            
            options = {
                "Behavior": [
                    "t - traveling", "sf - surface feeding",
                    "hac - half anticyclonic circle", "hc - half cyclonic circle",
                    "r - resting", "br - breaching", "n - nursing",
                    "f or zz - foraging or zig-zag", "st - straight line"
                ],
                "First Blow": ["Y", "N"],
                "Fluke": ["Y", "N"],
                "Shallow dive": ["Y", "N"],
                "Feces": ["N", "Y"],
                "M-C": ["0", "M-Madre", "C-Cria"],
                "Engine On": ["Y", "N"],
                "Hydrophone": ["Y", "N"]
            }

            entries = []
            # --- Almacenaremos todos los StringVar para que no sean borrados por Python ---
            # Esto es vital para que el Combobox mantenga su valor.
            frame._string_vars = []
            for col, label in enumerate(labels):
                # Header cell
                tk.Label(
                    frame,
                    text=label,
                    bg=HEADER_BG,
                    fg=TEXT_GRAY,
                    font=("Arial", 9, "bold"),
                    anchor="center"
                ).grid(row=row_index, column=col, padx=6, pady=(0, 2), sticky="we")

                # --- ID FIELD (non-editable) ---
                if label == "ID":
                    entry = ttk.Entry(frame, width=16)
                    entry.insert(0, whale_id_letter)
                    entry.configure(justify="center")
                    entry.configure(state="disabled")  # NO editable
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)
                    continue

                # Input cell just below
                if label in options:
                    var = tk.StringVar(frame)
                    var.set(options[label][0]) # Establece el valor por defecto
                    combo = ttk.Combobox(
                        frame,
                        textvariable=var,
                        values=options[label],
                        width=14,
                        state="readonly"
                    )
                    combo.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    # --- CORRECCIÓN VITAL: Mantener la variable viva ---
                    frame._string_vars.append(var)
                    entries.append(combo) # Devolvemos el widget para el scroll/get
                elif label == "# Skin Sample":
                    # For "# Skin Sample", set the default value to 0
                    skin_sample_var = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    # Aseguramos que el valor "0" se muestre inmediatamente, si textvariable falla.
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries
                elif label == "# Feces":
                    # For "# Feces", set the default value to 0
                    feces = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    # Aseguramos que el valor "0" se muestre inmediatamente, si textvariable falla.
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries                    
                elif label == "# Boats":
                    # For "# Boats", set the default value to 0
                    boats_var = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries
                elif label == "Boat Speed":
                    # For "Boat Speed", set the default value to 0
                    boat_speed_var = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries
                elif label == "# Blows":
                    # For "Boat Speed", set the default value to 0
                    blows_var = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries
                elif label == "WW-Whale Distance":
                    # For "WW-Whale Distance", set the default value to 0
                    ww_whale_dist_var = tk.StringVar(frame, value="0")  # Default value is 0
                    entry = ttk.Entry(frame, width=16)
                    entry.insert(0, "0")
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)  # Add the StringVar to the list of entries
                else:
                    entry = ttk.Entry(frame, width=16)
                    entry.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(entry)

            return entries

        def get_form_data(entries, columns):
            """
            entries: lista que devolvió create_whale_form (widgets/StringVar)
            columns: lista de nombres de columna (la misma que se usa para la tabla)
            Devuelve un diccionario { "Init Pos": "valor", ... }
            """
            data = {}
            for col_name, widget in zip(columns, entries):
                # ID está deshabilitado, pero es un Entry normal
                # Behavior, Fluke, etc. son StringVar (porque vienen de Combobox)
                if isinstance(widget, tk.StringVar):
                    value = widget.get()
                else:
                    value = widget.get()
                data[col_name] = value
            return data

        # ---------- FORMULARIO A ----------
        def ensure_visible_h(canvas, widget, padding=20):
            """
            Mueve el canvas horizontalmente y verticalmente para que 'widget'
            quede dentro de la zona visible cuando recibe el foco.
            """
            canvas.update_idletasks()  # Asegura que las coordenadas sean actuales
            widget.update_idletasks()  # Asegura que el widget esté actualizado

            # 1. Dimensiones de la vista actual (en este caso, con desplazamiento)
            x0_view = canvas.canvasx(0)
            y0_view = canvas.canvasy(0)
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            x1_view = x0_view + canvas_width
            y1_view = y0_view + canvas_height

            # 2. Posición mundial (scrollregion) del widget
            widget_world_x = widget.winfo_x()
            widget_world_y = widget.winfo_y()
            widget_width = widget.winfo_width()
            widget_height = widget.winfo_height()
            widget_world_x1 = widget_world_x + widget_width  # Borde derecho mundial
            widget_world_y1 = widget_world_y + widget_height  # Borde inferior mundial

            # 3. Ancho y alto total para la normalización
            bbox = canvas.bbox("all")
            if not bbox:
                return
            total_width = bbox[2] - bbox[0]
            total_height = bbox[3] - bbox[1]
            if total_width <= 0 or total_height <= 0:
                return

            new_x0, new_y0 = None, None

            # Caso 1: Widget demasiado a la izquierda
            if widget_world_x - padding < x0_view:
                new_x0 = widget_world_x - padding

            # Caso 2: Widget demasiado a la derecha
            elif widget_world_x1 + padding > x1_view:
                new_x0 = widget_world_x1 + padding - canvas_width

            # Caso 3: Widget demasiado arriba
            if widget_world_y - padding < y0_view:
                new_y0 = widget_world_y - padding

            # Caso 4: Widget demasiado abajo
            elif widget_world_y1 + padding > y1_view:
                new_y0 = widget_world_y1 + padding - canvas_height

            # Desplazamos solo si es necesario
            if new_x0 is not None or new_y0 is not None:
                if new_x0 is not None:
                    # 4. Asegurar límites (new_x0 nunca puede ser negativo)
                    if new_x0 < 0:
                        new_x0 = 0
                    fraction_x = new_x0 / total_width
                    fraction_x = max(0, min(1, fraction_x))
                    canvas.xview_moveto(fraction_x)

                if new_y0 is not None:
                    # 5. Asegurar límites (new_y0 nunca puede ser negativo)
                    if new_y0 < 0:
                        new_y0 = 0
                    fraction_y = new_y0 / total_height
                    fraction_y = max(0, min(1, fraction_y))
                    canvas.yview_moveto(fraction_y)

        def bind_autoscroll_to_widgets(canvas, widgets):
            def on_focus(event, c=canvas):
                widget = event.widget
                # Asegurarnos de que el widget se mueva si está oculto
                ensure_visible_h(c, widget)

            for w in widgets:
                # Asegurarnos de que todos los tipos de widgets adecuados reciban el enfoque
                if isinstance(w, (tk.Entry, ttk.Entry, ttk.Combobox, tk.Text)):
                    w.bind("<FocusIn>", on_focus)  # Cuando el widget recibe el foco
                    w.bind("<Enter>", on_focus)    # Cuando el cursor entra en el widget

        #### Contador de cuanto tiempo hace que una ballena se fue #######
        whale_ids = ["A", "B", "C"]

        gone_running = {wid: False for wid in whale_ids}
        gone_start   = {wid: None  for wid in whale_ids}
        gone_afterid = {wid: None  for wid in whale_ids}
        gone_var     = {wid: tk.StringVar(value="00:00") for wid in whale_ids}  # label por ballena

        def fmt_mmss(seconds: float) -> str:
            s = int(seconds)
            mm = s // 60
            ss = s % 60
            return f"{mm:02d}:{ss:02d}"

        def _update_gone_counter(whale_id: str):
            if not gone_running[whale_id] or gone_start[whale_id] is None:
                return

            elapsed = time.time() - gone_start[whale_id]
            gone_var[whale_id].set(fmt_mmss(elapsed))

            gone_afterid[whale_id] = outer_frame.after(200, lambda: _update_gone_counter(whale_id))

        def start_gone_counter(whale_id: str):
            # STOP: reinicia a 0 y empieza a contar
            if gone_afterid[whale_id] is not None:
                try:
                    outer_frame.after_cancel(gone_afterid[whale_id])
                except Exception:
                    pass
                gone_afterid[whale_id] = None

            gone_var[whale_id].set("00:00")
            gone_start[whale_id] = time.time()
            gone_running[whale_id] = True
            _update_gone_counter(whale_id)

        def stop_gone_counter(whale_id: str):
            # START: pausa el contador
            gone_running[whale_id] = False
            if gone_afterid[whale_id] is not None:
                try:
                    outer_frame.after_cancel(gone_afterid[whale_id])
                except Exception:
                    pass
                gone_afterid[whale_id] = None

        #-----------------------------------
        gone_panel = tk.Frame(outer_frame, bg=FORM_BG)
        gone_panel.place(x=10, y=125, width=80, height=280)  # ajusta height según tus 3 filas

        # A (misma y que el contenedor A)
        tk.Label(gone_panel, text="A:", bg=FORM_BG).place(x=0, y=25)
        tk.Label(gone_panel, textvariable=gone_var["A"], bg=FORM_BG, font=("Arial", 12, "bold")).place(x=20, y=23)

        form_container_A = tk.Frame(outer_frame, bg=FORM_BG, bd=1, relief="solid")
        form_container_A.place(x=100, y=125, width=1045, height=80)

        form_canvas_A = tk.Canvas(form_container_A, bg=FORM_BG, highlightthickness=0)
        form_canvas_A.pack(side="top", fill="both", expand=True)

        h_scrollbar_A = tk.Scrollbar(form_container_A, orient="horizontal", command=form_canvas_A.xview)
        h_scrollbar_A.place(x=0, y=60, width=1042)

        form_canvas_A.configure(xscrollcommand=h_scrollbar_A.set)

        form_frame_A = tk.Frame(form_canvas_A, bg=FORM_BG)
        form_canvas_A.create_window((0, 0), window=form_frame_A, anchor="nw")

        def on_form_A_configure(event):
            form_canvas_A.configure(scrollregion=form_canvas_A.bbox("all"))

        form_frame_A.bind("<Configure>", on_form_A_configure)

        whale_row_A = create_whale_form(form_frame_A, "A", 0)

        def on_save_whale_a():
            whale_id = "A"

            # 0) debe existir start
            t0 = start_times.get(whale_id, None)
            if t0 is None:
                messagebox.showwarning("Sin inicio", f"Primero presiona 'Start' para la ballena {whale_id}.")
                return

            # 1) si NUNCA dieron stop, crear stop "por defecto" UNA sola vez (freeze)
            if stop_snapshot.get(whale_id) is None:
                elapsed = time.time() - t0

                if "get_current_position" in handlers:
                    pos = handlers["get_current_position"](whale_id)
                else:
                    pos = "AUTO_POS_END"

                final_time = time.strftime("%H:%M:%S", time.localtime())
                stop_snapshot[whale_id] = {"elapsed": elapsed, "final_time": final_time, "final_pos": pos}

                # y sí: llenamos los campos (para que lo que guardes sea coherente con GUI)
                row = get_whale_row(whale_id)

                widget_final = row[IDX_FINAL_POS]
                if isinstance(widget_final, tk.StringVar):
                    widget_final.set(pos)
                else:
                    widget_final.delete(0, "end")
                    widget_final.insert(0, pos)

                time_str = format_elapsed(elapsed)
                widget_time = row[IDX_TIME]
                if isinstance(widget_time, tk.StringVar):
                    widget_time.set(time_str)
                else:
                    widget_time.delete(0, "end")
                    widget_time.insert(0, time_str)

                widget_final_time = row[IDX_FINAL_TIME]
                if isinstance(widget_final_time, tk.StringVar):
                    widget_final_time.set(final_time)
                else:
                    widget_final_time.delete(0, "end")
                    widget_final_time.insert(0, final_time)

                # >>> CLAVE: si Save “define” que se fue, arrancar contador de “se fue hace…”
                start_gone_counter(whale_id)
            # 2) ahora sí, guardar (sin recalcular tiempos)
            data = get_form_data(whale_row_A, columns)

            ok = True
            if "save_whale" in handlers:
                ok = handlers["save_whale"](whale_id, data)  # debe devolver True/False

            # 3) si guardó bien, apagar timer definitivo
            if ok:
                start_times[whale_id] = None
                stop_snapshot[whale_id] = None

        save_button_whale_a = tk.Button(outer_frame, text="Save Whale A", font=("Arial", 10), bg="#2563EB", fg="white", command=on_save_whale_a)
        save_button_whale_a.place(x=1024, y=105, width=105, height=15)
        bind_autoscroll_to_widgets(form_canvas_A, whale_row_A)

        # ---------- FORMULARIO B ----------
        # B (80px abajo si cada form_container mide 80 de alto)
        tk.Label(gone_panel, text="B:", bg=FORM_BG).place(x=0, y=130)
        tk.Label(gone_panel, textvariable=gone_var["B"], bg=FORM_BG, font=("Arial", 12, "bold")).place(x=20, y=128)

        form_container_B = tk.Frame(outer_frame, bg=FORM_BG, bd=1, relief="solid")
        form_container_B.place(x=100, y=230, width=1045, height=80)

        form_canvas_B = tk.Canvas(form_container_B, bg=FORM_BG, highlightthickness=0)
        form_canvas_B.pack(side="top", fill="both", expand=True)

        h_scrollbar_B = tk.Scrollbar(form_container_B, orient="horizontal", command=form_canvas_B.xview)
        h_scrollbar_B.place(x=0, y=60, width=1042)

        form_canvas_B.configure(xscrollcommand=h_scrollbar_B.set)

        form_frame_B = tk.Frame(form_canvas_B, bg=FORM_BG)
        form_canvas_B.create_window((0, 0), window=form_frame_B, anchor="nw")

        def on_form_B_configure(event):
            form_canvas_B.configure(scrollregion=form_canvas_B.bbox("all"))

        form_frame_B.bind("<Configure>", on_form_B_configure)

        whale_row_B = create_whale_form(form_frame_B, "B", 0)

        def on_save_whale_b():
            whale_id = "B"

            # 0) debe existir start
            t0 = start_times.get(whale_id, None)
            if t0 is None:
                messagebox.showwarning("Sin inicio", f"Primero presiona 'Start' para la ballena {whale_id}.")
                return

            # 1) si NUNCA dieron stop, crear stop "por defecto" UNA sola vez (freeze)
            if stop_snapshot.get(whale_id) is None:
                elapsed = time.time() - t0

                if "get_current_position" in handlers:
                    pos = handlers["get_current_position"](whale_id)
                else:
                    pos = "AUTO_POS_END"

                final_time = time.strftime("%H:%M:%S", time.localtime())
                stop_snapshot[whale_id] = {"elapsed": elapsed, "final_time": final_time, "final_pos": pos}

                # y sí: llenamos los campos (para que lo que guardes sea coherente con GUI)
                row = get_whale_row(whale_id)

                widget_final = row[IDX_FINAL_POS]
                if isinstance(widget_final, tk.StringVar):
                    widget_final.set(pos)
                else:
                    widget_final.delete(0, "end")
                    widget_final.insert(0, pos)

                time_str = format_elapsed(elapsed)
                widget_time = row[IDX_TIME]
                if isinstance(widget_time, tk.StringVar):
                    widget_time.set(time_str)
                else:
                    widget_time.delete(0, "end")
                    widget_time.insert(0, time_str)

                widget_final_time = row[IDX_FINAL_TIME]
                if isinstance(widget_final_time, tk.StringVar):
                    widget_final_time.set(final_time)
                else:
                    widget_final_time.delete(0, "end")
                    widget_final_time.insert(0, final_time)

                # >>> CLAVE: si Save “define” que se fue, arrancar contador de “se fue hace…”
                start_gone_counter(whale_id)

            # 2) ahora sí, guardar (sin recalcular tiempos)
            data = get_form_data(whale_row_B, columns)

            ok = True
            if "save_whale" in handlers:
                ok = handlers["save_whale"](whale_id, data)  # debe devolver True/False

            # 3) si guardó bien, apagar timer definitivo
            if ok:
                start_times[whale_id] = None
                stop_snapshot[whale_id] = None

        save_button_whale_b = tk.Button(outer_frame, text="Save Whale B", font=("Arial", 10), bg="#2563EB", fg="white", command=on_save_whale_b)
        save_button_whale_b.place(x=1024, y=208, width=105, height=15)
        bind_autoscroll_to_widgets(form_canvas_B, whale_row_B)

        #----------------------------- FORMULARIO C -------------
        tk.Label(gone_panel, text="C:", bg=FORM_BG).place(x=0, y=235)
        tk.Label(gone_panel, textvariable=gone_var["C"], bg=FORM_BG, font=("Arial", 12, "bold")).place(x=20, y=233)

        form_container_C = tk.Frame(outer_frame, bg=FORM_BG, bd=1, relief="solid")
        form_container_C.place(x=100, y=335, width=1045, height=80)

        form_canvas_C = tk.Canvas(form_container_C, bg=FORM_BG, highlightthickness=0)
        form_canvas_C.pack(side="top", fill="both", expand=True)

        h_scrollbar_C = tk.Scrollbar(form_container_C, orient="horizontal", command=form_canvas_C.xview)
        h_scrollbar_C.place(x=0, y=60, width=1042)

        form_canvas_C.configure(xscrollcommand=h_scrollbar_C.set)

        form_frame_C = tk.Frame(form_canvas_C, bg=FORM_BG)
        form_canvas_C.create_window((0, 0), window=form_frame_C, anchor="nw")

        def on_form_C_configure(event):
            form_canvas_C.configure(scrollregion=form_canvas_C.bbox("all"))

        form_frame_C.bind("<Configure>", on_form_C_configure)

        whale_row_C = create_whale_form(form_frame_C, "C", 0)

        def on_save_whale_c():
            whale_id = "C"

            # 0) debe existir start
            t0 = start_times.get(whale_id, None)
            if t0 is None:
                messagebox.showwarning("Sin inicio", f"Primero presiona 'Start' para la ballena {whale_id}.")
                return

            # 1) si NUNCA dieron stop, crear stop "por defecto" UNA sola vez (freeze)
            if stop_snapshot.get(whale_id) is None:
                elapsed = time.time() - t0

                if "get_current_position" in handlers:
                    pos = handlers["get_current_position"](whale_id)
                else:
                    pos = "AUTO_POS_END"

                final_time = time.strftime("%H:%M:%S", time.localtime())
                stop_snapshot[whale_id] = {"elapsed": elapsed, "final_time": final_time, "final_pos": pos}

                # y sí: llenamos los campos (para que lo que guardes sea coherente con GUI)
                row = get_whale_row(whale_id)

                widget_final = row[IDX_FINAL_POS]
                if isinstance(widget_final, tk.StringVar):
                    widget_final.set(pos)
                else:
                    widget_final.delete(0, "end")
                    widget_final.insert(0, pos)

                time_str = format_elapsed(elapsed)
                widget_time = row[IDX_TIME]
                if isinstance(widget_time, tk.StringVar):
                    widget_time.set(time_str)
                else:
                    widget_time.delete(0, "end")
                    widget_time.insert(0, time_str)

                widget_final_time = row[IDX_FINAL_TIME]
                if isinstance(widget_final_time, tk.StringVar):
                    widget_final_time.set(final_time)
                else:
                    widget_final_time.delete(0, "end")
                    widget_final_time.insert(0, final_time)

                # >>> CLAVE: si Save “define” que se fue, arrancar contador de “se fue hace…”
                start_gone_counter(whale_id)
                
            # 2) ahora sí, guardar (sin recalcular tiempos)
            data = get_form_data(whale_row_C, columns)

            ok = True
            if "save_whale" in handlers:
                ok = handlers["save_whale"](whale_id, data)  # debe devolver True/False

            # 3) si guardó bien, apagar timer definitivo
            if ok:
                start_times[whale_id] = None
                stop_snapshot[whale_id] = None

        save_button_whale_c = tk.Button(outer_frame, text="Save Whale C", font=("Arial", 10), bg="#2563EB", fg="white", command=on_save_whale_c)
        save_button_whale_c.place(x=1024, y=313, width=110, height=15)
        bind_autoscroll_to_widgets(form_canvas_C, whale_row_C)
        ###---------------------------------------SECCIÓN 3 - ÚLTIMOS REGISTROS-----------------------------------###
        #---------------------------------- FUNCIONES AUXILIARES ----------------------------------#
        def clear_form(entries):
            """
            Limpia todos los campos del formulario, excepto el ID (pos 0).
            entries = lista que devuelve create_whale_form
            """
            # Guardamos los valores predeterminados de los campos
            default_values = {}
            for i, widget in enumerate(entries):
                if i == 0:  # ID → no se borra
                    continue

                if isinstance(widget, ttk.Combobox):
                    # Guardamos el valor por defecto de los Combobox
                    default_values[i] = widget.get()

                elif isinstance(widget, tk.StringVar):
                    # Para los StringVars, guardamos su valor actual
                    default_values[i] = widget.get()

                elif isinstance(widget, ttk.Entry):
                    # Para los Entry, si tienen valores predeterminados, los guardamos
                    if widget.get() == "0":  # Para casos como "# Skin Sample", "# Feces", "# Boats", etc.
                        default_values[i] = "0"

            # Limpiar los campos del formulario
            for i, widget in enumerate(entries):
                if i == 0:  # ID → no se borra
                    continue

                if isinstance(widget, tk.StringVar):
                    # Para los StringVars, los restablecemos al valor original
                    widget.set(default_values.get(i, ""))  # Restaurar el valor predeterminado

                elif isinstance(widget, ttk.Combobox):
                    # Para los Combobox, restauramos el valor predeterminado
                    widget.set(default_values.get(i, widget.get()))  # Restaurar el valor predeterminado o el actual

                elif isinstance(widget, ttk.Entry):
                    # Restauramos el valor predeterminado (si es "0" o cualquier otro valor inicial)
                    if i in default_values:
                        widget.delete(0, "end")
                        widget.insert(0, default_values[i])
                    else:
                        widget.delete(0, "end")  # Limpiar el Entry normalmente



        def clear_form_A():
            clear_form(whale_row_A)

        def clear_form_B():
            clear_form(whale_row_B)
        
        def clear_form_C():
            clear_form(whale_row_C)

        # Hacemos accesibles las funciones de limpieza desde main.py
        handlers["clear_forms"] = {
            "A": clear_form_A,
            "B": clear_form_B,
            "C": clear_form_C,
        }

        #---------------------------------- GUI DE LA SECCIÓN 3 ----------------------------------#

        # Título de la sección
        last_records_label = tk.Label(
            outer_frame,
            text="Last records",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#555555"
        )
        last_records_label.place(x=10, y=420)

        # Marco que contiene la tabla
        records_frame = tk.Frame(outer_frame, bg="white", bd=1, relief="solid")
        records_frame.place(x=10, y=440, width=1135, height=140)

        # Treeview inside the table_frame
        tree = ttk.Treeview(
            records_frame,
            columns=columns,
            show="headings",
            height=4
        )

        # Función que pide los últimos registros a main.py y llena la tabla
        item_to_dbid = {}  
        def load_last_5_records():
            """Carga los últimos 5 registros desde la BD usando el handler."""
            # limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            item_to_dbid.clear()

            # pedir datos a main.py
            if "fetch_last_records" not in handlers:
                return  # por seguridad

            records = handlers["fetch_last_records"]()

            for rec in records:
                db_id = rec.get("_db_id")  # id real de BD (1,2,3,...)
                values = [rec.get(col, "") for col in columns]

                item = tree.insert("", "end", values=values)

                if db_id is not None:
                    item_to_dbid[item] = db_id

        # Estilo
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        style.configure("Treeview", font=("Arial", 9))

        # Configurar encabezados y ancho de columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Barra horizontal conectada AL TREEVIEW
        h_scroll = ttk.Scrollbar(records_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=h_scroll.set)

        # Ubicar ambos
        tree.place(x=0, y=0, width=1133, height=125)
        h_scroll.place(x=0, y=120, width=1133)

        # Mostrar registros iniciales
        load_last_5_records()

        # Mapeo columna -> nombre 
        col_to_field = {i: col for i, col in enumerate(columns)}

        def edit_cell(event):
            region = tree.identify("region", event.x, event.y)
            if region != "cell":
                return

            row_id = tree.identify_row(event.y)
            col_id = tree.identify_column(event.x)
            if not row_id or not col_id:
                return

            col_index = int(col_id.replace("#", "")) - 1
            field_name = col_to_field[col_index]

            # No dejamos editar el ID desde aquí
            if field_name == "ID":
                return

            # Preguntar antes de permitir la edición
            seguro = messagebox.askyesno(
                "Editar celda",
                f"¿Quieres editar el campo '{field_name}'?"
            )
            if not seguro:
                return  # el usuario se arrepintió

            # Posición y tamaño de la celda
            x, y, width, height = tree.bbox(row_id, col_id)
            current_value = tree.set(row_id, field_name)

            edit_var = tk.StringVar()
            edit_var.set(current_value)

            edit_entry = ttk.Entry(tree, textvariable=edit_var)
            edit_entry.place(x=x, y=y, width=width, height=height)
            edit_entry.focus()

            def save_edit(event=None):
                new_value = edit_var.get()

                # Si no cambió nada, simplemente cerrar
                if new_value == current_value:
                    edit_entry.destroy()
                    return

                # Confirmar antes de guardar el cambio
                seguro_guardar = messagebox.askyesno(
                    "Confirmar cambio",
                    f"¿Cambiar '{current_value}' por '{new_value}' en '{field_name}'?"
                )
                if not seguro_guardar:
                    # restaurar valor original por si se cambió en el Entry
                    tree.set(row_id, field_name, current_value)
                    edit_entry.destroy()
                    return

                # Actualizar el Treeview
                tree.set(row_id, field_name, new_value)

                # aquí es donde usamos el id REAL de la BD
                db_id = item_to_dbid.get(row_id)
                if db_id is not None and "update_record_field" in handlers:
                    handlers["update_record_field"](db_id, field_name, new_value)

                edit_entry.destroy()

            edit_entry.bind("<Return>", save_edit)
            edit_entry.bind("<FocusOut>", lambda e: edit_entry.destroy())

        tree.bind("<Double-1>", edit_cell)

        # Función que main.py puede llamar después de guardar
        def refresh_last_records():
            load_last_5_records()

        # Dejamos accesible a main.py
        handlers["refresh_last_records"] = refresh_last_records
    
    #----------- FUNCIONES PARA EL GPS GLOBAL -------------#
    def start_general_tracking(self):
        if self.general_tracking_active:
            messagebox.showinfo("General Route", "El tracking general ya está en marcha.")
            return

        # Asegurarse de que hay handler para posición
        if "get_current_position" not in self.handlers:
            messagebox.showerror("Error", "No hay handler para obtener posición GPS.")
            return

        # Preguntar cada cuántos minutos quieres registrar
        n = simpledialog.askinteger(
            "Intervalo de registro",
            "¿Cada cuántos minutos quieres guardar la posición?",
            initialvalue=self.general_interval_min,
            minvalue=1,
            parent=self,
        )
        if n is None:
            return  # canceló

        self.general_interval_min = n
        interval_ms = n * 60 * 1000

        # Usa una carpeta fija de prueba:
        folder = os.getcwd()

        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"general_route_{timestamp}.csv"
        self.general_route_file = os.path.join(folder, filename)

        # Escribir encabezado
        try:
            with open(self.general_route_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["fecha", "hora", "latitud", "longitud"])  # Nuevo encabezado
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el archivo:\n{e}")
            self.general_route_file = None
            return

        # Marcar como activo y cambiar colores
        self.general_tracking_active = True
        self.start_button_general_tracking.config(bg="#16A34A")  # verde
        self.stop_button_general_tracking.config(bg="#DC2626")   # rojo

        # Guardar intervalo y lanzar primera captura
        self.general_interval_ms = interval_ms
        self._capture_general_point()  # primera captura inmediata

    def _capture_general_point(self):
        """Captura una posición y programa la siguiente captura."""
        if not self.general_tracking_active:
            return
        if not self.general_route_file:
            return

        # Obtener posición del handler (no ligada a A o B, así que paso None)
        try:
            pos = self.handlers["get_current_position"](None)
        except Exception as e:
            print("Error obteniendo posición GPS:", e)
            pos = "GPS_ERROR"

        # Timestamp actual
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: "YYYY-MM-DD HH:MM:SS"
        date, time = ts.split(" ")  # Dividir la fecha y la hora

        # Separar latitud y longitud (asumimos que `pos` es "latitud,longitud")
        lat, lon = pos.split(",") if pos != "GPS_ERROR" else ("0.0", "0.0")

        # Guardar en el CSV
        try:
            with open(self.general_route_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date, time, lat, lon])  # Guardar en columnas separadas
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo escribir en el archivo de tracking:\n{e}")
            # si falla, mejor detener el tracking
            self.stop_general_tracking(show_message=False)
            return

        # Programar siguiente captura
        self.general_tracking_job = self.after(self.general_interval_ms, self._capture_general_point)

    def stop_general_tracking(self, show_message=True):
        if not self.general_tracking_active:
            if show_message:
                messagebox.showinfo("General Route", "No hay tracking general en marcha.")
            return

        self.general_tracking_active = False

        # Cancelar after si está programado
        if self.general_tracking_job is not None:
            try:
                self.after_cancel(self.general_tracking_job)
            except Exception:
                pass
            self.general_tracking_job = None

        # Reset colores de botones
        self.start_button_general_tracking.config(bg="black")
        self.stop_button_general_tracking.config(bg="black")

        # Avisar dónde quedó el archivo
        if show_message and self.general_route_file:
            messagebox.showinfo(
                "Tracking general finalizado",
                f"Se guardó el tracking general en:\n{self.general_route_file}"
            )

class LogsScreen(tk.Frame):
    def __init__(self, parent, app, handlers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.handlers = handlers

        BG = "#f5f7fb"
        TEXT = "#111827"

        self.configure(bg=BG)

        # MAPPING Treeview item -> id de la BD
        self.item_to_dbid = {}

        # ---------- Título ----------
        title = tk.Label(
            self,
            text="Tracking History",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=TEXT
        )
        title.pack(pady=(20, 10))

        # ----- Filtros de fecha -----
        filter_frame = tk.Frame(self, bg=BG)
        filter_frame.pack(pady=10)

        actions_frame = tk.Frame(self, bg=BG)
        actions_frame.pack(pady=(5,10))

        tk.Label(
            filter_frame,
            # text="From (YYYY-MM-DD):",
            text="From (DD-MM-YYYY):",
            bg=BG,
            fg=TEXT,
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.entry_from = tk.Entry(filter_frame, width=12)
        self.entry_from.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            filter_frame,
            text="To (DD-MM-YYYY):",
            bg=BG,
            fg=TEXT,
            font=("Arial", 10)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.entry_to = tk.Entry(filter_frame, width=12)
        self.entry_to.grid(row=0, column=3, padx=5, pady=5)

        # Paleta de colores para botones
        COLORS = {
            "primary": "#2563EB",     # Filter, Export
            "secondary": "#6B7280",   # Clear, Back
            "success": "#16A34A",     # Refresh
            "danger": "#DC2626",      # Delete
            "backup": "#1E3A8A",      # Backup DB
            "text": "#111827",
            "bg": "#F3F4F6",
        }

        filter_btn = tk.Button(
            filter_frame,
            text="Filter",
            font=("Arial", 10),
            bg=COLORS["primary"],
            fg="white",
            command=self.apply_filter         
        )
        filter_btn.grid(row=0, column=4, padx=10, pady=5)

        clear_btn = tk.Button(
            filter_frame,
            text="Clear",
            font=("Arial", 10),
            bg=COLORS["secondary"],
            fg="white",
            command=self.clear_filters
        )
        clear_btn.grid(row=0, column=5, padx=10, pady=5)

        export_btn = tk.Button(
            actions_frame,
            text="Export CSV",
            font=("Arial", 10),
            bg=COLORS["primary"],
            fg="white",
            command=self.export_csv         
        )
        export_btn.grid(row=0, column=6, padx=10, pady=5)

        delete_btn = tk.Button(
            actions_frame,
            text="Delete selected",
            font=("Arial", 10),
            bg=COLORS["danger"],
            fg="white",
            command=self.delete_selected
        )
        delete_btn.grid(row=0, column=7, padx=10, pady=5)

        refresh_btn = tk.Button(
            actions_frame,
            text="Refresh",
            font=("Arial", 10),
            bg=COLORS["success"],
            fg="white",
            command=self.refresh_view
        )
        refresh_btn.grid(row=0, column=8, padx=10, pady=5)

        backup_btn = tk.Button(
            actions_frame,
            text="Backup DB",
            font=("Arial", 10),
            bg=COLORS["backup"],
            fg="white",
            command=self.backup_db
        )
        backup_btn.grid(row=0, column=9, padx=10, pady=5)

        back_btn = tk.Button(
            actions_frame,
            text="← Back",
            font=("Arial", 10),
            bg= COLORS["secondary"],
            fg="white",
            command=lambda: self.app.show_screen("start")
        )
        back_btn.grid(row=0, column=10, padx=10, pady=5)

        # ---------- Tabla para ver registros ----------
        table_frame = tk.Frame(self, bg=BG)
        table_frame.pack(pady=30, padx=40, fill="both", expand=True)

        self.columns = [
            "Date", "ID", "M-C", "Init Pos","Init Time", "Final Pos", "Final Time", "Surface Time",
            "# Sightings", "Behavior", "# Blows", "First Blow",
            "# Whales", "Individual (letter)", "Initial Distance", "Angle",
            "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
            "Feces", "# Feces","# Boats", "Boat Speed",
            "WW-Whale Distance", "Engine On",
            "# Visibility", "Hydrophone", "Observations"
        ]

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,          
            show="headings",
            height=12
        )
        self.tree.bind("<Button-1>", self._tree_deselect)
        self.tree.bind("<Escape>", lambda e: self.tree.selection_remove(self.tree.selection()))

        # headers
        for col in self.columns:         
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar horizontal
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scroll_x.set)

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        # ----------------------
        # Layout usando GRID
        # ----------------------
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_x.grid(row=1, column=0, sticky="ew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        # ----------------------
        # Para que el Treeview se expanda
        # ----------------------
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # donde guardamos los registros actuales (para exportar a CSV)
        self.current_records = []

        # opcional: cargar algo inicial (últimos 20)
        self.load_logs()

    # --------- Lógica de filtros ---------

    def apply_filter(self):
        start_str = self.entry_from.get().strip()
        end_str = self.entry_to.get().strip()

        if not start_str and not end_str:
            messagebox.showwarning("Fechas requeridas", "Ingresa al menos una fecha.")
            return

        # si solo ponen una, usamos la misma como from/to
        if start_str and not end_str:
            end_str = start_str
        if end_str and not start_str:
            start_str = end_str

        # validar formato DD-MM-YYYY
        for label, value in (("From", start_str), ("To", end_str)):
            try:
                datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror(
                    "Formato inválido",
                    f"El campo '{label}' debe tener formato DD-MM-YYYY."
                )
                return

        # Convertir las fechas a formato YYYY-MM-DD para trabajar internamente
        try:
            start_date = datetime.strptime(start_str, "%d-%m-%Y").date()  # Convertir a YYYY-MM-DD
            end_date = datetime.strptime(end_str, "%d-%m-%Y").date()  # Convertir a YYYY-MM-DD
        except ValueError:
            messagebox.showerror(
                "Error de fecha",
                "Hubo un error al convertir las fechas. Asegúrate de que el formato sea DD-MM-YYYY."
            )
            return

        # Convertir las fechas a formato string en YYYY-MM-DD para usarlas en la consulta
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        if "fetch_records_by_date" not in self.handlers:
            messagebox.showerror("Error", "No hay handler para filtrar por fecha.")
            return

        records = self.handlers["fetch_records_by_date"](start_date_str, end_date_str)
        self.current_records = records  # guardamos para exportar

        # limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_to_dbid.clear()

        # rellenar
        for rec in records:
            values = [rec.get(col, "") for col in self.columns]
            item_id = self.tree.insert("", "end", values=values)

            # guardar id de BD
            db_id = rec.get("_db_id")
            if db_id is not None:
                self.item_to_dbid[item_id] = db_id

    def clear_filters(self):
        """Limpia las cajas de fecha y recarga el log inicial (últimos registros)."""
        self.entry_from.delete(0, "end")
        self.entry_to.delete(0, "end")
        self.load_logs()

    def refresh_view(self):
        """Vuelve a cargar la vista actual: filtro si hay fechas, log inicial si no."""
        start_str = self.entry_from.get().strip()
        end_str = self.entry_to.get().strip()

        # Si no hay fechas → simplemente recargar últimos registros
        if not start_str and not end_str:
            self.load_logs()
            return

        # Si hay algo escrito, usamos la lógica de filtros
        self.apply_filter()

    #----------- Deseleccionar celda ------------------
    def _tree_deselect(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region not in ("cell", "tree"):
            self.tree.selection_remove(self.tree.selection())

    # --------- Borrar registros seleccionados ---------
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Sin selección", "Selecciona al menos un registro para borrar.")
            return

        if "delete_records" not in self.handlers:
            messagebox.showerror("Error", "No hay handler para borrar registros.")
            return

        if not messagebox.askyesno(
            "Confirmar borrado",
            f"¿Borrar {len(selected_items)} registro(s)? Esta acción no se puede deshacer."
        ):
            return

        # obtener ids de la BD asociados a los items seleccionados
        db_ids = []
        for item in selected_items:
            db_id = self.item_to_dbid.get(item)
            if db_id is not None:
                db_ids.append(db_id)

        if not db_ids:
            messagebox.showwarning(
                "No encontrado",
                "No se encontraron IDs de base de datos para los registros seleccionados."
            )
            return

        # borrar en la BD
        try:
            self.handlers["delete_records"](db_ids)
        except Exception as e:
            messagebox.showerror("Error al borrar", f"No se pudieron borrar los registros:\n{e}")
            return

        # borrar del Treeview y de estructuras locales
        for item in selected_items:
            self.tree.delete(item)
            self.item_to_dbid.pop(item, None)

        # actualizar self.current_records filtrando los que borramos
        self.current_records = [
            r for r in self.current_records
            if r.get("_db_id") not in db_ids
        ]

        messagebox.showinfo("Borrado", "Registros borrados correctamente.")


    # --------- Exportar CSV ---------
    def export_csv(self):
        if not self.current_records:
            messagebox.showinfo("Sin datos", "No hay registros para exportar.")
            return

        # separar registros por ID (A y B)
        records_A = [rec for rec in self.current_records if rec.get("ID") == "A"]
        records_B = [rec for rec in self.current_records if rec.get("ID") == "B"]
        records_C = [rec for rec in self.current_records if rec.get("ID") == "C"]

        if not records_A and not records_B and not records_C:
            messagebox.showinfo(
                "Sin datos",
                "No hay registros con ID 'A', 'B' ni 'C' en el filtro actual."
            )
            return

        # -----------------------------
        # Construir sufijo de fecha/rango
        # -----------------------------
        start_str = self.entry_from.get().strip()
        end_str = self.entry_to.get().strip()

        # Normalizar como haces en apply_filter
        if start_str and not end_str:
            end_str = start_str
        if end_str and not start_str:
            start_str = end_str

        def normalize_date(s):
            try:
                # lo dejamos en YYYY-MM-DD bien formateado
                return datetime.strptime(s, "%Y-%m-%d").date().isoformat()
            except Exception:
                return s  # por si acaso

        if start_str and end_str:
            start_norm = normalize_date(start_str)
            end_norm = normalize_date(end_str)
            if start_norm == end_norm:
                date_suffix = f"_{start_norm}"
            else:
                date_suffix = f"_{start_norm}_to_{end_norm}"
        else:
            # sin filtro de fechas: usar timestamp para no sobrescribir
            ts = datetime.now().strftime("%Y-%m-%d")
            date_suffix = f"_{ts}"

        # -----------------------------
        # Carpeta por defecto: donde está el programa / exe
        # -----------------------------
        try:
            if getattr(sys, "frozen", False):
                folder = os.path.dirname(sys.executable)  # cuando es .exe
            else:
                folder = os.path.dirname(os.path.abspath(__file__))  # en desarrollo
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo obtener la carpeta del programa:\n{e}"
            )
            return

        errors = []

        # función interna para escribir un archivo
        def write_csv(path, records):
            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                # Escribir los encabezados
                # Nuevos encabezados con columnas separadas para fecha, hora, latitud y longitud
                writer.writerow([
                    "fecha", "hora", "ID", "M-C", "Init Latitude","Init Longitude", "Init Time", "Final Latitude", "Final Longitude","Final Time",
                    "Surface Time", "# Sightings", "Behavior", "# Blows", "First Blow", "# Whales",
                    "Individual (letter)", "Initial Distance", "Angle", "# Photos", "Fluke", "Shallow dive",
                    "# Skin Sample", "Feces", "# Feces", "# Boats", "Boat Speed", "WW-Whale Distance", "Engine On",
                    "# Visibility", "Hydrophone", "Observations", "Latitud", "Longitud"
                ])

                for rec in records:
                    # Separar los valores de fecha y hora
                    timestamp = rec.get("Date", "")
                    date, time = timestamp.split(" ") if timestamp else ("", "")
                    
                    # Separar latitud y longitud
                    init_pos = rec.get("Init Pos", "")
                    lat_init, lon_init = init_pos.split(",") if init_pos else ("", "")

                    # Separar latitud y longitud de Final Pos (latitud, longitud)
                    final_pos = rec.get("Final Pos", "")
                    lat_final, lon_final = final_pos.split(",") if final_pos else ("", "")

                    # Crear una fila con los nuevos valores separados
                    row = [
                        date,  # fecha
                        time,  # hora
                        rec.get("ID", ""),
                        rec.get("M-C", ""),
                        lat_init,  # latitud inicial
                        lon_init,  # longitud inicial
                        rec.get("Init Time", ""),
                        lat_final, # latitud final
                        lon_final, # longitud final
                        rec.get("Final Time", ""),
                        rec.get("Surface Time", ""),
                        rec.get("# Sightings", ""),
                        rec.get("Behavior", ""),
                        rec.get("# Blows", ""),
                        rec.get("First Blow", ""),
                        rec.get("# Whales", ""),
                        rec.get("Individual (letter)", ""),
                        rec.get("Initial Distance", ""),
                        rec.get("Angle", ""),
                        rec.get("# Photos", ""),
                        rec.get("Fluke", ""),
                        rec.get("Shallow dive", ""),
                        rec.get("# Skin Sample", ""),
                        rec.get("Feces", ""),
                        rec.get("# Feces", ""),
                        rec.get("# Boats", ""),
                        rec.get("Boat Speed", ""),
                        rec.get("WW-Whale Distance", ""),
                        rec.get("Engine On", ""),
                        rec.get("# Visibility", ""),
                        rec.get("Hydrophone", ""),
                        rec.get("Observations", ""),
                    ]
                    writer.writerow(row)

        # guardar A
        path_A = None
        if records_A:
            filename_A = f"whale_A_logs{date_suffix}.csv"
            path_A = os.path.join(folder, filename_A)
            try:
                write_csv(path_A, records_A)
            except Exception as e:
                errors.append(f"A: {e}")

        # guardar B
        path_B = None
        if records_B:
            filename_B = f"whale_B_logs{date_suffix}.csv"
            path_B = os.path.join(folder, filename_B)
            try:
                write_csv(path_B, records_B)
            except Exception as e:
                errors.append(f"B: {e}")
        # Guardar C
        path_C = None
        if records_C:
            filename_C = f"whale_C_logs{date_suffix}.csv"
            path_C = os.path.join(folder, filename_C)
            try:
                write_csv(path_C, records_C)
            except Exception as e:
                errors.append(f"C: {e}")

        if errors:
            messagebox.showerror(
                "Error al exportar",
                "Ocurrieron errores al exportar:\n" + "\n".join(errors)
            )
        else:
            msg = "Archivos exportados correctamente:\n"
            if path_A:
                msg += f"  - {path_A}\n"
            if path_B:
                msg += f"  - {path_B}\n"
            if path_C:
                msg += f"  - {path_C}\n"  
            messagebox.showinfo("Exportación exitosa", msg)

    # ---------- Cargar algo al entrar, esto es para el log ----------
    def load_logs(self):
        """Carga algunos registros iniciales (por ejemplo, los últimos 20)."""
        if "fetch_last_records" not in self.handlers:
            return

        records = self.handlers["fetch_last_records"](limit=20)
        self.current_records = records

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_to_dbid.clear()   # limpiar mapping inicial

        for rec in records:
            values = [rec.get(col, "") for col in self.columns]
            item_id = self.tree.insert("", "end", values=values)

            db_id = rec.get("_db_id")
            if db_id is not None:
                self.item_to_dbid[item_id] = db_id

    def backup_db(self):
        """Pide una carpeta y crea un backup de la base de datos ahí."""
        if "backup_db" not in self.handlers:
            messagebox.showerror("Error", "No hay handler para hacer backup de la base de datos.")
            return

        # Obtener carpeta del ejecutable o del script
        try:
            import sys, os
            if getattr(sys, "frozen", False):
                folder = os.path.dirname(sys.executable)      # cuando es .exe
            else:
                folder = os.path.dirname(os.path.abspath(__file__))  # cuando es código fuente
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener carpeta del programa:\n{e}")
            return

        try:
            backup_path = self.handlers["backup_db"](folder)
        except Exception as e:
            messagebox.showerror(
                "Error al crear backup",
                f"No se pudo crear el backup de la base de datos:\n{e}"
            )
            return

        messagebox.showinfo(
            "Backup creado",
            f"Backup creado correctamente en:\n{backup_path}"
        )

class ConfigScreen(tk.Frame):
    def __init__(self, parent, app, handlers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.app = app
        self.handlers = handlers

        self.config_data = gps.load_config()

        bg = "#f5f7fb"
        text = "#111827"

        self.configure(bg=bg)

        title = tk.Label(
            self,
            text="GPS Configuration",
            font=("Arial", 22, "bold"),
            bg=bg,
            fg=text
        )
        title.pack(pady=(140, 10))

        # ----- Tarjeta centrada -----
        card = tk.Frame(self, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center")

        inner = tk.Frame(card, bg="white")
        inner.pack(padx=40, pady=30)

        # Texto explicativo
        info = tk.Label(
            inner,
            text=(
                "This app can use the Windows GNSS location sensor\n"
                "(u-blox) or a simulated GPS for testing."
            ),
            bg="white",
            fg=text,
            font=("Arial", 10),
            justify="left"
        )
        info.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # ------- USE MOCK -------
        self.use_mock_var = tk.BooleanVar()
        self.use_mock_var.set(self.config_data.get("use_mock", True))

        chk = tk.Checkbutton(
            inner,
            text="Use simulated GPS (testing mode)",
            variable=self.use_mock_var,
            bg="white",
            fg=text,
            font=("Arial", 10),
            anchor="w"
        )
        chk.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # ------- BOTONES -------
        btn_frame = tk.Frame(inner, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=2)

        test_btn = tk.Button(
            btn_frame,
            text="Test GPS",
            font=("Arial", 10),
            bg="#2563EB",
            fg="white",
            width=10,
            command=self.test_gps
        )
        test_btn.grid(row=0, column=0, padx=5)

        save_btn = tk.Button(
            btn_frame,
            text="Save",
            font=("Arial", 10),
            bg="#16A34A",
            fg="white",
            width=10,
            command=self.save_config
        )
        save_btn.grid(row=0, column=1, padx=5)

        back_btn = tk.Button(
            btn_frame,
            text="← Back",
            font=("Arial", 10),
            bg="#6B7280",
            fg="white",
            width=10,
            command=lambda: self.app.show_screen("start")
        )
        back_btn.grid(row=0, column=2, padx=5)

    # ---------------- TEST GPS ----------------
    def test_gps(self):
        use_mock = self.use_mock_var.get()

        if use_mock:
            messagebox.showinfo(
                "Test OK",
                "Simulated GPS is active.\n"
                "Switch off this option to test the real GNSS sensor."
            )
            return

        try:
            # test_connection ya ignora config, así que no le pasamos nada
            lat, lon = gps.test_connection()
            messagebox.showinfo(
                "GPS OK",
                f"Fix acquired:\nLat: {lat:.5f}\nLon: {lon:.5f}"
            )
        except gps.GPSNotAvailable as e:
            messagebox.showerror(
                "GPS not available",
                f"{e}\n\nCheck that:\n"
                "- The GNSS sensor is enabled in Windows.\n"
                "- You have location permissions."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not read GPS:\n{e}")

    # ---------------- SAVE CONFIG ----------------
    def save_config(self):
        new_cfg = {
            "use_mock": self.use_mock_var.get()
        }

        gps.save_config(new_cfg)

        if "configure_gps" in self.handlers:
            self.handlers["configure_gps"](new_cfg)

        messagebox.showinfo("Saved", "GPS configuration saved.")
        self.app.show_screen("start")
