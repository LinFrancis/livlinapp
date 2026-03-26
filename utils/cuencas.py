"""utils/cuencas.py -- Identificacion de cuenca, subcuenca y subsubcuenca
a partir de coordenadas geograficas usando shapefiles BNA Chile.

Requiere: geopandas, shapely (en requirements.txt).
Los shapefiles se incluyen en data/cuencas/.
"""
import os
from pathlib import Path

_BASE = Path(__file__).parent.parent / "data" / "cuencas"
_CUENCAS_SHP = _BASE / "Cuencas_BNA" / "Cuencas_BNA.shp"
_SUBCUENCAS_SHP = _BASE / "SubcuencasBNA" / "Subcuencas_BNA.shp"
_SUBSUBCUENCAS_SHP = _BASE / "SubsubcuencasBNA" / "Subsubcuencas_BNA.shp"

# Cache loaded GeoDataFrames
_cache = {}


def _load_gdf(path):
    """Load a GeoDataFrame from shapefile, with caching."""
    key = str(path)
    if key not in _cache:
        try:
            import geopandas as gpd
            _cache[key] = gpd.read_file(str(path))
        except Exception as e:
            print(f"[cuencas] Error loading {path}: {e}")
            _cache[key] = None
    return _cache[key]


def identificar_cuenca(lat, lon):
    """Given lat/lon, return dict with cuenca/subcuenca/subsubcuenca info.

    Returns dict with keys:
      cuenca_cod, cuenca_nombre,
      subcuenca_cod, subcuenca_nombre,
      subsubcuenca_cod, subsubcuenca_nombre
    All values are strings or None if not found.
    """
    result = {
        "cuenca_cod": None, "cuenca_nombre": None,
        "subcuenca_cod": None, "subcuenca_nombre": None,
        "subsubcuenca_cod": None, "subsubcuenca_nombre": None,
    }

    try:
        from shapely.geometry import Point
    except ImportError:
        return result

    point = Point(lon, lat)  # shapely uses (x=lon, y=lat)

    # Search subsubcuencas first (most specific)
    gdf = _load_gdf(_SUBSUBCUENCAS_SHP)
    if gdf is not None:
        for _, row in gdf.iterrows():
            if row.geometry and row.geometry.contains(point):
                result["cuenca_cod"] = str(row.get("COD_CUEN", "")).strip()
                result["subcuenca_cod"] = str(row.get("COD_SUBC", "")).strip()
                result["subsubcuenca_cod"] = str(row.get("COD_SSUBC", "")).strip()
                result["subsubcuenca_nombre"] = str(row.get("NOM_SSUBC", "")).strip()
                break

    # Get cuenca name
    if result["cuenca_cod"]:
        gdf_c = _load_gdf(_CUENCAS_SHP)
        if gdf_c is not None:
            match = gdf_c[gdf_c["COD_CUEN"].str.strip() == result["cuenca_cod"]]
            if len(match) > 0:
                result["cuenca_nombre"] = str(match.iloc[0].get("NOM_CUEN", "")).strip()

    # Get subcuenca name
    if result["subcuenca_cod"]:
        gdf_s = _load_gdf(_SUBCUENCAS_SHP)
        if gdf_s is not None:
            match = gdf_s[gdf_s["COD_SUBC"].str.strip() == result["subcuenca_cod"]]
            if len(match) > 0:
                result["subcuenca_nombre"] = str(match.iloc[0].get("NOM_SUBC", "")).strip()

    # If subsubcuenca search failed, try cuenca level
    if not result["cuenca_cod"]:
        gdf_c = _load_gdf(_CUENCAS_SHP)
        if gdf_c is not None:
            for _, row in gdf_c.iterrows():
                if row.geometry and row.geometry.contains(point):
                    result["cuenca_cod"] = str(row.get("COD_CUEN", "")).strip()
                    result["cuenca_nombre"] = str(row.get("NOM_CUEN", "")).strip()
                    break

    return result


def wikipedia_link(nombre):
    """Return Wikipedia search URL for a cuenca name."""
    if not nombre:
        return None
    import urllib.parse
    query = urllib.parse.quote(nombre)
    return f"https://es.wikipedia.org/wiki/Special:Search?search={query}&go=Go"


def wikipedia_summary(query, lang="es"):
    """Fetch Wikipedia summary for a query. Returns string or None."""
    if not query:
        return None
    try:
        import requests
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": query,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
        }
        response = requests.get(url, params=params, timeout=8)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))
        extract = page.get("extract", "")
        if extract and len(extract) > 30:
            # Truncate to reasonable length
            if len(extract) > 600:
                extract = extract[:600] + "..."
            return extract
    except Exception:
        pass
    return None


def get_cuenca_info(data):
    """Main entry point: identify cuenca from visit data coordinates.
    Stores results in data dict and returns the cuenca result dict."""
    lat = data.get("geo_lat")
    lon = data.get("geo_lon")

    if not lat or not lon:
        return None

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return None

    result = identificar_cuenca(lat, lon)

    # Store in data
    data["cuenca_cod"] = result.get("cuenca_cod", "")
    data["cuenca_nombre"] = result.get("cuenca_nombre", "")
    data["subcuenca_cod"] = result.get("subcuenca_cod", "")
    data["subcuenca_nombre"] = result.get("subcuenca_nombre", "")
    data["subsubcuenca_cod"] = result.get("subsubcuenca_cod", "")
    data["subsubcuenca_nombre"] = result.get("subsubcuenca_nombre", "")

    # Try to get Wikipedia summary for the most specific level
    for key in ["subsubcuenca_nombre", "subcuenca_nombre", "cuenca_nombre"]:
        nombre = result.get(key)
        if nombre:
            wiki = wikipedia_summary(nombre)
            if wiki:
                data["cuenca_wiki_summary"] = wiki
                data["cuenca_wiki_source"] = nombre
                break

    # Generate Wikipedia links
    for level in ["cuenca", "subcuenca", "subsubcuenca"]:
        nombre = result.get(f"{level}_nombre")
        if nombre:
            data[f"{level}_wiki_link"] = wikipedia_link(nombre)

    return result
