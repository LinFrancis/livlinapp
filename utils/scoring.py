"""scoring.py v4.2 — todas las métricas derivadas de petalo_i_obs/ipr_* data.
Sin dependencia de fl_p* ni ipr_petalos para el radar principal.
"""
import json
from pathlib import Path

# ── Cargar pétalos desde JSON (orden canónico) ────────────────────────────────
def _load_petalos():
    jf = Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(jf, encoding="utf-8") as f:
            return json.load(f)["petalos"]
    except Exception:
        return []

# ── 7 pétalos de la Flor (Holmgren 2002) — índice canónico ────────────────────
FLOWER_DOMAINS = {
    "Administración de la Tierra y la Naturaleza": {
        "icon": "🌳", "petal_num": 1, "color": "#40916C",
        "desc": "Sistemas regenerativos: bosques comestibles, semillas, agua y agroforestería",
        "indicators": []
    },
    "Entorno Construido": {
        "icon": "🏡", "petal_num": 2, "color": "#2D9596",
        "desc": "Bioarquitectura, bioclimática, materiales naturales",
        "indicators": []
    },
    "Herramientas y Tecnología": {
        "icon": "🛠️", "petal_num": 3, "color": "#8B5E3C",
        "desc": "Tecnología apropiada, eficiencia energética, reutilización",
        "indicators": []
    },
    "Educación y Cultura": {
        "icon": "📚", "petal_num": 4, "color": "#7B61FF",
        "desc": "Educación viva, saberes locales, cultura regenerativa",
        "indicators": []
    },
    "Salud y Bienestar Espiritual": {
        "icon": "🧘", "petal_num": 5, "color": "#A67C00",
        "desc": "Prevención, medicina holística, cuidado integral",
        "indicators": []
    },
    "Finanzas y Economía": {
        "icon": "💚", "petal_num": 6, "color": "#2D6A4F",
        "desc": "Finanzas éticas, autosuficiencia, comercio justo",
        "indicators": []
    },
    "Tenencia de la Tierra y Gobernanza Comunitaria": {
        "icon": "🤝", "petal_num": 7, "color": "#1A6B6B",
        "desc": "Gobernanza colectiva, cooperativas, resolución de conflictos",
        "indicators": []
    },
}

# Canonical petal order (matches JSON index 0-6)
PETAL_ORDER = list(FLOWER_DOMAINS.keys())


def _count_to_score(n: int) -> float:
    """Map practice count to 0-5 score scale."""
    if n == 0: return 0.0
    if n == 1: return 1.0
    if n == 2: return 2.0
    if n == 3: return 3.0
    if n <= 5: return 4.0
    return 5.0


def _ipr_obs_from_data(data: dict) -> list:
    """
    Derive observed practice counts for each petal (index 0-6).
    Priority order:
    1. ipr_obs already computed and stored
    2. Count directly from petalo_i_obs keys
    """
    # Option 1: already computed
    ipr_obs = data.get("ipr_obs", [])
    if ipr_obs and len(ipr_obs) >= 7:
        return [int(x) for x in ipr_obs[:7]]

    # Option 2: count from petalo_i_obs keys
    counts = []
    for i in range(7):
        obs  = data.get(f"petalo_{i}_obs", {})
        otros = data.get(f"petalo_{i}_otros_obs", [])
        n = sum(len(v) for v in obs.values() if isinstance(v, list)) + len(otros)
        counts.append(n)
    return counts


def _ipr_tot_from_data(data: dict) -> list:
    """
    Derive total (obs + potential) practice counts for each petal.
    Priority: ipr_tot stored → compute from petalo_i keys.
    """
    ipr_tot = data.get("ipr_tot", [])
    if ipr_tot and len(ipr_tot) >= 7:
        return [int(x) for x in ipr_tot[:7]]

    counts = []
    for i in range(7):
        obs   = data.get(f"petalo_{i}_obs",     {})
        new_  = data.get(f"petalo_{i}_pot_new",  {})
        oo    = data.get(f"petalo_{i}_otros_obs", [])
        on    = data.get(f"petalo_{i}_otros_new", [])
        n = (sum(len(v) for v in obs.values()  if isinstance(v, list)) +
             sum(len(v) for v in new_.values() if isinstance(v, list)) +
             len(oo) + len(on))
        counts.append(n)
    return counts


def compute_domain_scores(data: dict) -> dict:
    """0-5 score per petal derived from IPR observed counts."""
    counts = _ipr_obs_from_data(data)
    return {PETAL_ORDER[i]: _count_to_score(counts[i])
            for i in range(7)}


def compute_domain_scores_total(data: dict) -> dict:
    """0-5 score per petal including potential (for potential radar)."""
    counts = _ipr_tot_from_data(data)
    return {PETAL_ORDER[i]: _count_to_score(counts[i])
            for i in range(7)}


def compute_wellbeing_score(data: dict) -> float:
    """Wellbeing from petal 4 (Salud y Bienestar Espiritual, index 4)."""
    counts = _ipr_obs_from_data(data)
    return _count_to_score(counts[4]) if len(counts) > 4 else 0.0


def compute_regenerative_score(data: dict) -> float:
    """Average score across all 7 petals (observed only)."""
    ds = compute_domain_scores(data)
    vals = list(ds.values())
    active = [v for v in vals if v > 0]
    if not active:
        return 0.0
    return round(sum(vals) / 7, 2)  # always divide by 7 for honest average


def score_label(score: float) -> tuple:
    if score == 0:    return "🌱 Inicio del viaje — potencial enorme por revelar", "#9E9E9E"
    if score < 1.0:   return "🌱 Semilla — el terreno está listo para regenerar", "#74C69D"
    if score < 2.0:   return "🌿 Brote — primeros pasos regenerativos en marcha", "#52B788"
    if score < 3.0:   return "🌳 Crecimiento — el espacio florece hacia la regeneración", "#40916C"
    if score < 4.0:   return "🌸 Florecimiento — espacio regenerativo sólido y activo", "#2D6A4F"
    return "🌺 Abundancia — referente vivo de regeneración", "#1B4332"


def compute_synthesis_potentials(data: dict) -> dict:
    """8 synthesis dimensions mapped from IPR data + manual overrides."""
    counts_obs = _ipr_obs_from_data(data)
    counts_tot = _ipr_tot_from_data(data)

    def _pot(manual_key, petal_idx, use_total=True):
        v = data.get(manual_key)
        if v is not None:
            try: return min(5.0, float(v))
            except (ValueError, TypeError): pass
        src = counts_tot if use_total else counts_obs
        return _count_to_score(src[petal_idx]) if petal_idx < len(src) else 0.0

    return {
        # P0 = Administración de la Tierra
        "Producción alimentaria":  _pot("sint_pot_alimentaria",  0),
        "Biodiversidad urbana":    _pot("sint_pot_biodiversidad", 0),
        "Regeneración del suelo":  _pot("sint_pot_suelo",        0),
        # P2 = Herramientas
        "Captación de agua":       _pot("sint_pot_agua",         2),
        # P3 = Educación
        "Educación ambiental":     _pot("sint_pot_educacion",    3),
        # P6 = Gobernanza
        "Bienestar comunitario":   _pot("sint_pot_bienestar",    6),
        # P5 = Finanzas
        "Economía regenerativa":   _pot("sint_pot_economia",     5),
        # P4 = Salud
        "Bienestar interior":      _pot("sint_pot_interior",     4, use_total=False),
    }
