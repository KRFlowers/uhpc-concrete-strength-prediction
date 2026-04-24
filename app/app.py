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
    "This tool adds interactive access to the ***UHPC Concrete Strength "
    "Prediction analysis***."
)
st.sidebar.markdown(
    "It allows **browsing the 792 training mixes** to see predicted "
    "compressive strength, SHAP-based feature impact, and a cradle-to-gate CO₂ "
    "estimate. It also allows **designing a custom mix** to review the same outputs."
)
st.sidebar.markdown(
    "It uses the tuned XGBoost model from the analysis "
    "([notebook 02]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/02_model_development.ipynb), "
    "RMSE 5.93 MPa on held-out test data)."
)

st.sidebar.markdown("### Limitations")
st.sidebar.markdown(
    "This app is a prototype for experimental use. Outputs should be validated "
    "against domain expertise and materials science literature."
)

st.sidebar.markdown("### CO₂ Emissions (Methodology & Assumptions)")
st.sidebar.markdown(
    "CO₂ estimates use emission factors compiled from peer-reviewed literature. "
    "Ranges reflect variability across studies. Values are for exploratory use "
    "only, not for formal assessment, reporting, or decision-making."
)
st.sidebar.markdown(
    "Sources: [docs/emission_factors_v2.md]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/docs/emission_factors_v2.md)"
)

st.sidebar.markdown("### Data & Code")
st.sidebar.markdown(
    "[GitHub repository]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction)"
)

# Hide  Streamlit sidebar entirely; all inputs live in-tab.
#st.html(
#    """
 #   <style>
#      section[data-testid="stSidebar"] { display: none; }
#      button[data-testid="stSidebarCollapsedControl"] { display: none; }
#    </style>
#    """
#)

# Render shared header and caption.
st.title("UHPC Strength Prediction Tool")

#st.markdown(
 #   "Interactive interface for the "
  #  "[UHPC Concrete Strength Prediction analysis]"
  #  "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction). "
  #  "Allows browsing the initial 792 mix designs for strength and feature importance, "
  #  "as well as defining custom concrete mixes and reviewing predicted strength."
# ) 

# Render top tabs and call each page's render() function within its tab.
explorer_tab, predictor_tab = st.tabs([
    "Dataset Explorer",
    "Strength Predictor",
])

with explorer_tab:
    render_explorer()

with predictor_tab:
    render_predictor()
