from tkinter import messagebox
from gui import run_gui
import database

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

def get_current_position_handler(whale_id):
    # aquí luego podrás conectar con GPS, NMEA, o lo que uses
    return "N00°00.000', W000°00.000'"  # ejemplo

def main():
    database.init_db()

    # main rellena handlers con lo que la GUI necesitará llamar
    handlers["save_whale"] = save_whale_handler
    handlers["fetch_last_records"] = fetch_last_records_handler
    handlers["update_record_field"] = update_record_field_handler  
    handlers["get_current_position"] = get_current_position_handler
    # database.debug_print_all_records()

    run_gui(handlers)

if __name__ == "__main__":
    main()