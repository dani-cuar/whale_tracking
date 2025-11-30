import tkinter as tk
from tkinter import ttk, messagebox

def run_gui(handlers):
    # Crear la ventana principal
    root = tk.Tk()

    # Establecer las dimensiones de la ventana (ancho x alto)
    root.geometry("1200x650")  # Por ejemplo, 1200 píxeles de ancho y 650 píxeles de alto

    # Título de la ventana
    root.title("Whale Tracking System")

    # Crear un marco exterior con borde gris y margen interior
    outer_frame = tk.Frame(root, bd=0.5, relief="solid", bg="white")  # Borde gris claro
    outer_frame.pack(padx=20, pady=20)  # Margen interior de 20 píxeles

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

    start_button_whale_a = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white")
    start_button_whale_a.place(x=330, y=65, width=100, height=25)

    stop_button_whale_a = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white")
    stop_button_whale_a.place(x=450, y=65, width=100, height=25)

    # Fila 2: Whale B
    whale_b_label = tk.Label(outer_frame, text="Whale B", font=("Arial", 14), bg="white")
    whale_b_label.place(x=630, y=65, width=100, height=25)

    # Rectángulo informativo para "Available" (verde)
    status_whale_b = tk.Label(outer_frame, text="Available", font=("Arial", 12), bg="green", fg="white")
    status_whale_b.place(x=790, y=65, width=100, height=25) 

    start_button_whale_b = tk.Button(outer_frame, text="Start", font=("Arial", 12), bg="black", fg="white")
    start_button_whale_b.place(x=910, y=65, width=100, height=25)

    stop_button_whale_b = tk.Button(outer_frame, text="Stop", font=("Arial", 12), bg="black", fg="white")
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
            "Visibility", "Hydrophone", "Observations"
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
                entry.configure(state="disabled")  # 🔒 NO editable
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
        columns: lista de nombres de columna (la misma que usas para la tabla)
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
    # Labels (columns)
    columns = [
        "ID", "Init Pos", "Final Pos", "Time", "# Sightings",
        "Behavior", "# Blows", "First Blow",
        "# Whales", "Individual (letter)", "Initial Distance",
        "# Photos", "Fluke", "Shallow dive", "# Skin Sample",
        "Feces in Trail", "# Boats", "Boat Speed",
        "WW-Whale Distance", "Engine On",
        "Visibility", "Hydrophone", "Observations"
    ]

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

    # Iniciar el bucle de la aplicación
    root.mainloop()



