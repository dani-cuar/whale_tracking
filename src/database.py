import sqlite3
from pathlib import Path

# Ruta de la base de datos (puedes ajustarla si tienes carpeta data/)
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.db"
DB_PATH.parent.mkdir(exist_ok=True)  # crea carpeta data/ si no existe

# Mapeo GUI -> columna SQL (importante para futuro)
GUI_TO_DB = {
    "ID": "id_tag",
    "Init Pos": "init_pos",
    "Final Pos": "final_pos",
    "Time": "time_str",
    "# Sightings": "sightings",
    "Behavior": "behavior",
    "# Blows": "blows",
    "First Blow": "first_blow",
    "# Whales": "whales_count",
    "Individual (letter)": "individual_letter",
    "Initial Distance": "initial_distance",
    "# Photos": "photos_count",
    "Fluke": "fluke",
    "Shallow dive": "shallow_dive",
    "# Skin Sample": "skin_samples",
    "Feces in Trail": "feces_trail",
    "# Boats": "boats_count",
    "Boat Speed": "boat_speed",
    "WW-Whale Distance": "ww_whale_distance",
    "Engine On": "engine_on",
    "# Visibility": "visibility",
    "Hydrophone": "hydrophone",
    "Observations": "observations",
}

DB_TO_GUI = {v: k for k, v in GUI_TO_DB.items()}

def get_last_records(limit=6):
    """
    Devuelve una lista de dicts con claves de la GUI (las de `columns`):
    [{ "ID": "A", "Init Pos": "...", ... }, ...]
    """
    with get_connection() as conn:
        cur = conn.cursor()
        # seleccionamos solo las columnas que conocemos
        db_cols = list(DB_TO_GUI.keys())  # ej: ["id_tag", "init_pos", ...]
        cols_sql = ", ".join(db_cols)

        # ordenamos por created_at DESC para tener los más recientes primero
        cur.execute(
            f"""
            SELECT id, {cols_sql}
            FROM records
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = cur.fetchall()

    records = []
    for row in rows:
        db_id = row[0]          # ESTE es el id único de la BD (1,2,3,...)
        data_cols = row[1:]

        gui_dict = {"_db_id": db_id}

        for db_col, value in zip(db_cols, data_cols):
            gui_key = DB_TO_GUI.get(db_col)
            if gui_key:
                gui_dict[gui_key] = "" if value is None else str(value)

        records.append(gui_dict)

    return records

def get_records_by_date(start_date, end_date):
    """
    start_date, end_date: strings 'YYYY-MM-DD'
    Devuelve lista de dicts como get_last_records, con clave extra '_db_id'.
    """
    with get_connection() as conn:
        cur = conn.cursor()

        db_cols = list(DB_TO_GUI.keys())  # ["id_tag", "init_pos", ...]
        cols_sql = ", ".join(db_cols)

        cur.execute(
            f"""
            SELECT id, {cols_sql}
            FROM records
            WHERE date(created_at) BETWEEN date(?) AND date(?)
            ORDER BY created_at ASC, id ASC
            """,
            (start_date, end_date)
        )
        rows = cur.fetchall()

    records = []
    for row in rows:
        db_id = row[0]
        data_cols = row[1:]

        gui_dict = {"_db_id": db_id}
        for db_col, value in zip(db_cols, data_cols):
            gui_key = DB_TO_GUI.get(db_col)
            if gui_key:
                gui_dict[gui_key] = "" if value is None else str(value)
        records.append(gui_dict)

    return records

def update_record_field(db_id, gui_field_name, new_value):
    db_col = GUI_TO_DB.get(gui_field_name)
    if not db_col:
        return

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"UPDATE records SET {db_col} = ? WHERE id = ?",
            (new_value, db_id)
        )
        conn.commit()

def get_connection():
    """Devuelve una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Crea la tabla si no existe."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tag TEXT,
                init_pos TEXT,
                final_pos TEXT,
                time_str TEXT,
                sightings INTEGER,
                behavior TEXT,
                blows INTEGER,
                first_blow TEXT,
                whales_count INTEGER,
                individual_letter TEXT,
                initial_distance REAL,
                photos_count INTEGER,
                fluke TEXT,
                shallow_dive TEXT,
                skin_samples INTEGER,
                feces_trail TEXT,
                boats_count INTEGER,
                boat_speed REAL,
                ww_whale_distance REAL,
                engine_on TEXT,
                visibility TEXT,
                hydrophone TEXT,
                observations TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

def debug_print_all_records():
    """Imprime todas las filas tal cual están en la BD (sin transformar)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM records ORDER BY id ASC")
        rows = cur.fetchall()

    print("\n----- CONTENIDO DE LA TABLA records -----")
    for row in rows:
        print(row)
    print("----------------------------------------\n")
