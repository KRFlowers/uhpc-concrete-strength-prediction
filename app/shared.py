"""
Shared configuration, model/data loaders, and display helpers
for the UHPC Compressive Strength app.

Both pages (Strength Predictor and Observation Explorer) import from this
module to avoid duplicating constants, loading logic, and display code.
"""

# --- Imports ---

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


# --- Configuration ---
#Define file paths relative to the project structure


APP_DIR = Path(__file__).parent            # WHAT: Resolves to the app/ folder
PROJECT_ROOT = APP_DIR.parent              # WHAT: Resolves to the project root folder
RESULTS_DIR = PROJECT_ROOT / "data" / "results"

# Path to the trained XGBoost model saved by notebook 02

MODEL_PATH = RESULTS_DIR / "xgb_tuned_model.joblib"

# Set FHWA-defined minimum compressive strength for UHPC classification
UHPC_THRESHOLD = 150  # MPa

#  Define feature metadata used to build sidebar sliders dynamically
FEATURE_CONFIG = {
    "cement":           ("Cement",              "kg/m³", 200.0, 1300.0, 770.0, 10.0, "Primary binder (present in all mixes)"),
    "slag":             ("Slag",                "kg/m³",   0.0,  400.0,   0.0, 10.0, "Supplementary cite material (optional)"),
    "silica_fume":      ("Silica Fume",         "kg/m³",   0.0,  450.0, 144.0, 5.0,  "Supplementary binder for strength gain"),
    "limestone_powder": ("Limestone Powder",    "kg/m³",   0.0, 1100.0,   0.0, 10.0, "Filler material (optional)"),
    "quartz_powder":    ("Quartz Powder",       "kg/m³",   0.0,  400.0,   0.0, 10.0, "Fine filler (optional)"),
    "fly_ash":          ("Fly Ash",             "kg/m³",   0.0,  360.0,   0.0, 10.0, "Supplementary cementitious material (optional)"),
    "nano_silica":      ("Nano-Silica",         "kg/m³",   0.0,   50.0,   0.0, 1.0,  "Nano-scale additive (optional)"),
    "aggregate":        ("Aggregate",           "kg/m³", 400.0, 2000.0, 1104.0, 10.0, "Coarse/fine aggregate (present in all mixes)"),
    "water":            ("Water",               "kg/m³",  90.0,  275.0, 177.0, 5.0,  "Mix water (present in all mixes)"),
    "fiber":            ("Fiber",               "kg/m³",   0.0,  240.0,   0.0, 5.0,  "Reinforcing fiber (optional)"),
    "superplasticizer": ("Superplasticizer",    "kg/m³",   1.0,   60.0,  30.0, 1.0,  "Chemical admixture for workability"),
    "temperature":      ("Curing Temperature",  "°C",     20.0,  210.0,  21.0, 1.0,  "Curing temperature"),
    "age":              ("Curing Age",          "days",    1.0,  365.0,  28.0, 1.0,  "Days of curing"),
}


# --- Load model and data ---

@st.cache_resource
def load_model():
    """Load the trained XGBoost model and feature names from the saved joblib file."""
    artifacts = joblib.load(MODEL_PATH)
    return artifacts["model"], artifacts["feature_names"]


@st.cache_data
def load_training_data():
    """Load the training set — needed by SHAP as background data."""
    return pd.read_csv(RESULTS_DIR / "X_train.csv")


@st.cache_data
def load_all_observations():
    """Load all 792 observations (train + test) with actual strengths and set labels.

    Returns a single DataFrame with 13 feature columns, compressive_strength,
    and a Set column ('Train' or 'Test').
    """
    X_train = pd.read_csv(RESULTS_DIR / "X_train.csv")
    X_test = pd.read_csv(RESULTS_DIR / "X_test.csv")
    y_train = pd.read_csv(RESULTS_DIR / "y_train.csv")
    y_test = pd.read_csv(RESULTS_DIR / "y_test.csv")

    train = pd.concat([X_train, y_train], axis=1)
    train["Set"] = "Train"

    test = pd.concat([X_test, y_test], axis=1)
    test["Set"] = "Test"

    return pd.concat([train, test], ignore_index=True)


# --- Display helpers ---

def display_uhpc_metric(strength, label="UHPC Classification"):
    """Render a st.metric card for UHPC classification with correct color logic.

    Always uses delta_color='normal' so that:
      - Positive delta (above threshold) -> green
      - Negative delta (below threshold) -> red
    """
    st.metric(
        label=label,
        value="Meets UHPC" if strength >= UHPC_THRESHOLD else "Below UHPC",
        delta=f"{strength - UHPC_THRESHOLD:+.1f} MPa from threshold",
        delta_color="normal",
    )


def display_shap_table(shap_values_array, feature_names, feature_values):
    """Render the SHAP feature-impact table sorted by absolute impact.

    Parameters
    ----------
    shap_values_array : np.ndarray
        1-D array of SHAP values for a single observation.
    feature_names : list[str]
        Feature column names (model order).
    feature_values : dict or pd.Series
        Mapping of feature name -> value for the observation.
    """
    shap_df = pd.DataFrame({
        "Feature": [FEATURE_CONFIG[f][0] for f in feature_names],
        "Value": [feature_values[f] for f in feature_names],
        "Unit": [FEATURE_CONFIG[f][1] for f in feature_names],
        "SHAP Impact (MPa)": shap_values_array,
        "|Impact|": np.abs(shap_values_array),
    }).sort_values("|Impact|", ascending=False)

    st.dataframe(
        shap_df[["Feature", "Value", "Unit", "SHAP Impact (MPa)"]].style.format(
            {"Value": "{:.1f}", "SHAP Impact (MPa)": "{:+.2f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )
