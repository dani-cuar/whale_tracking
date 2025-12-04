from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from gui import StartScreen, TrackingScreen, LogsScreen, ConfigScreen
import database
import gps

handlers = {}  # diccionario global compartido con la GUI

# Campos que deben ser enteros
NUMERIC_INT_FIELDS = {
    "# Sightings",
    "# Blows",
    "# Whales",
    "# Photos",
    "# Skin Sample",
    "# Boats",
    "# Visibility",
}

# Campos que deben ser decimales (float)
NUMERIC_FLOAT_FIELDS = {
    "Initial Distance",
    "Boat Speed",
    "WW-Whale Distance",
}

# Campo opcional (puede estar vacío)
OPTIONAL_FIELDS = {
    "Observations",
}

LETTER_FIELDS = {
    "Individual (letter)",
}

def validate_record(data_gui):
    """
    data_gui: dict con claves de la GUI (las de `columns`) y valores en texto.
    Devuelve (ok, cleaned_data, errors)
    """
    cleaned = {}
    errors = []

    for key, raw_value in data_gui.items():
        value = raw_value.strip() if isinstance(raw_value, str) else raw_value

        # 1. Campos obligatorios (todos menos OPTIONAL_FIELDS)
        if key not in OPTIONAL_FIELDS:
            if value == "":
                errors.append(f"El campo '{key}' no puede estar vacío.")
                continue  # no seguimos validando este campo

        # 2. Si está vacío y es opcional (Observations), lo guardamos como "" y seguimos
        if key in OPTIONAL_FIELDS and value == "":
            cleaned[key] = ""
            continue

        # 3. Validar enteros
        if key in NUMERIC_INT_FIELDS:
            try:
                cleaned[key] = int(value)
            except ValueError:
                errors.append(f"El campo '{key}' debe ser un número entero.")
            continue

        # 4. Validar decimales
        if key in NUMERIC_FLOAT_FIELDS:
            try:
                cleaned[key] = float(value)
            except ValueError:
                errors.append(f"El campo '{key}' debe ser un número decimal.")
            continue
        
        # 5. Validar campos tipo letra
        if key in LETTER_FIELDS:
            if not isinstance(value, str) or not value.isalpha():
                errors.append(f"El campo '{key}' debe ser una letra")
            else:
                cleaned[key] = value.upper()  # normalizamos a mayúscula
            continue

        # 6. Todo lo demás se queda como texto
        cleaned[key] = value

    ok = len(errors) == 0
    return ok, cleaned, errors

# ------------- HANDLERS LÓGICOS -----------------#

def fetch_last_records_handler(limit=6):
    """
    Devuelve lista de registros con claves de GUI (ID, Init Pos, etc.)
    """
    return database.get_last_records(limit)

def save_whale_handler(whale_id, data_gui):
    """
    whale_id: 'A' o 'B'
    data_gui: dict con claves de la GUI (las de `columns`)
    """

    ok, cleaned_data, errors = validate_record(data_gui)

    if not ok:
        # Construimos un solo mensaje con todas las fallas
        msg = "No se puede guardar el registro por los siguientes motivos:\n\n"
        msg += "\n".join(f"- {e}" for e in errors)
        messagebox.showerror("Error de validación", msg)
        return  # No guardamos en la BD

    # 1. Si todo esta bien convertir claves GUI -> columnas SQL
    db_fields = []
    db_values = []
    for gui_key, value in cleaned_data.items():
        if gui_key not in database.GUI_TO_DB:
            continue
        db_fields.append(database.GUI_TO_DB[gui_key])
        db_values.append(value)

    # 2. asegurarnos de incluir id_tag (A/B)
    # sobrescribimos por si acaso
    if "id_tag" not in db_fields:
        db_fields.insert(0, "id_tag")
        db_values.insert(0, whale_id)

    placeholders = ",".join(["?"] * len(db_fields))
    fields_sql   = ",".join(db_fields)

    with database.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO records ({fields_sql}) VALUES ({placeholders})",
            db_values
        )
        conn.commit()

    # Mensaje opcional de éxito
    messagebox.showinfo("Registro guardado", f"Registro de ballena {whale_id} guardado correctamente.")
    # Notificar a la GUI que el registro se guardó bien
    if "status_available" in handlers:
        handlers["status_available"](whale_id)

    # limpiar formulario
    if "clear_forms" in handlers:
        if whale_id == "A":
            handlers["clear_forms"]["A"]()
        else:
            handlers["clear_forms"]["B"]()

    # REFRESCAR TABLA DE ÚLTIMOS REGISTROS
    if "refresh_last_records" in handlers:
        handlers["refresh_last_records"]()

def update_record_field_handler(db_id, gui_field_name, new_value):
    database.update_record_field(db_id, gui_field_name, new_value)

def fetch_records_by_date_handler(start_date, end_date):
    return database.get_records_by_date(start_date, end_date)

def get_current_position_handler(whale_id):
    return gps.get_current_position(whale_id)
    # return "0.000000, 0.000000" 

def configure_gps_handler(config_dict):
    """
    Guarda configuración de GPS recibida desde la GUI.
    config_dict es algo tipo:
    {
        "port": "COM3",
        "baudrate": 4800,
        "use_mock": True/False
    }
    """
    gps.save_config(config_dict)

# --------------------- CLASE APP --------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # aplicar estilos ttk (botones redondeados, colores, etc.)
        # init_styles(self)

        # init ventana base
        self.title("Whale System - Inicio")
        self.geometry("1200x650")

        # init DB
        database.init_db()

        # init handlers compartidos
        self.handlers = handlers
        self._init_handlers()

        # contenedor para las pantallas
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # permitir que la pantalla (StartScreen / TrackingScreen)
        # se expanda para llenar todo el contenedor
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # diccionario de pantallas (StartScreen, TrackingScreen, etc.)
        self.screens = {}

        # crear pantallas y mostrar la de inicio
        self.show_screen("start")

    def _init_handlers(self):
        self.handlers["save_whale"] = save_whale_handler
        self.handlers["fetch_last_records"] = fetch_last_records_handler
        self.handlers["update_record_field"] = update_record_field_handler
        self.handlers["get_current_position"] = get_current_position_handler
        self.handlers["fetch_records_by_date"] = fetch_records_by_date_handler
        self.handlers["delete_records"] = database.delete_records
        self.handlers["backup_db"] = database.backup_database
        self.handlers["configure_gps"] = configure_gps_handler
        # database.debug_print_all_records()

        # si alguna pantalla quiere acceder a la app
        self.handlers["app"] = self

    def show_screen(self, name):
        """Muestra la pantalla 'start' o 'tracking'."""
        # si ya existe, solo la traemos al frente
        if name in self.screens:
            if name == "start":
                self.geometry("1200x650")
                self.title("Whale Tracking System")
            elif name == "tracking":
                self.geometry("1200x650")
                self.title("Whale Tracking System")
            elif name == "logs":
                self.geometry("1200x650")
                self.title("Whale Tracking System")
            elif name == "config":
                self.geometry("1200x650")
                self.title("Whale Tracking System")
            self.screens[name].tkraise()
            return

        # si no existe, la creamos
        if name == "start":
            self.geometry("1200x650")
            self.title("Whale Tracking System")
            frame = StartScreen(self.container, self, self.handlers)

        elif name == "tracking":
            # cuando pases a tracking, ajustas tamaño
            self.geometry("1200x650")
            self.title("Whale Tracking System")
            frame = TrackingScreen(self.container, self, self.handlers)

        elif name == "logs":
            self.geometry("1200x650")
            self.title("Tracking History")
            frame = LogsScreen(self.container, self, self.handlers)

        elif name == "config":
            self.geometry("1200x650")
            self.title("GPS Configuration")
            frame = ConfigScreen(self.container, self, self.handlers)
        else:
            raise ValueError(f"Pantalla desconocida: {name}")

        frame.grid(row=0, column=0, sticky="nsew")
        self.screens[name] = frame
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
