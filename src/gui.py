import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import time
import os

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

        # Tarjeta 2: View Logs (por ahora solo muestra un mensaje)
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
        """Otro placeholder para futura configuración."""
        messagebox.showinfo("GPS", "Aquí podrías configurar el GPS/dispositivo.")

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
            "ID", "Init Pos", "Final Pos", "Time", "# Sightings",
            "Behavior", "# Blows", "First Blow",
            "# Whales", "Individual (letter)", "Initial Distance",
            "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
            "Feces in Trail", "# Boats", "Boat Speed",
            "WW-Whale Distance", "Engine On",
            "# Visibility", "Hydrophone", "Observations"
        ]
        # índices útiles
        IDX_INIT_POS  = columns.index("Init Pos")
        IDX_FINAL_POS = columns.index("Final Pos")
        IDX_TIME      = columns.index("Time")

        # diccionario para guardar el momento en que se presionó Start por ballena
        start_times = {
            "A": None,
            "B": None,
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
            else:
                return whale_row_B

        # funciones para cambiar de estado el label
        def set_status_tracking(whale_id):
            lbl = status_labels[whale_id]
            lbl.config(text="Tracking", bg="orange", fg="black")

        def on_start_whale(whale_id):
            """
            Start: guarda hora de inicio y escribe Init Pos automáticamente.
            """
            set_status_tracking(whale_id)
            row = get_whale_row(whale_id)

            # 1) guardar la hora actual
            start_times[whale_id] = time.time()

            # 2) obtener posición actual (aquí decides de dónde sale)
            #    Por ahora:
            pos = ""
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

            # (opcional) limpiar Final Pos y Time
            widget_final = row[IDX_FINAL_POS]
            widget_time  = row[IDX_TIME]

            if isinstance(widget_final, tk.StringVar):
                widget_final.set("")
            else:
                widget_final.delete(0, "end")

            if isinstance(widget_time, tk.StringVar):
                widget_time.set("")
            else:
                widget_time.delete(0, "end")

        def on_stop_whale(whale_id):
            """
            Stop: calcula tiempo desde Start, y escribe Final Pos y Time.
            """
            row = get_whale_row(whale_id)

            t0 = start_times.get(whale_id)
            if t0 is None:
                # Nunca se presionó Start para esta ballena
                messagebox.showwarning(
                    "Sin inicio",
                    f"Primero presiona 'Start' para la ballena {whale_id}."
                )
                return

            elapsed = time.time() - t0
            start_times[whale_id] = None  # reseteamos

            # 1) Final Pos
            pos = ""
            if "get_current_position" in handlers:
                pos = handlers["get_current_position"](whale_id)
            else:
                pos = "AUTO_POS_END"

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
        line_x = 1160 // 2  
        canvas.create_line(line_x, 52, line_x, 100, fill="black", width=1)

        # Añadir las etiquetas y botones para "Whale A" y "Whale B"
        # Fila 1: Whale A
        whale_a_label = tk.Label(outer_frame, text="Whale A", font=("Arial", 14), bg="white")
        whale_a_label.place(x=50, y=65)

        # Rectángulo informativo para "Available" (verde)
        status_whale_a = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
        status_whale_a.place(x=210, y=65, width=100, height=25)  

        start_button_whale_a = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=lambda: on_start_whale("A"))
        start_button_whale_a.place(x=330, y=65, width=100, height=25)

        stop_button_whale_a = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=lambda: on_stop_whale("A"))
        stop_button_whale_a.place(x=450, y=65, width=100, height=25)

        # Fila 2: Whale B
        whale_b_label = tk.Label(outer_frame, text="Whale B", font=("Arial", 14), bg="white")
        whale_b_label.place(x=630, y=65, width=100, height=25)

        # Rectángulo informativo para "Available" (verde)
        status_whale_b = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
        status_whale_b.place(x=790, y=65, width=100, height=25) 

        start_button_whale_b = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white", command=lambda: on_start_whale("B"))
        start_button_whale_b.place(x=910, y=65, width=100, height=25)

        stop_button_whale_b = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white", command=lambda: on_stop_whale("B"))
        stop_button_whale_b.place(x=1030, y=65, width=100, height=25)

        # Añadir textos real time tracking y general tracking
        real_time_label = tk.Label(outer_frame, text="Real Time Tracking", font=("Arial", 14), bg="white")
        real_time_label.place(x=30, y=10)

        general_route_label = tk.Label(outer_frame, text="General Route", font=("Arial", 14), bg="white")
        general_route_label.place(x=750, y=10)

        start_button_general_tracking = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white")
        start_button_general_tracking.place(x=910, y=10, width=100, height=25)

        stop_button_general_tracking = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white")
        stop_button_general_tracking.place(x=1030, y=10, width=100, height=25)

        # diccionario para llevar el estado del tracking
        status_labels = {
            "A": status_whale_a,
            "B": status_whale_b,
        }
        ###--------------------------------SECCIÓN 2 - FORMULARIO DE REGISTRO--------------------------------###
        # Colores y fuentes
        HEADER_BG = "#f5f5f7"
        FORM_BG   = "white"
        TEXT_GRAY = "#555555"

        new_record_label = tk.Label(
            outer_frame,
            text="Enter new record",
            font=("Arial", 12, "bold"),
            bg=FORM_BG,
            fg=TEXT_GRAY
        )
        new_record_label.place(x=10, y=110)

        def create_whale_form(frame, whale_id_letter, row_index):
            """Create one row of column titles + input widgets inside `frame`."""

            labels = [
                "ID", "Init Pos", "Final Pos", "Time", "# Sightings",
                "Behavior", "# Blows", "First Blow",
                "# Whales", "Individual (letter)", "Initial Distance",
                "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
                "Feces in Trail", "# Boats", "Boat Speed",
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
                "Feces in Trail": ["Y", "N", "1", "2", "3", "4+"],
                "Engine On": ["Y", "N"],
                "Hydrophone": ["Y", "N"]
            }

            entries = []

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
                    var.set(options[label][0])
                    combo = ttk.Combobox(
                        frame,
                        textvariable=var,
                        values=options[label],
                        width=14,
                        state="readonly"
                    )
                    combo.grid(row=row_index + 1, column=col, padx=6, pady=(0, 5), sticky="we")
                    entries.append(var)
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
        form_container_A = tk.Frame(outer_frame, bg=FORM_BG, bd=1, relief="solid")
        form_container_A.place(x=10, y=140, width=1135, height=80)

        form_canvas_A = tk.Canvas(form_container_A, bg=FORM_BG, highlightthickness=0)
        form_canvas_A.pack(side="top", fill="both", expand=True)

        h_scrollbar_A = tk.Scrollbar(form_container_A, orient="horizontal", command=form_canvas_A.xview)
        h_scrollbar_A.place(x=0, y=60, width=1133)

        form_canvas_A.configure(xscrollcommand=h_scrollbar_A.set)

        form_frame_A = tk.Frame(form_canvas_A, bg=FORM_BG)
        form_canvas_A.create_window((0, 0), window=form_frame_A, anchor="nw")

        def on_form_A_configure(event):
            form_canvas_A.configure(scrollregion=form_canvas_A.bbox("all"))

        form_frame_A.bind("<Configure>", on_form_A_configure)

        whale_row_A = create_whale_form(form_frame_A, "A", 0)

        def on_save_whale_a():
            # whale_row_A es la lista de widgets/StringVar que devolvió create_whale_form
            data = get_form_data(whale_row_A, columns)
            # llamamos al handler externo
            if "save_whale" in handlers:
                handlers["save_whale"]("A", data)      

        save_button_whale_a = tk.Button(outer_frame, text="Save Whale A", font=("Arial", 12), bg="#5bc0ff", fg="white", command=on_save_whale_a)
        save_button_whale_a.place(x=1024, y=115, width=105, height=20)

        # ---------- FORMULARIO B ----------
        form_container_B = tk.Frame(outer_frame, bg=FORM_BG, bd=1, relief="solid")
        form_container_B.place(x=10, y=260, width=1135, height=80)

        form_canvas_B = tk.Canvas(form_container_B, bg=FORM_BG, highlightthickness=0)
        form_canvas_B.pack(side="top", fill="both", expand=True)

        h_scrollbar_B = tk.Scrollbar(form_container_B, orient="horizontal", command=form_canvas_B.xview)
        h_scrollbar_B.place(x=0, y=60, width=1133)

        form_canvas_B.configure(xscrollcommand=h_scrollbar_B.set)

        form_frame_B = tk.Frame(form_canvas_B, bg=FORM_BG)
        form_canvas_B.create_window((0, 0), window=form_frame_B, anchor="nw")

        def on_form_B_configure(event):
            form_canvas_B.configure(scrollregion=form_canvas_B.bbox("all"))

        form_frame_B.bind("<Configure>", on_form_B_configure)

        whale_row_B = create_whale_form(form_frame_B, "B", 0)

        def on_save_whale_b():
            data = get_form_data(whale_row_B, columns)
            if "save_whale" in handlers:
                handlers["save_whale"]("B", data)

        save_button_whale_b = tk.Button(outer_frame, text="Save Whale B", font=("Arial", 12), bg="#5bc0ff", fg="white", command=on_save_whale_b)
        save_button_whale_b.place(x=1024, y=235, width=105, height=20)

        ###---------------------------------------SECCIÓN 3 - ÚLTIMOS REGISTROS-----------------------------------###
        #---------------------------------- FUNCIONES AUXILIARES ----------------------------------#
        def clear_form(entries):
            """
            Limpia todos los campos del formulario, excepto el ID (pos 0).
            entries = lista que devuelve create_whale_form
            """
            for i, widget in enumerate(entries):
                if i == 0:  # ID → no se borra
                    continue

                # Combobox → widget es un StringVar
                if isinstance(widget, tk.StringVar):
                    widget.set(widget.get())  # lo dejamos en su primer valor, si quieres lo vaciamos luego
                else:
                    widget.delete(0, "end")  # Entry normal

        def clear_form_A():
            clear_form(whale_row_A)

        def clear_form_B():
            clear_form(whale_row_B)

        # Hacemos accesibles las funciones de limpieza desde main.py
        handlers["clear_forms"] = {
            "A": clear_form_A,
            "B": clear_form_B,
        }

        #---------------------------------- GUI DE LA SECCIÓN 3 ----------------------------------#

        # Título de la sección
        last_records_label = tk.Label(
            outer_frame,
            text="Last records",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#555555"
        )
        last_records_label.place(x=10, y=350)

        # Marco que contiene la tabla
        records_frame = tk.Frame(outer_frame, bg="white", bd=1, relief="solid")
        records_frame.place(x=10, y=400, width=1135, height=180)

        # Treeview inside the table_frame
        tree = ttk.Treeview(
            records_frame,
            columns=columns,
            show="headings",
            height=4
        )

        # Función que pide los últimos registros a main.py y llena la tabla
        item_to_dbid = {}  
        def load_last_6_records():
            """Carga los últimos 6 registros desde la BD usando el handler."""
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
        tree.place(x=0, y=0, width=1133, height=160)
        h_scroll.place(x=0, y=160, width=1133)

        # Mostrar registros iniciales
        load_last_6_records()

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
            load_last_6_records()

        # Dejamos accesible a main.py
        handlers["refresh_last_records"] = refresh_last_records


# class LogsScreen(tk.Frame):
#     def __init__(self, parent, app, handlers, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.app = app
#         self.handlers = handlers

#         BG = "#f5f7fb"
#         TEXT = "#111827"
#         # MUTED = "#6b7280"

#         self.configure(bg=BG)

#         # ---------- Título ----------
#         title = tk.Label(
#             self,
#             text="Tracking History",
#             font=("Arial", 20, "bold"),
#             bg=BG,
#             fg=TEXT
#         )
#         title.pack(pady=(20, 10))
#         # title.pack(pady=20)

#         # ----- Filtros de fecha -----
#         filter_frame = tk.Frame(self, bg=BG)
#         filter_frame.pack(pady=10)

#         tk.Label(
#             filter_frame,
#             text="From (YYYY-MM-DD):",
#             bg=BG,
#             fg=TEXT,
#             font=("Arial", 10)
#         ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

#         self.entry_from = tk.Entry(filter_frame, width=12)
#         self.entry_from.grid(row=0, column=1, padx=5, pady=5)

#         tk.Label(
#             filter_frame,
#             text="To (YYYY-MM-DD):",
#             bg=BG,
#             fg=TEXT,
#             font=("Arial", 10)
#         ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

#         self.entry_to = tk.Entry(filter_frame, width=12)
#         self.entry_to.grid(row=0, column=3, padx=5, pady=5)

#         filter_btn = tk.Button(
#             filter_frame,
#             text="Filter",
#             font=("Arial", 10),
#             bg="black",
#             fg="white",
#             command=self.apply_filter
#         )
#         filter_btn.grid(row=0, column=4, padx=10, pady=5)

#         export_btn = tk.Button(
#             filter_frame,
#             text="Export CSV",
#             font=("Arial", 10),
#             bg="#2563eb",
#             fg="white",
#             command=self.export_csv
#         )
#         export_btn.grid(row=0, column=5, padx=10, pady=5)

#         back_btn = tk.Button(
#             filter_frame,
#             text="← Back",
#             font=("Arial", 10),
#             bg="#6b7280",
#             fg="white",
#             command=lambda: self.app.show_screen("start")
#         )
#         back_btn.grid(row=0, column=6, padx=10, pady=5)

#         # ---------- Tabla para ver registros ----------
#         table_frame = tk.Frame(self, bg=BG)
#         table_frame.pack(pady=10, padx=40, fill="both", expand=True)

#         self.columns = [
#             "ID", "Init Pos", "Final Pos", "Time",
#             "# Sightings", "Behavior", "# Blows", "First Blow",
#             "# Whales", "Individual (letter)", "Initial Distance",
#             "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
#             "Feces in Trail", "# Boats", "Boat Speed",
#             "WW-Whale Distance", "Engine On",
#             "# Visibility", "Hydrophone", "Observations"
#         ]

#         self.tree = ttk.Treeview(
#             table_frame,
#             columns=columns,
#             show="headings",
#             height=12
#         )

#         # headers
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=150, anchor="center")

#         self.tree.pack(side="left", fill="both", expand=True)

#         # scrollbar
#         scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scrollbar.set)
#         scrollbar.pack(side="right", fill="y")

#         # donde guardamos los registros actuales (para exportar a CSV)
#         self.current_records = []

#         # --------- Lógica de filtros ---------

#         def apply_filter(self):
#             start_str = self.entry_from.get().strip()
#             end_str = self.entry_to.get().strip()

#             if not start_str and not end_str:
#                 messagebox.showwarning("Fechas requeridas", "Ingresa al menos una fecha.")
#                 return

#             # si solo ponen una, usamos la misma como from/to
#             if start_str and not end_str:
#                 end_str = start_str
#             if end_str and not start_str:
#                 start_str = end_str

#             # validar formato YYYY-MM-DD
#             for label, value in (("From", start_str), ("To", end_str)):
#                 try:
#                     datetime.strptime(value, "%Y-%m-%d")
#                 except ValueError:
#                     messagebox.showerror(
#                         "Formato inválido",
#                         f"El campo '{label}' debe tener formato YYYY-MM-DD."
#                     )
#                     return

#             if "fetch_records_by_date" not in self.handlers:
#                 messagebox.showerror("Error", "No hay handler para filtrar por fecha.")
#                 return

#             records = self.handlers["fetch_records_by_date"](start_str, end_str)
#             self.current_records = records  # guardamos para exportar

#             # limpiar tabla
#             for item in self.tree.get_children():
#                 self.tree.delete(item)

#             # rellenar
#             for rec in records:
#                 values = [rec.get(col, "") for col in self.columns]
#                 self.tree.insert("", "end", values=values)

#         # --------- Exportar CSV ---------

#         def export_csv(self):
#             if not self.current_records:
#                 messagebox.showinfo("Sin datos", "No hay registros para exportar.")
#                 return

#             file_path = filedialog.asksaveasfilename(
#                 defaultextension=".csv",
#                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
#                 title="Guardar como CSV"
#             )
#             if not file_path:
#                 return  # usuario canceló

#             try:
#                 with open(file_path, mode="w", newline="", encoding="utf-8") as f:
#                     writer = csv.writer(f)

#                     # encabezados
#                     writer.writerow(self.columns)

#                     # filas
#                     for rec in self.current_records:
#                         row = [rec.get(col, "") for col in self.columns]
#                         writer.writerow(row)

#                 messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\n{file_path}")
#             except Exception as e:
#                 messagebox.showerror("Error al exportar", f"No se pudo guardar el CSV:\n{e}")

#             # ---------- Botón volver ----------
#             back_btn = tk.Button(
#                 self,
#                 text="← Back",
#                 font=("Arial", 12),
#                 bg="black",
#                 fg="white",
#                 command=lambda: self.app.show_screen("start")
#             )
#             back_btn.pack(pady=20)

#         # cargar datos
#         self.load_logs()

#     def load_logs(self):
#         """Carga TODOS los registros de la BD y los muestra en la tabla."""
#         if "fetch_last_records" not in self.handlers:
#             return

#         # IMPORTANTE: pedimos muchos registros (1000) o todos
#         records = self.handlers["fetch_last_records"](limit=1000)

#         # limpiar tabla
#         for item in self.tree.get_children():
#             self.tree.delete(item)

#         for rec in records:
#             values = [rec.get(col, "") for col in self.tree["columns"]]
#             self.tree.insert("", "end", values=values)


class LogsScreen(tk.Frame):
    def __init__(self, parent, app, handlers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.handlers = handlers

        BG = "#f5f7fb"
        TEXT = "#111827"

        self.configure(bg=BG)

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

        tk.Label(
            filter_frame,
            text="From (YYYY-MM-DD):",
            bg=BG,
            fg=TEXT,
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.entry_from = tk.Entry(filter_frame, width=12)
        self.entry_from.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            filter_frame,
            text="To (YYYY-MM-DD):",
            bg=BG,
            fg=TEXT,
            font=("Arial", 10)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.entry_to = tk.Entry(filter_frame, width=12)
        self.entry_to.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = tk.Button(
            filter_frame,
            text="Filter",
            font=("Arial", 10),
            bg="black",
            fg="white",
            command=self.apply_filter          # 👈 ahora existe como método
        )
        filter_btn.grid(row=0, column=4, padx=10, pady=5)

        export_btn = tk.Button(
            filter_frame,
            text="Export CSV",
            font=("Arial", 10),
            bg="#2563eb",
            fg="white",
            command=self.export_csv            # 👈 idem
        )
        export_btn.grid(row=0, column=5, padx=10, pady=5)

        back_btn = tk.Button(
            filter_frame,
            text="← Back",
            font=("Arial", 10),
            bg="#6b7280",
            fg="white",
            command=lambda: self.app.show_screen("start")
        )
        back_btn.grid(row=0, column=6, padx=10, pady=5)

        # ---------- Tabla para ver registros ----------
        table_frame = tk.Frame(self, bg=BG)
        table_frame.pack(pady=10, padx=40, fill="both", expand=True)

        self.columns = [
            "ID", "Init Pos", "Final Pos", "Time",
            "# Sightings", "Behavior", "# Blows", "First Blow",
            "# Whales", "Individual (letter)", "Initial Distance",
            "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
            "Feces in Trail", "# Boats", "Boat Speed",
            "WW-Whale Distance", "Engine On",
            "# Visibility", "Hydrophone", "Observations"
        ]

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,          # 👈 self.columns
            show="headings",
            height=12
        )

        # headers
        for col in self.columns:          # 👈 self.columns
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # donde guardamos los registros actuales (para exportar a CSV)
        self.current_records = []

        # opcional: cargar algo inicial (últimos N)
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

        # validar formato YYYY-MM-DD
        for label, value in (("From", start_str), ("To", end_str)):
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Formato inválido",
                    f"El campo '{label}' debe tener formato YYYY-MM-DD."
                )
                return

        if "fetch_records_by_date" not in self.handlers:
            messagebox.showerror("Error", "No hay handler para filtrar por fecha.")
            return

        records = self.handlers["fetch_records_by_date"](start_str, end_str)
        self.current_records = records  # guardamos para exportar

        # limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # rellenar
        for rec in records:
            values = [rec.get(col, "") for col in self.columns]
            self.tree.insert("", "end", values=values)

    # --------- Exportar CSV ---------
    def export_csv(self):
        if not self.current_records:
            messagebox.showinfo("Sin datos", "No hay registros para exportar.")
            return

        # separar registros por ID (A y B)
        records_A = [rec for rec in self.current_records if rec.get("ID") == "A"]
        records_B = [rec for rec in self.current_records if rec.get("ID") == "B"]

        if not records_A and not records_B:
            messagebox.showinfo(
                "Sin datos",
                "No hay registros con ID 'A' ni 'B' en el filtro actual."
            )
            return

        # pedir carpeta donde guardar los archivos
        folder = filedialog.askdirectory(
            title="Selecciona la carpeta para guardar los CSV de A y B"
        )
        if not folder:
            return  # usuario canceló

        errors = []

        # función interna para escribir un archivo
        def write_csv(path, records):
            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)  # encabezados
                for rec in records:
                    row = [rec.get(col, "") for col in self.columns]
                    writer.writerow(row)

        # guardar A
        path_A = None
        if records_A:
            path_A = os.path.join(folder, "whale_A_logs.csv")
            try:
                write_csv(path_A, records_A)
            except Exception as e:
                errors.append(f"A: {e}")

        # guardar B
        path_B = None
        if records_B:
            path_B = os.path.join(folder, "whale_B_logs.csv")
            try:
                write_csv(path_B, records_B)
            except Exception as e:
                errors.append(f"B: {e}")

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
            messagebox.showinfo("Exportación exitosa", msg)

    
    # ---------- Cargar algo al entrar ----------
    def load_logs(self):
        """Carga algunos registros iniciales (por ejemplo, los últimos 6)."""
        if "fetch_last_records" not in self.handlers:
            return

        records = self.handlers["fetch_last_records"](limit=6)
        self.current_records = records

        for item in self.tree.get_children():
            self.tree.delete(item)

        for rec in records:
            values = [rec.get(col, "") for col in self.columns]
            self.tree.insert("", "end", values=values)

