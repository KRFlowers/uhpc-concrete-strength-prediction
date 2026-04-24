"""
UHPC Strength Prediction Tool

Renders a shared header and top tabs; each tab calls the page module's render().
"""

# Import modules
import streamlit as st
from pages.observation_explorer import render as render_explorer
from pages.strength_predictor import render as render_predictor


# Set page config and hide sidebar; all inputs live in-tab.
st.set_page_config(
    page_title="UHPC Concrete Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Sidebar styling: hide Streamlit's auto-page nav, and shrink text for density.
st.html(
    """
    <style>
      /* Hide Streamlit's auto-generated page nav at the top of the sidebar */
      div[data-testid="stSidebarNav"] { display: none; }

      /* Shrink sidebar body text and tighten line height */
      section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
      section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] li {
        font-size: 0.85rem;
        line-height: 1.35;
      }
      /* Shrink sidebar H3 section headers */
      section[data-testid="stSidebar"] h3 {
        font-size: 1.05rem;
      }
    </style>
    """
)

# Sidebar: about, limitations, CO2 methodology, repo link
st.sidebar.markdown("### About this Tool")
st.sidebar.markdown(
    "This tool is part of the **UHPC Concrete Strength Prediction** project that enables interactive access to its features."
)
st.sidebar.markdown(
    "**Dataset Explorer** allows browsing the 792 training mixes to see predicted "
    "compressive strength, SHAP feature impact, and cradle-to-gate CO₂ emissions."
)

st.sidebar.markdown(
    "**Strength Predictor** allows designing custom mixes to review the same three outputs."
)

st.sidebar.markdown("### Limitations")
st.sidebar.markdown(
    "This app is a prototype for experimental use. Outputs should be validated "
    "against domain expertise and materials science literature."
)

#st.sidebar.markdown("### CO₂ Emissions (Methodology & Assumptions)")
st.sidebar.markdown(
    "CO₂ estimates use emission factors compiled from peer-reviewed literature. "
    "Ranges reflect variability across studies and are for exploratory use only. "
    "Sources: [docs/emission_factors_v2.md]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/docs/emission_factors_v2.md)"
)

st.sidebar.markdown("### Data & Code")
st.sidebar.markdown(
    "The app loads artifacts from the original analysis: the tuned XGBoost model "
    "([notebook 02]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/02_model_development.ipynb), "
    "RMSE 5.93 MPa on held-out test data) and the SHAP TreeExplainer from "
    "[notebook 03]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/03_model_interpretation.ipynb), "
    "enabling prediction reproducibility."
)
st.sidebar.markdown(
    "[GitHub repository]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction)"
)


# Render shared header and caption.
st.title("UHPC Strength Prediction Tool")


# Render top tabs and call each page's render() function within its tab.
explorer_tab, predictor_tab = st.tabs([
    "Dataset Explorer",
    "Strength Predictor",
])

with explorer_tab:
    render_explorer()

with predictor_tab:
    render_predictor()
