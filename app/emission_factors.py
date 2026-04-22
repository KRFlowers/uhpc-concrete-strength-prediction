"""
Cradle-to-gate (A1-A3) CO2 emission factors for UHPC mix ingredients.

Values are compiled from peer-reviewed LCA literature. See
notes/emission_factors_v2.md for full citations and methodological caveats.

Keys in EMISSION_FACTORS match the feature names in shared.FEATURE_CONFIG so
the widget can accept the same mix dict that is passed to the XGBoost model.

Intended for proof-of-concept visualization only — not for procurement,
EPD reporting, or regulatory use.
"""

# --- Emission factor table ---
# (default, low, high) in kg CO2e per kg material.
# Keys must match FEATURE_CONFIG feature names in shared.py.

EMISSION_FACTORS = {
    "cement":           (0.830,    0.740,  0.950),
    "water":            (0.000196, 0.0001, 0.0008),
    "fly_ash":          (0.009,    0.004,  0.050),
    "silica_fume":      (0.014,    0.014,  0.143),
    "nano_silica":      (1.500,    0.500,  3.000),
    "quartz_powder":    (0.0237,   0.016,  0.048),
    "limestone_powder": (0.017,    0.007,  0.032),
    "slag":             (0.052,    0.019,  0.083),
    "superplasticizer": (0.944,    0.720,  2.200),
    # Aggregate — UHPC typically uses only fine aggregate (quartz sand).
    "aggregate":        (0.005,    0.003,  0.026),
    # Fiber — the widget chooses between virgin (BF-BOF) and recycled (EAF).
    "fiber_virgin":     (2.500,    1.900,  3.200),
    "fiber_recycled":   (0.900,    0.500,  1.300),
}

# FEATURE_CONFIG keys that are NOT physical material masses.
# The widget must skip these when computing emissions.
NON_MATERIAL_FEATURES = {"temperature", "age"}


# --- Public API ---

def compute_co2(mix: dict, fiber_type: str = "virgin") -> dict:
    """Compute per-m3 CO2 emissions from a mix dict.

    Parameters
    ----------
    mix : dict
        Mass of each ingredient in kg/m3. Keys match shared.FEATURE_CONFIG.
        Non-material keys (temperature, age) and unknown keys are ignored.
    fiber_type : {"virgin", "recycled"}, default "virgin"
        Which steel-fiber factor to apply to the mix["fiber"] mass.

    Returns
    -------
    dict with shape
        {
          "totals":        {"low": float, "default": float, "high": float},
          "by_ingredient": {feature_name: (low, default, high)},
          "fiber_type":    "virgin" | "recycled",
        }
        All values are in kg CO2e per m3 of concrete.
    """
    fiber_key = f"fiber_{fiber_type}"
    if fiber_key not in EMISSION_FACTORS:
        raise ValueError("fiber_type must be 'virgin' or 'recycled'")

    # Helper: return the factor tuple for a given mix key.
    # For 'fiber', substitute in the virgin/recycled variant.
    def factor_tuple(name: str):
        key = fiber_key if name == "fiber" else name
        return EMISSION_FACTORS[key]

    totals = {"low": 0.0, "default": 0.0, "high": 0.0}
    by_ingredient = {}

    for name, mass in mix.items():
        # Skip features that are not physical masses (curing temp, age)
        if name in NON_MATERIAL_FEATURES:
            continue
        # Skip keys that have no emission factor (defensive — should not happen
        # in practice, since mix is built from FEATURE_CONFIG)
        if name not in EMISSION_FACTORS and name != "fiber":
            continue
        if not mass:
            # Ingredient absent from this mix — skip to keep the output clean
            continue

        default, low, high = factor_tuple(name)
        contribution = (mass * low, mass * default, mass * high)
        by_ingredient[name] = contribution

        totals["low"] += contribution[0]
        totals["default"] += contribution[1]
        totals["high"] += contribution[2]

    return {
        "totals": totals,
        "by_ingredient": by_ingredient,
        "fiber_type": fiber_type,
    }
