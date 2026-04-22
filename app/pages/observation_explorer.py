"""
Observation Explorer Page

Browse the full dataset (train + test), filter observations, select one to
view the model's prediction and SHAP explanation. Filters live in a left
column; results render on the right.
"""

# --- Imports ---
import streamlit as st
import pandas as pd
import shap

from shared import (
    FEATURE_CONFIG,
    load_model,
    load_training_data,
    load_all_observations,
    display_uhpc_metric,
    display_shap_table,
)
from emission_factors import compute_co2


def render():
    # --- Load model and data ---
    try:
        model, feature_names = load_model()
    except FileNotFoundError:
        st.error(
            "Model file not found. Run notebook 02 to generate the model artifacts."
        )
        st.stop()

    all_obs = load_all_observations()

    # --- Intro ---
    st.markdown(
        "Select a mix design below to see measured strength, model "
        "prediction, and SHAP explanation."
    )

    # --- Two-column layout: filters (left) | content (right) ---
    filters_col, content_col = st.columns([1, 3], gap="large")

    with filters_col:
        with st.container(border=True):
            st.markdown("##### Filters")

            strength_min = float(all_obs["compressive_strength"].min())
            strength_max = float(all_obs["compressive_strength"].max())
            strength_range = st.slider(
                "Compressive Strength (MPa)",
                min_value=strength_min,
                max_value=strength_max,
                value=(strength_min, strength_max),
                step=1.0,
                help="Filter observations by actual compressive strength",
            )

            set_filter = st.radio(
                "Dataset Split",
                options=["All", "Train", "Test"],
                horizontal=True,
                help="Show observations from training set, test set, or both",
            )

            optional_materials = [
                "slag", "silica_fume", "limestone_powder", "quartz_powder",
                "fly_ash", "nano_silica", "fiber",
            ]
            required_materials = st.multiselect(
                "Required materials",
                options=optional_materials,
                format_func=lambda mat: FEATURE_CONFIG[mat][0],
                help="Show only observations that contain all selected materials",
            )

    # --- Apply filters ---
    filtered = all_obs.copy()
    filtered = filtered[filtered["compressive_strength"].between(*strength_range)]

    if set_filter != "All":
        filtered = filtered[filtered["Set"] == set_filter]

    for mat in required_materials:
        filtered = filtered[filtered[mat] > 0]

    with content_col:
        # --- Observation summary header + metric cards ---
        st.markdown("##### Observation Summary")
        metrics_container = st.container()

        # --- Records table header ---
        st.markdown("##### Mix Design Records")
        st.caption(f"Showing {len(filtered)} of {len(all_obs)} observations.")

        # --- Build display table ---
        display_columns = {f: f"{FEATURE_CONFIG[f][0]} ({FEATURE_CONFIG[f][1]})" for f in feature_names}
        display_columns["compressive_strength"] = "Strength (MPa)"
        display_columns["Set"] = "Set"

        display_df = filtered.rename(columns=display_columns).reset_index(drop=True)
        strength_col = display_df.pop("Strength (MPa)")
        display_df.insert(0, "Strength (MPa)", strength_col)

        # --- Selectable dataframe ---
        event = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            height=200,
        )

        # --- Resolve selection and fill metric cards ---
        # If the user hasn't clicked a row, showcase the highest-strength
        # observation in the current filtered set so the cards and SHAP
        # populate on first load.
        selected_rows = event.selection.rows
        user_selected = bool(selected_rows)

        feature_vals = {}
        input_df = pd.DataFrame()
        actual_strength = 0.0
        predicted_strength = 0.0
        has_selection = False
        showing_default = False

        if user_selected:
            selected_idx = selected_rows[0]
            has_selection = True
        elif len(filtered) > 0:
            selected_idx = int(filtered["compressive_strength"].values.argmax())
            has_selection = True
            showing_default = True

        if has_selection:
            selected = filtered.iloc[selected_idx]
            feature_vals = {f: selected[f] for f in feature_names}
            actual_strength = selected["compressive_strength"]
            input_df = pd.DataFrame([feature_vals])
            predicted_strength = model.predict(input_df)[0]

        # --- CO2 estimate for the selected mix ---
        # Read fiber type from session state so the card reflects the toggle
        # that lives in the breakdown expander below.
        co2_result = None
        if has_selection:
            fiber_type = st.session_state.get("co2_fiber_type_explorer", "virgin")
            co2_result = compute_co2(feature_vals, fiber_type=fiber_type)

        with metrics_container:
            if showing_default:
                st.caption("Showing highest-strength observation.")
            elif not has_selection:
                st.caption("Select an observation from the table below.")
            col1, col2, col3, col4 = st.columns(4)

            # Col 1: Measured Strength (ground truth from source dataset)
            with col1:
                with st.container(border=True, height=110):
                    st.metric(
                        label="Measured Strength",
                        value=f"{actual_strength:.1f} MPa" if has_selection else "—",
                        help="Compressive strength reported in the source dataset.",
                    )

            # Col 2: Model Prediction (adjacent to measured for visual comparison)
            with col2:
                with st.container(border=True, height=110):
                    st.metric(
                        label="Model Prediction",
                        value=f"{predicted_strength:.1f} MPa" if has_selection else "—",
                        help="XGBoost model prediction for this observation.",
                    )

            # Col 3: UHPC Classification
            with col3:
                with st.container(border=True, height=110):
                    if has_selection:
                        display_uhpc_metric(actual_strength)
                    else:
                        st.metric(label="UHPC Classification", value="—")

            # Col 4: CO₂ Emissions (Baseline) — cradle-to-gate estimate
            with col4:
                with st.container(border=True, height=110):
                    if has_selection and co2_result is not None:
                        st.metric(
                            label="CO₂ Emissions (Baseline)",
                            value=f"{co2_result['totals']['default']:.0f} kg/m³",
                            help="Cradle-to-gate (A1–A3) estimate. Expand the "
                                 "breakdown below for range and top contributors.",
                        )
                    else:
                        st.metric(
                            label="CO₂ Emissions (Baseline)",
                            value="—",
                        )

            # --- CO₂ breakdown (only when a row is selected) ---
            if has_selection and co2_result is not None:
                with st.expander("CO₂ breakdown"):
                    st.radio(
                        "Steel fiber source",
                        options=["virgin", "recycled"],
                        key="co2_fiber_type_explorer",
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



        # --- SHAP explanation (only when a row is selected) ---
        if has_selection:
            st.divider()

            st.markdown("#### Feature Impact (SHAP)")
            st.markdown(
                "How much each feature increases or decreases the predicted "
                "strength for this observation."
            )

            X_train = load_training_data()
            explainer = shap.TreeExplainer(model, data=X_train)
            shap_values = explainer(input_df)

            display_shap_table(shap_values.values[0], feature_names, feature_vals)

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
