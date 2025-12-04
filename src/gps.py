import json
import asyncio
from pathlib import Path
from typing import Optional, Dict

# Intentamos importar winrt (para el sensor GNSS de Windows)
try:
    from winrt.windows.devices.geolocation import Geolocator
except ImportError:
    Geolocator = None

# Archivo donde guardamos la configuración del GPS
CONFIG_PATH = Path(__file__).resolve().parent / "gps_config.json"

# Configuración por defecto
DEFAULT_CONFIG = {
    "use_mock": True,     # True = modo simulado, False = usar GNSS real
}


class GPSNotAvailable(Exception):
    """Excepción para indicar que no se pudo usar el GPS real."""
    pass


def load_config() -> Dict:
    """Carga configuración de gps_config.json o devuelve DEFAULT_CONFIG."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(data)
        return cfg
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict) -> None:
    """Guarda configuración en gps_config.json."""
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(config)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ------------------ MODO SIMULADO ------------------ #

def _get_mock_position(whale_id: Optional[str] = None) -> str:
    """
    Devuelve coordenadas simuladas.
    Puedes ajustarlas a tu zona de estudio real.
    """
    if whale_id == "A":
        return "27.500000, -112.000000"
    elif whale_id == "B":
        return "27.510000, -112.010000"
    else:
        return "27.505000, -112.005000"


# ------------------ MODO REAL (GNSS) ------------------ #

async def _get_location_async(timeout_sec: float = 10.0):
    """
    Usa el sensor de ubicación de Windows (GNSS) para obtener lat/lon.
    """
    if Geolocator is None:
        raise GPSNotAvailable(
            "La librería 'winrt' no está instalada. "
            "Instala con: pip install winrt"
        )

    locator = Geolocator()

    try:
        pos = await asyncio.wait_for(locator.get_geoposition_async(), timeout=timeout_sec)
    except asyncio.TimeoutError:
        raise GPSNotAvailable("Tiempo de espera agotado esperando fix de GPS.")

    coord = pos.coordinate.point.position
    return coord.latitude, coord.longitude


# ------------------ API PÚBLICA USADA POR LA APP ------------------ #

def get_current_position(whale_id: Optional[str] = None) -> str:
    """
    Devuelve 'lat, lon' como string.

    - Si use_mock=True  -> devuelve posiciones simuladas.
    - Si use_mock=False -> intenta usar el sensor GNSS real.
    """
    cfg = load_config()

    # ----- MODO SIMULADO -----
    if cfg.get("use_mock", True):
        return _get_mock_position(whale_id)

    # ----- MODO REAL (GNSS) -----
    try:
        lat, lon = asyncio.run(_get_location_async())
        return f"{lat:.6f}, {lon:.6f}"
    except Exception as e:
        print("Error leyendo GPS real:", e)
        return "GPS_ERROR"


def test_connection(config: Optional[Dict] = None):
    """
    Función pensada para tu ConfigScreen:
    Prueba que se pueda obtener una posición REAL (GNSS).
    Ignoramos 'config' porque con el sensor GNSS no usamos puerto COM.
    """
    lat, lon = asyncio.run(_get_location_async(timeout_sec=10.0))
    return lat, lon
