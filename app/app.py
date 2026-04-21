"""
UHPC Strength Prediction Tool

Renders a shared header and top tabs; each tab calls the page module's render().
"""

import streamlit as st

from pages.observation_explorer import render as render_explorer
from pages.strength_predictor import render as render_predictor


# --- Page config ---
st.set_page_config(
    page_title="UHPC Concrete Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide the (now-unused) Streamlit sidebar entirely; all inputs live in-tab.
st.html(
    """
    <style>
      section[data-testid="stSidebar"] { display: none; }
      button[data-testid="stSidebarCollapsedControl"] { display: none; }
    </style>
    """
)

# --- Header ---
st.title("UHPC Strength Prediction Tool")
st.caption(
    "Interactive interface for the "
    "[UHPC Concrete Strength Prediction analysis]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction). "
    "Allows browsing the initial 792 mix designs for strength and feature importance, "
    "as well as defining custom concrete mixes and reviewing predicted strength."
)

# --- Tabs ---
explorer_tab, predictor_tab = st.tabs([
    "Observation Explorer",
    "Strength Predictor",
])

with explorer_tab:
    render_explorer()

with predictor_tab:
    render_predictor()
