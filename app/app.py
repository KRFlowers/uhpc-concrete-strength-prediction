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
# Hide Streamlit's auto-generated page nav at the top of the sidebar,
# but keep the sidebar itself so our Instructions/Data blocks still show.
st.html(
    """
    <style>
      div[data-testid="stSidebarNav"] { display: none; }
    </style>
    """
)

# Sidebar: about, disclaimer, and repo link
st.sidebar.markdown("### About This Tool")
st.sidebar.markdown(
    "This tool is a companion to the "
    "[UHPC Concrete Strength Prediction analysis]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction). "
    "It uses the tuned XGBoost model trained in [notebook 02]"
    "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/02_model_development.ipynb). "
    "You can browse the 792 mix designs used to train the model, or define "
    "your own mix in the Strength Predictor. Both views show the predicted "
    "strength alongside each feature's impact on that prediction."
)

st.sidebar.markdown("### Disclaimer")
st.sidebar.markdown(
    "Research prototype — predictions are exploratory only. The tool doesn't "
    "encode materials-science domain knowledge and isn't a substitute for "
    "expert judgment or laboratory testing. Not for use in production mix "
    "design or structural applications."
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
