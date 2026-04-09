"""Utilidades geográficas v4.0 — Nominatim + Open-Meteo + retry logic."""
import json
import math
import time
from datetime import datetime, date

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

NOMINATIM_URL       = "https://nominatim.openstreetmap.org/search"
OPENMETEO_URL       = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_ARC_URL   = "https://archive-api.open-meteo.com/v1/archive"
HEADERS = {"User-Agent": "LivLin-IndagacionRegenerativa/4.0 (contacto@livlin.cl)"}
MONTHS_ES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]


def geocode_address(address: str, retries: int = 3) -> dict | None:
    """Geocodifica una dirección con reintentos automáticos y fallbacks."""
    if not REQUESTS_OK or not address.strip():
        return None
    
    # Clean up address for better matching
    addr_clean = address.strip()
    
    # Try 1: exact address
    result = _nominatim_query(addr_clean)
    if result:
        return result
    
    # Try 2: add country hint if not present
    if "chile" not in addr_clean.lower() and "," not in addr_clean:
        result = _nominatim_query(addr_clean + ", Chile")
        if result:
            return result
    
    # Try 3: simplify (remove apt/depto number, keep street+city)
    parts = [p.strip() for p in addr_clean.split(",") if p.strip()]
    if len(parts) >= 2:
        simplified = ", ".join(parts[-2:])  # last 2 parts (city, country usually)
        result = _nominatim_query(simplified)
        if result:
            return result
    
    return None


def _nominatim_query(address: str, timeout: int = 10) -> dict | None:
    """Single Nominatim query with proper error handling."""
    try:
        r = requests.get(
            NOMINATIM_URL,
            params={
                "q": address,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
                "accept-language": "es",
            },
            headers=HEADERS,
            timeout=timeout,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        item = data[0]
        addr = item.get("address", {})
        return {
            "lat":          float(item["lat"]),
            "lon":          float(item["lon"]),
            "display_name": item.get("display_name", address),
            "country":      addr.get("country", ""),
            "city":         addr.get("city", addr.get("town", addr.get(
                            "village", addr.get("municipality", "")))),
            "state":        addr.get("state", ""),
            "postcode":     addr.get("postcode", ""),
        }
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception:
        return None


def get_weather_now(lat: float, lon: float) -> dict | None:
    if not REQUESTS_OK:
        return None
    try:
        r = requests.get(OPENMETEO_URL, params={
            "latitude": lat, "longitude": lon,
            "current": ["temperature_2m","relative_humidity_2m","apparent_temperature",
                        "precipitation","wind_speed_10m","wind_direction_10m",
                        "weather_code","uv_index"],
            "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum",
                      "uv_index_max","sunrise","sunset"],
            "timezone": "auto", "forecast_days": 7,
        }, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_annual_climate(lat: float, lon: float) -> dict | None:
    """Estadísticas climáticas anuales desde Open-Meteo archivo histórico."""
    if not REQUESTS_OK:
        return None
    try:
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
        raw = r.json()
        daily = raw.get("daily", {})
        dates = daily.get("time", [])
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        prec  = daily.get("precipitation_sum", [])
        if not dates:
            return None
        # Aggregate by month
        monthly = {m: {"t_max":[],"t_min":[],"prec":[]} for m in range(1,13)}
        for i, d in enumerate(dates):
            try:
                m = int(d[5:7])
                if i < len(t_max) and t_max[i] is not None: monthly[m]["t_max"].append(t_max[i])
                if i < len(t_min) and t_min[i] is not None: monthly[m]["t_min"].append(t_min[i])
                if i < len(prec)  and prec[i]  is not None: monthly[m]["prec"].append(prec[i])
            except Exception:
                pass
        t_max_list, t_min_list, prec_list = [], [], []
        for m in range(1,13):
            mx = monthly[m]["t_max"]
            mn = monthly[m]["t_min"]
            pr = monthly[m]["prec"]
            # prec: sum of daily values divided by number of years to get monthly avg
            years = 5
            t_max_list.append(round(sum(mx)/len(mx), 1) if mx else None)
            t_min_list.append(round(sum(mn)/len(mn), 1) if mn else None)
            prec_list.append(round(sum(pr)/years, 1) if pr else None)

        # Find key statistics
        valid_tmax = [(i, v) for i, v in enumerate(t_max_list) if v is not None]
        valid_tmin = [(i, v) for i, v in enumerate(t_min_list) if v is not None]
        valid_prec = [(i, v) for i, v in enumerate(prec_list) if v is not None]

        mes_caluroso = MONTHS_ES[max(valid_tmax, key=lambda x: x[1])[0]] if valid_tmax else None
        mes_frio     = MONTHS_ES[min(valid_tmin, key=lambda x: x[1])[0]] if valid_tmin else None
        t_max_media  = round(sum(v for _,v in valid_tmax)/len(valid_tmax), 1) if valid_tmax else None
        t_min_media  = round(sum(v for _,v in valid_tmin)/len(valid_tmin), 1) if valid_tmin else None

        # Annual precipitation = sum of monthly averages
        prec_anual = round(sum(v for v in prec_list if v), 0) if prec_list else None

        # Absolute max/min from last year
        abs_max = max((v for v in t_max if v is not None), default=None)
        abs_min = min((v for v in t_min if v is not None), default=None)

        return {
            "months":               MONTHS_ES,
            "t_max":                t_max_list,
            "t_min":                t_min_list,
            "prec":                 prec_list,
            "mes_mas_caluroso":     mes_caluroso,
            "mes_mas_frio":         mes_frio,
            "t_max_media":          t_max_media,
            "t_min_media":          t_min_media,
            "prec_anual":           prec_anual,
            "abs_max_ultimo_anio":  round(abs_max, 1) if abs_max is not None else None,
            "abs_min_ultimo_anio":  round(abs_min, 1) if abs_min is not None else None,
            "anio_referencia":      end_year,
        }
    except Exception:
        return None


def get_solar_data(lat: float, lon: float) -> dict | None:
    if not REQUESTS_OK:
        return None
    try:
        r = requests.get(OPENMETEO_URL, params={
            "latitude": lat, "longitude": lon,
            "daily": ["shortwave_radiation_sum","sunshine_duration"],
            "timezone": "auto", "forecast_days": 7,
        }, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_lunar_phase() -> dict:
    """Calcula la fase lunar actual. Returns dict with phase_name, icon, phase_frac."""
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
        0:"Cielo despejado", 1:"Mayormente despejado", 2:"Parcialmente nublado",
        3:"Nublado", 45:"Niebla", 48:"Niebla con escarcha",
        51:"Llovizna ligera", 53:"Llovizna moderada", 55:"Llovizna densa",
        61:"Lluvia ligera", 63:"Lluvia moderada", 65:"Lluvia intensa",
        71:"Nieve ligera", 73:"Nieve moderada", 75:"Nieve intensa",
        80:"Chubascos", 81:"Chubascos moderados", 82:"Chubascos intensos",
        95:"Tormenta",
    }
    return codes.get(code, f"Código #{code}")


def wind_direction_label(deg: float) -> str:
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
            "S","SSO","SO","OSO","O","ONO","NO","NNO"]
    return dirs[round(deg / 22.5) % 16]


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
        panel_kwh   = [round(v * 0.1 * 0.8, 2) if v else None for v in monthly_avg]
        return {
            "months": MONTHS_ES,
            "monthly_kwh_m2": monthly_avg,
            "annual_avg_kwh_m2": annual_avg,
            "panel_100w_kwh_day": panel_kwh,
        }
    except Exception:
        return None


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
