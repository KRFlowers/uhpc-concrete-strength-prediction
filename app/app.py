"""
UHPC Compressive Strength App — Main Entry Point

Configures multi-page navigation via st.navigation and st.Page.
"""

import streamlit as st

# --- Page config ---
# Set the browser tab 
st.set_page_config(
    page_title="UHPC Strength Predictor",
    layout="centered",
)

# --- Navigation ---
# Define pages 
pages = [
    st.Page(
        "pages/strength_predictor.py",
        title="Strength Predictor",
        icon=":material/model_training:",
        default=True,
    ),
    st.Page(
        "pages/observation_explorer.py",
        title="Observation Explorer",
        icon=":material/search:",
    ),
]

page = st.navigation(pages)
page.run()
