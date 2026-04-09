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
    """Given lat/lon (WGS84 degrees), return dict with cuenca/subcuenca/subsubcuenca info.

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
        import geopandas as gpd
    except ImportError:
        return result

    # Create point in WGS84 (EPSG:4326)
    point_wgs84 = gpd.GeoDataFrame(
        geometry=[Point(lon, lat)], crs="EPSG:4326"
    )

    def _reproject_point(gdf_target):
        """Reproject the WGS84 point to match the target GeoDataFrame's CRS."""
        if gdf_target.crs and gdf_target.crs != point_wgs84.crs:
            return point_wgs84.to_crs(gdf_target.crs).geometry.iloc[0]
        return point_wgs84.geometry.iloc[0]

    def _find_containing(gdf, tolerance=500):
        """Find the polygon that contains the point, or the nearest within tolerance (meters)."""
        if gdf is None:
            return None
        pt = _reproject_point(gdf)
        # First: exact containment
        mask = gdf.geometry.contains(pt)
        if mask.any():
            return gdf[mask].iloc[0]
        # Fallback: nearest polygon within tolerance meters
        distances = gdf.geometry.distance(pt)
        min_dist = distances.min()
        if min_dist <= tolerance:
            return gdf.iloc[distances.idxmin()]
        return None

    # Search subsubcuencas first (most specific)
    gdf_ssc = _load_gdf(_SUBSUBCUENCAS_SHP)
    match = _find_containing(gdf_ssc)
    if match is not None:
        result["cuenca_cod"]        = str(match.get("COD_CUEN", "")).strip()
        result["subcuenca_cod"]     = str(match.get("COD_SUBC", "")).strip()
        result["subsubcuenca_cod"]  = str(match.get("COD_SSUBC", "")).strip()
        result["subsubcuenca_nombre"] = str(match.get("NOM_SSUBC", "")).strip()

    # Get cuenca name
    if result["cuenca_cod"]:
        gdf_c = _load_gdf(_CUENCAS_SHP)
        if gdf_c is not None:
            m = gdf_c[gdf_c["COD_CUEN"].str.strip() == result["cuenca_cod"]]
            if len(m) > 0:
                result["cuenca_nombre"] = str(m.iloc[0].get("NOM_CUEN", "")).strip()

    # Get subcuenca name
    if result["subcuenca_cod"]:
        gdf_s = _load_gdf(_SUBCUENCAS_SHP)
        if gdf_s is not None:
            m = gdf_s[gdf_s["COD_SUBC"].str.strip() == result["subcuenca_cod"]]
            if len(m) > 0:
                result["subcuenca_nombre"] = str(m.iloc[0].get("NOM_SUBC", "")).strip()

    # Fallback: try at cuenca level if subsubcuenca search returned nothing
    if not result["cuenca_cod"]:
        gdf_c = _load_gdf(_CUENCAS_SHP)
        match = _find_containing(gdf_c)
        if match is not None:
            result["cuenca_cod"]    = str(match.get("COD_CUEN", "")).strip()
            result["cuenca_nombre"] = str(match.get("NOM_CUEN", "")).strip()

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

    # Store identifiers
    data["cuenca_cod"]          = result.get("cuenca_cod", "")
    data["cuenca_nombre"]       = result.get("cuenca_nombre", "")
    data["subcuenca_cod"]       = result.get("subcuenca_cod", "")
    data["subcuenca_nombre"]    = result.get("subcuenca_nombre", "")
    data["subsubcuenca_cod"]    = result.get("subsubcuenca_cod", "")
    data["subsubcuenca_nombre"] = result.get("subsubcuenca_nombre", "")

    # Wikipedia links for all levels
    for level in ["cuenca", "subcuenca", "subsubcuenca"]:
        nombre = result.get(f"{level}_nombre")
        if nombre:
            data[f"{level}_wiki_link"] = wikipedia_link(nombre)

    # Wikipedia summary: fetch main cuenca first (most relevant for report)
    cuenca_nombre = result.get("cuenca_nombre")
    if cuenca_nombre and not data.get("cuenca_wiki_summary"):
        wiki = wikipedia_summary(cuenca_nombre)
        if wiki:
            data["cuenca_wiki_summary"] = wiki
            data["cuenca_wiki_source"]  = cuenca_nombre

    # Also fetch subcuenca and subsubcuenca summaries independently
    for level in ["subcuenca", "subsubcuenca"]:
        nombre = result.get(f"{level}_nombre")
        key    = f"{level}_wiki_summary"
        if nombre and not data.get(key):
            wiki = wikipedia_summary(nombre)
            if wiki:
                data[key] = wiki

    return result

