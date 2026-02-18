"""
Strength Predictor Page

Lets users define a UHPC mix design via sidebar sliders and predicts
compressive strength using the trained XGBoost model. SHAP values
explain which features drive the prediction.
"""

# --- Imports ---
# WHAT: Load external libraries and shared app utilities
# WHY: streamlit builds the web interface, pandas handles data,
#      shap explains predictions. Shared imports (from shared.py)
#      provide constants and helpers used across both pages.

import streamlit as st
import pandas as pd
import shap

from shared import (
    FEATURE_CONFIG,
    load_model,
    load_training_data,
    display_uhpc_metric,
    display_shap_table,
)


# --- Load model ---
# WHAT: Load the saved model from disk
# WHY: If the model file is missing, st.stop() halts the app with a clear
#      error message instead of crashing with an unreadable traceback

try:
    model, feature_names = load_model()
except FileNotFoundError:
    st.error(
        "Model file not found. Run notebook 02 to generate the model artifacts."
    )
    st.stop()


# --- Header ---
# WHAT: Display the page title and introductory description
# WHY: Orients the user — tells them what this page does and where to start

st.title("UHPC Compressive Strength Predictor")
st.markdown(
    "Predictions powered by the XGBoost model trained in "
    "[notebook 02](https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/02_model_development.ipynb). "
    "Adjust the sliders in the sidebar to define a mix design."
)


# --- Sidebar inputs ---
# WHAT: Build one slider per feature in the sidebar
# WHY: The loop reads from FEATURE_CONFIG so the sidebar is driven by data,
#      not hardcoded — adding/removing a feature only requires editing the dict

st.sidebar.header("Mix Design Inputs")
st.sidebar.markdown("Adjust values to define a UHPC mix design.")

input_values = {}
for feature in feature_names:
    label, unit, min_val, max_val, default, step, help_text = FEATURE_CONFIG[feature]
    input_values[feature] = st.sidebar.slider(
        f"{label} ({unit})",
        min_value=min_val, max_value=max_val,
        value=default, step=step, help=help_text,
    )

# WHAT: Add a reset button to the sidebar
# WHY: st.rerun() clears all slider state back to defaults without
#      the user having to manually reset each slider
if st.sidebar.button("Reset to Defaults"):
    st.rerun()


# --- Prediction ---
# WHAT: Convert slider values to a DataFrame and run model.predict()
# WHY: The model expects a DataFrame with columns matching the training
#      features — a dict wrapped in a list creates a single-row DataFrame

input_df = pd.DataFrame([input_values])
prediction = model.predict(input_df)[0]

# WHAT: Display three metric cards side by side
# WHY: Gives the user a quick summary — prediction, UHPC classification,
#      and model accuracy — without scrolling
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Predicted Compressive Strength",
        value=f"{prediction:.1f} MPa",
    )

with col2:
    # WHAT: UHPC classification metric with correct color logic
    # WHY: display_uhpc_metric always uses delta_color="normal" so the
    #      sign of the delta determines the color (green = above, red = below)
    display_uhpc_metric(prediction)

with col3:
    # WHAT: Show the model's test-set accuracy as a static metric
    # WHY: Gives the user confidence in the prediction — update these
    #      values if the model is retrained with different results
    st.metric(
        label="Model Performance",
        value="RMSE 5.93 MPa",
        help="XGBoost (tuned via GridSearchCV) from notebook 02. "
             "RMSE 5.93 MPa, R² = 0.978 on held-out test set.",
    )

# WHAT: Cross-link to the Observation Explorer page
# WHY: Right-aligned so it reads as secondary navigation — discoverable
#      without competing with the primary metrics above
_, link_col = st.columns([1.7, 1])
with link_col:
    st.page_link(
        "pages/observation_explorer.py",
        label="Explore individual observations",
        icon=":material/search:",
    )

st.divider()


# --- Feature Importance (SHAP) ---
# WHAT: Use SHAP TreeExplainer to calculate per-feature impact values
# WHY: TreeExplainer is exact (not approximate) for tree-based models and
#      shows how much each feature pushed the prediction above or below
#      the model's average prediction (the base value)

st.subheader("Feature Impact on This Mix Design")
st.markdown(
    "SHAP values below show how much each feature increases or decreases "
    "the predicted strength."
)

# WHAT: Load the training data and create the SHAP explainer
# WHY: TreeExplainer needs the training data as background to compute
#      the base value (average prediction) that SHAP values are relative to
X_train = load_training_data()
explainer = shap.TreeExplainer(model, data=X_train)
shap_values = explainer(input_df)

# WHAT: Render the SHAP impact table sorted by absolute impact
# WHY: display_shap_table handles formatting and sorting — the user sees
#      which features had the biggest effect on this mix's predicted strength
display_shap_table(shap_values.values[0], feature_names, input_values)


# --- About (collapsed by default) ---
# WHAT: Add a collapsible section with model and dataset details
# WHY: Keeps the main page clean while making project context available
#      for anyone who wants to understand how the model was built

with st.expander("About This Tool"):
    st.markdown("""
This app is part of the [UHPC Compressive Strength Prediction](https://github.com/KRFlowers/uhpc-concrete-strength-prediction) project.
It loads the trained model directly from the project's saved artifacts — predictions
reflect the exact model built in the analysis notebooks.

**Model:** XGBoost (tuned via GridSearchCV)
- RMSE: 5.93 MPa on held-out test set
- R²: 0.978
- Trained on 633 samples, tested on 159 samples

**Dataset:** 810 UHPC mix designs (792 after cleaning) from
Kashem et al. (2023), Mendeley Data.

**Features:** 13 mix design variables including cement, water, aggregate,
supplementary cementitious materials, fiber, and curing conditions.

**Interpretation:** SHAP (TreeExplainer) provides feature-level explanations
for each prediction.

**Limitations:**
- Predictions are based on patterns in the training data and should not
  replace laboratory testing for structural applications
- The model has not been validated on external datasets
- Input values outside the training data range may produce unreliable predictions
    """)


# --- Footer ---
# WHAT: Display a disclaimer caption at the bottom of the page
# WHY: Reminds users this is for exploratory use — not a substitute
#      for laboratory testing in structural applications

st.divider()
st.caption(
    "UHPC Compressive Strength Predictor | "
    "Built on the XGBoost model from notebook 02 | "
    "For exploratory use only"
)
