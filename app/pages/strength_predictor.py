"""
Strength Predictor Page

UHPC mix design tool. Inputs live in a left column; predictions,
classification, and SHAP explanations render on the right.
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
from emission_factors import compute_co2


def render():
    # --- Load model ---
    try:
        model, feature_names = load_model()
    except FileNotFoundError:
        st.error(
            "Model file not found. Run notebook 02 to generate the model artifacts."
        )
        st.stop()

    # --- Intro ---
    st.markdown(
        "Define inputs to review the predicted compressive strength "
        "Predictions come from the tuned "
        "XGBoost model developed in [notebook 02]"
        "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
        "blob/main/notebooks/02_model_development.ipynb) "
        "of the accompanying analysis."
    )

    # Shrink the st.metric value font so the cards don't dominate the page
    st.markdown(
        """
        <style>
          [data-testid="stMetricValue"] { font-size: 1.5rem; }
          [data-testid="stMetricLabel"] { font-size: 0.9rem; }
          [data-testid="stMetricDelta"] { font-size: 0.8rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Two-column layout: inputs (left) | content (right) ---
    inputs_col, content_col = st.columns([1, 3], gap="large")

    with inputs_col:
        with st.container(border=True):
            st.subheader("Mix Design Inputs")
            st.caption("Adjust values to define a UHPC mix design.")

            input_values = {}
            for feature in feature_names:
                label, unit, min_val, max_val, default, step, help_text = FEATURE_CONFIG[feature]
                input_values[feature] = st.slider(
                    f"{label} ({unit})",
                    min_value=min_val, max_value=max_val,
                    value=default, step=step, help=help_text,
                )

            if st.button("Reset to Defaults"):
                st.rerun()

    with content_col:
        # --- Prediction ---
        input_df = pd.DataFrame([input_values])
        prediction = model.predict(input_df)[0]

        # --- CO2 estimate for the current mix ---
        # Read fiber type from session state so the card reflects the toggle
        # that lives in the breakdown expander below.
        fiber_type = st.session_state.get("co2_fiber_type_predictor", "virgin")
        co2_result = compute_co2(input_values, fiber_type=fiber_type)

        st.subheader("Strength Prediction")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True, height=110):
                st.metric(
                    label="Predicted Strength",
                    value=f"{prediction:.1f} MPa",
                )

        with col2:
            with st.container(border=True, height=110):
                display_uhpc_metric(prediction)

        with col3:
            with st.container(border=True, height=110):
                st.metric(
                    label="CO₂ Emissions (Baseline)",
                    value=f"{co2_result['totals']['default']:.0f} kg/m³",
                    help="Cradle-to-gate (A1–A3) estimate. Expand the "
                         "breakdown below for range and top contributors.",
                )

        # --- CO₂ breakdown ---
        with st.expander("CO₂ breakdown"):
            st.radio(
                "Steel fiber source",
                options=["virgin", "recycled"],
                key="co2_fiber_type_predictor",
                horizontal=True,
                help="Virgin = blast furnace / BOF route. "
                     "Recycled = electric-arc-furnace (EAF) from scrap.",
            )

            totals = co2_result["totals"]
            by_ingredient = co2_result["by_ingredient"]

            c1, c2, c3 = st.columns(3)
            c1.metric("Low",     f"{totals['low']:.0f} kg CO₂/m³")
            c2.metric("Default", f"{totals['default']:.0f} kg CO₂/m³")
            c3.metric("High",    f"{totals['high']:.0f} kg CO₂/m³")

            if by_ingredient:
                total_default = totals["default"] or 1.0
                contributors = sorted(
                    by_ingredient.items(),
                    key=lambda kv: kv[1][1],
                    reverse=True,
                )[:3]
                pieces = [
                    f"{FEATURE_CONFIG[name][0]}: {vals[1]:.0f} kg "
                    f"({100 * vals[1] / total_default:.0f}%)"
                    for name, vals in contributors
                ]
                st.caption(
                    "**Top contributors (default):** " + " · ".join(pieces)
                )

            st.caption(
                "Scope: cradle-to-gate (A1–A3). Sources compiled from "
                "peer-reviewed LCA literature (Sameer et al. 2019; "
                "Randl et al. 2014; Habert et al. 2020; and others). "
                "Not suitable for procurement, EPD reporting, or "
                "regulatory use."
            )

        st.divider()

        # --- Feature Importance (SHAP) ---
        st.subheader("Feature Impact (SHAP)")
        st.markdown(
            "How much each feature pushes the prediction above or below the model's "
            "average prediction on the training set."
        )

        X_train = load_training_data()
        explainer = shap.TreeExplainer(model, data=X_train)
        shap_values = explainer(input_df)

        display_shap_table(shap_values.values[0], feature_names, input_values)
        st.caption(
            "SHAP values computed live via the same `TreeExplainer` approach as "
            "[notebook 03](https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
            "blob/main/notebooks/03_model_interpretation.ipynb)."
        )

        # --- About (collapsed by default) ---
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
        "UHPC Strength Prediction Tool · Prototype · "
        "Companion to the "
        "[UHPC Concrete Strength Prediction analysis]"
        "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction) · "
        "Model developed in [notebook 02]"
        "(https://github.com/KRFlowers/uhpc-concrete-strength-prediction/"
        "blob/main/notebooks/02_model_development.ipynb)"
    )
