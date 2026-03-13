"""Utilidades geográficas v3 — Nominatim + Open-Meteo + Solar + Lunar."""
import json
import math
from datetime import datetime, date

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

NOMINATIM_URL      = "https://nominatim.openstreetmap.org/search"
OPENMETEO_URL      = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_ARC_URL  = "https://archive-api.open-meteo.com/v1/archive"
OPENMETEO_SOLAR_URL= "https://api.open-meteo.com/v1/forecast"
HEADERS = {"User-Agent": "LivLin-IndagacionRegenerativa/3.0 (livlin@permacultura.cl)"}

MONTHS_ES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]


def geocode_address(address: str) -> dict | None:
    if not REQUESTS_OK or not address.strip():
        return None
    try:
        r = requests.get(NOMINATIM_URL,
            params={"q": address, "format": "json", "limit": 1, "addressdetails": 1},
            headers=HEADERS, timeout=8)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        item = data[0]
        addr = item.get("address", {})
        return {
            "lat": float(item["lat"]), "lon": float(item["lon"]),
            "display_name": item.get("display_name", address),
            "country": addr.get("country", ""),
            "city": addr.get("city", addr.get("town", addr.get("village", ""))),
            "state": addr.get("state", ""),
            "postcode": addr.get("postcode", ""),
        }
    except Exception:
        return None


def get_weather_now(lat: float, lon: float) -> dict | None:
    if not REQUESTS_OK:
        return None
    try:
        r = requests.get(OPENMETEO_URL, params={
            "latitude": lat, "longitude": lon,
            "current": ["temperature_2m","relative_humidity_2m","apparent_temperature",
                        "precipitation","wind_speed_10m","wind_direction_10m","weather_code","uv_index"],
            "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum",
                      "uv_index_max","sunrise","sunset"],
            "timezone": "auto", "forecast_days": 7,
        }, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_annual_climate(lat: float, lon: float) -> dict | None:
    """Obtiene estadísticas climáticas anuales desde el archivo histórico de Open-Meteo.
    Retorna medias mensuales de temperatura y precipitación acumulada."""
    if not REQUESTS_OK:
        return None
    try:
        # Usar los últimos 5 años disponibles
        end_year = date.today().year - 1
        start_year = end_year - 4
        r = requests.get(OPENMETEO_ARC_URL, params={
            "latitude": lat, "longitude": lon,
            "start_date": f"{start_year}-01-01",
            "end_date":   f"{end_year}-12-31",
            "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum",
                      "wind_speed_10m_max"],
            "timezone": "auto",
        }, headers=HEADERS, timeout=20)
        r.raise_for_status()
        data = r.json()
        if "daily" not in data:
            return None

        times   = data["daily"]["time"]
        t_max   = data["daily"].get("temperature_2m_max", [])
        t_min   = data["daily"].get("temperature_2m_min", [])
        prec    = data["daily"].get("precipitation_sum", [])
        wind    = data["daily"].get("wind_speed_10m_max", [])

        # Agregar por mes
        monthly = {m: {"t_max": [], "t_min": [], "prec": [], "wind": []} for m in range(1, 13)}
        for i, t in enumerate(times):
            try:
                m = int(t[5:7])
                if i < len(t_max) and t_max[i] is not None:
                    monthly[m]["t_max"].append(t_max[i])
                if i < len(t_min) and t_min[i] is not None:
                    monthly[m]["t_min"].append(t_min[i])
                if i < len(prec) and prec[i] is not None:
                    monthly[m]["prec"].append(prec[i])
                if i < len(wind) and wind[i] is not None:
                    monthly[m]["wind"].append(wind[i])
            except Exception:
                pass

        def avg(lst): return round(sum(lst) / len(lst), 1) if lst else None
        def total(lst): return round(sum(lst) / max(1, len(lst) / 30), 0) if lst else None  # avg monthly total

        result = {"months": MONTHS_ES, "t_max": [], "t_min": [], "prec": [], "wind": []}
        for m in range(1, 13):
            result["t_max"].append(avg(monthly[m]["t_max"]))
            result["t_min"].append(avg(monthly[m]["t_min"]))
            result["prec"].append(total(monthly[m]["prec"]))
            result["wind"].append(avg(monthly[m]["wind"]))

        # ── Extremos y meses clave ──────────────────────────────────────
        valid_tmax = [(i, v) for i, v in enumerate(result["t_max"]) if v is not None]
        valid_tmin = [(i, v) for i, v in enumerate(result["t_min"]) if v is not None]

        if valid_tmax:
            hottest_idx = max(valid_tmax, key=lambda x: x[1])[0]
            coldest_idx = min(valid_tmin, key=lambda x: x[1])[0] if valid_tmin else 0
            result["mes_mas_caluroso"] = MONTHS_ES[hottest_idx]
            result["mes_mas_frio"]     = MONTHS_ES[coldest_idx]
            result["t_max_media"]      = result["t_max"][hottest_idx]
            result["t_min_media"]      = result["t_min"][coldest_idx] if valid_tmin else None
        else:
            result["mes_mas_caluroso"] = None
            result["mes_mas_frio"]     = None
            result["t_max_media"]      = None
            result["t_min_media"]      = None

        # ── Valores absolutos del último año disponible ─────────────────
        last_year_tmax_all = [v for vals in [monthly[m]["t_max"][-365//12:] for m in range(1,13)] for v in vals]
        last_year_tmin_all = [v for vals in [monthly[m]["t_min"][-365//12:] for m in range(1,13)] for v in vals]
        result["abs_max_ultimo_anio"] = round(max(last_year_tmax_all), 1) if last_year_tmax_all else None
        result["abs_min_ultimo_anio"] = round(min(last_year_tmin_all), 1) if last_year_tmin_all else None
        result["anio_referencia"]     = end_year

        return result
    except Exception:
        return None


def get_solar_radiation(lat: float, lon: float) -> dict | None:
    """Obtiene irradiancia solar mensual (shortwave_radiation_sum) de Open-Meteo."""
    if not REQUESTS_OK:
        return None
    try:
        end_year = date.today().year - 1
        start_year = end_year - 2
        r = requests.get(OPENMETEO_ARC_URL, params={
            "latitude": lat, "longitude": lon,
            "start_date": f"{start_year}-01-01",
            "end_date":   f"{end_year}-12-31",
            "daily": ["shortwave_radiation_sum"],
            "timezone": "auto",
        }, headers=HEADERS, timeout=20)
        r.raise_for_status()
        data = r.json()
        if "daily" not in data:
            return None

        times = data["daily"]["time"]
        rad   = data["daily"].get("shortwave_radiation_sum", [])

        monthly = {m: [] for m in range(1, 13)}
        for i, t in enumerate(times):
            try:
                m = int(t[5:7])
                if i < len(rad) and rad[i] is not None:
                    monthly[m].append(rad[i])
            except Exception:
                pass

        def avg(lst): return round(sum(lst) / len(lst), 2) if lst else None

        monthly_avg = [avg(monthly[m]) for m in range(1, 13)]
        annual_avg  = round(sum(x for x in monthly_avg if x) / max(1, sum(1 for x in monthly_avg if x)), 2)

        # kWh/day for 100W panel = radiation_kWh_m2_day * 0.1 * efficiency(0.8)
        panel_kwh = [round(v * 0.1 * 0.8, 2) if v else None for v in monthly_avg]

        return {
            "months": MONTHS_ES,
            "monthly_kwh_m2": monthly_avg,
            "annual_avg_kwh_m2": annual_avg,
            "panel_100w_kwh_day": panel_kwh,
        }
    except Exception:
        return None


def get_lunar_phase() -> dict:
    """Calcula la fase lunar actual."""
    now = datetime.utcnow()
    known_new = datetime(2000, 1, 6, 18, 14)
    cycle_days = 29.53058770576
    delta = (now - known_new).total_seconds() / 86400
    phase_frac = (delta % cycle_days) / cycle_days

    if phase_frac < 0.0625:   phase_name, icon = "Luna Nueva",       "🌑"
    elif phase_frac < 0.1875: phase_name, icon = "Cuarto Creciente", "🌒"
    elif phase_frac < 0.3125: phase_name, icon = "Luna Creciente",   "🌓"
    elif phase_frac < 0.4375: phase_name, icon = "Cuarto Creciente", "🌔"
    elif phase_frac < 0.5625: phase_name, icon = "Luna Llena",       "🌕"
    elif phase_frac < 0.6875: phase_name, icon = "Cuarto Menguante", "🌖"
    elif phase_frac < 0.8125: phase_name, icon = "Luna Menguante",   "🌗"
    elif phase_frac < 0.9375: phase_name, icon = "Cuarto Menguante", "🌘"
    else:                      phase_name, icon = "Luna Nueva",       "🌑"

    days_to_full = round((0.5 - phase_frac if phase_frac < 0.5 else 1.5 - phase_frac) * cycle_days)
    return {"phase_name": phase_name, "icon": icon,
            "phase_frac": round(phase_frac * 100, 1),
            "days_to_full": abs(days_to_full)}


def wmo_weather_description(code: int) -> str:
    codes = {
        0:"Cielo despejado ☀️", 1:"Mayormente despejado 🌤️", 2:"Parcialmente nublado ⛅",
        3:"Nublado ☁️", 45:"Niebla 🌫️", 51:"Llovizna ligera 🌦️",
        61:"Lluvia ligera 🌧️", 63:"Lluvia moderada 🌧️", 65:"Lluvia intensa 🌧️",
        71:"Nieve ligera 🌨️", 80:"Chubascos 🌦️", 95:"Tormenta ⛈️",
    }
    return codes.get(code, f"Código #{code}")


def wind_direction_label(deg: float) -> str:
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSO","SO","OSO","O","ONO","NO","NNO"]
    return dirs[round(deg / 22.5) % 16]


def search_nearby_places(lat: float, lon: float, category: str, radius: int = 2000) -> list:
    """Busca lugares cercanos usando Overpass API (OpenStreetMap), sin API key."""
    if not REQUESTS_OK:
        return []
    TAG_MAP = {
        "parques":    '[leisure~"park|garden|nature_reserve"]',
        "ferias":     '[amenity~"marketplace|market"]',
        "mercados":   '[shop~"supermarket|greengrocer|farm"]',
        "huertas":    '[leisure="garden"][garden:type="community"]',
        "bibliotecas":'[amenity="library"]',
        "escuelas":   '[amenity~"school|college|university"]',
        "hospitales": '[amenity~"hospital|clinic|doctors"]',
        "plazas":     '[leisure="pitch"][sport]',
    }
    tag = TAG_MAP.get(category, '[amenity]')
    query = f"""
    [out:json][timeout:15];
    (node{tag}(around:{radius},{lat},{lon});
     way{tag}(around:{radius},{lat},{lon}););
    out center 10;
    """
    try:
        r = requests.post("https://overpass-api.de/api/interpreter",
                         data={"data": query}, timeout=15)
        r.raise_for_status()
        elements = r.json().get("elements", [])
        results = []
        for e in elements[:10]:
            name = e.get("tags", {}).get("name", "Sin nombre")
            clat = e.get("lat", e.get("center", {}).get("lat"))
            clon = e.get("lon", e.get("center", {}).get("lon"))
            if clat and clon:
                dist = round(math.sqrt((clat - lat)**2 + (clon - lon)**2) * 111320)
                results.append({"name": name, "lat": clat, "lon": clon, "dist_m": dist})
        return sorted(results, key=lambda x: x["dist_m"])
    except Exception:
        return []
