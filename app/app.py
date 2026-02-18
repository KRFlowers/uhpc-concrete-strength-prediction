"""
UHPC Compressive Strength App — Entry Point

Defines the multi-page navigation using st.navigation / st.Page.
Run with: streamlit run app/app.py
"""

import streamlit as st

# --- Page config ---
# Set the browser tab title, icon, and page layout

st.set_page_config(
    page_title="UHPC Strength Predictor",
    page_icon="🏗️",
    layout="centered",
)

# --- Navigation ---
# Define the two pages and let Streamlit handle routing

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
