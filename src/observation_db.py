import sqlite3
from pathlib import Path
import os
import sys
import csv

def _get_db_path() -> Path:
    # Si es ejecutable (PyInstaller)
    if getattr(sys, "frozen", False):
        app_dir = Path(os.environ["LOCALAPPDATA"]) / "WhaleTrackingSystem"
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir / "observation_points.db"

    # Desarrollo: ./data/observation_points.db en la raíz del proyecto
    project_root = Path(__file__).resolve().parent.parent  # src/.. = raíz
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "observation_points.db"


DB_PATH = _get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS observation_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                latitude TEXT,
                longitude TEXT,
                notes TEXT,
                duration_seconds INTEGER,
                created_at TEXT DEFAULT (datetime('now','localtime'))
            )
            """
        )
        conn.commit()

def insert_point(date, time, latitude, longitude, notes, duration_seconds):
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO observation_points
            (date, time, latitude, longitude, notes, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date, time, latitude, longitude, notes, duration_seconds)
        )
        conn.commit()
        return cur.lastrowid

def export_to_csv(csv_path: str):
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, date, time, latitude, longitude, notes, duration_seconds, created_at
            FROM observation_points
            ORDER BY id ASC
        """)
        rows = cur.fetchall()

    headers = ["id", "date", "time", "latitude", "longitude", "notes", "duration_seconds", "created_at"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return csv_path

def get_db_path_str():
    return str(DB_PATH)

def count_points():
    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM observation_points")
        return cur.fetchone()[0]
