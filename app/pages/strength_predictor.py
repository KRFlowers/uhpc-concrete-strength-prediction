"""
Strength Predictor Page

Lets users define a UHPC mix design via sidebar sliders and predicts
compressive strength using the trained XGBoost model. SHAP values
explain which features drive the prediction.
"""
# Load external libraries and shared app utilities

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

try:
    model, feature_names = load_model()
except FileNotFoundError:
    st.error(
        "Model file not found. Run notebook 02 to generate the model artifacts."
    )
    st.stop()


# --- Header ---

st.header("UHPC Compressive Strength Predictor")
st.markdown(
    "Predicted compressive strength is computed by the tuned XGBoost model from "
    "[notebook 02](https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
    "blob/main/notebooks/02_model_development.ipynb). "
    "Use the sidebar sliders to define a UHPC mix design. "
)

# Shrink the st.metric value font so the cards don't dominate the page
st.markdown(
    """
    <style>
      [data-testid="stMetricValue"] { font-size: 1.5rem; }
      [data-testid="stMetricLabel"] { font-size: 0.9rem; }
      [data-testid="stMetricDelta"] { font-size: 0.8rem; }
      [data-testid="stPageLink"] p { font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Sidebar inputs ---
#  loop reads from FEATURE_CONFIG so the sidebar is dynamically generated 

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

# Add a reset button to the sidebar

if st.sidebar.button("Reset to Defaults"):
    st.rerun()


# --- Prediction ---
# Convert slider values to a DataFrame and run model.predict()

input_df = pd.DataFrame([input_values])
prediction = model.predict(input_df)[0]

st.subheader("Strength Prediction")

# Display three metric cards side by side
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=140):
        st.metric(
            label="Predicted Compressive Strength",
            value=f"{prediction:.1f} MPa",
        )

with col2:
    with st.container(border=True, height=140):
        # UHPC classification metric with color logic
        display_uhpc_metric(prediction)

with col3:
    with st.container(border=True, height=140):
        # Show the model's test-set accuracy as a static metric
        st.metric(
            label="Model Performance",
            value="RMSE 5.93 MPa",
            help="XGBoost (tuned via GridSearchCV) from notebook 02. "
                 "RMSE 5.93 MPa, R² = 0.978 on held-out test set.",
        )

# Cross-link to the Observation Explorer page
_, link_col = st.columns([1.7, 1])
with link_col:
    st.page_link(
        "pages/observation_explorer.py",
        label="Explore individual observations",
        icon=":material/search:",
    )

st.divider()


# --- Feature Importance (SHAP) ---
# Use SHAP TreeExplainer to calculate per-feature impact values

st.subheader("Feature Impact (SHAP)")
st.markdown(
    "How much each feature pushes the prediction above or below the model's "
    "average prediction on the training set."
)

# Load the training data and create the SHAP explainer
X_train = load_training_data()
explainer = shap.TreeExplainer(model, data=X_train)
shap_values = explainer(input_df)

# Render the SHAP impact table sorted by absolute impact
display_shap_table(shap_values.values[0], feature_names, input_values)


# --- About (collapsed by default) ---
# Keep the main page clean while making project context available

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

st.divider()
st.caption(
    "UHPC Compressive Strength Predictor | "
    "Built on the XGBoost model from notebook 02 | "
    "For exploratory use only"
)
