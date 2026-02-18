"""
Observation Explorer Page

Lets users browse the full dataset (train + test), filter observations,
select a row, and see the model's prediction and SHAP explanation for
that specific mix design.
"""

# --- Imports ---
# Load external libraries and shared app utilities

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


# --- Load model and data ---
#  Load the trained XGBoost model and all 792 observations from disk

try:
    model, feature_names = load_model()
except FileNotFoundError:
    st.error(
        "Model file not found. Run notebook 02 to generate the model artifacts."
    )
    st.stop()

all_obs = load_all_observations()


# --- Header ---
# Display the page title and introductory description

st.title("Observation Explorer")
st.markdown(
    "Browse the dataset of 792 UHPC mix designs. Select a row to see "
    "the model's prediction and feature-level SHAP explanation."
)


# --- Metric card placeholder ---
#  Reserve space for metric cards at the top of the page

metrics_container = st.container()

# --- Sidebar filters ---
# Sidebar filters to narrow the observation table to help users find specific
# strength ranges or material combinations quickly

st.sidebar.header("Filters")

# Strength range slider to users isolate mixes within a specific performance range
strength_min = float(all_obs["compressive_strength"].min())
strength_max = float(all_obs["compressive_strength"].max())
strength_range = st.sidebar.slider(
    "Compressive Strength (MPa)",
    min_value=strength_min,
    max_value=strength_max,
    value=(strength_min, strength_max),
    step=1.0,
    help="Filter observations by actual compressive strength",
)

# Train/Test split filter
set_filter = st.sidebar.radio(
    "Dataset Split",
    options=["All", "Train", "Test"],
    horizontal=True,
    help="Show observations from training set, test set, or both",
)

# Add checkboxes for filtering by whether a material is present lets users
# find mixes that include specific supplementary materials
st.sidebar.markdown("**Filter by material presence:**")
material_filters = {}
optional_materials = [
    "slag", "silica_fume", "limestone_powder", "quartz_powder",
    "fly_ash", "nano_silica", "fiber",
]
for mat in optional_materials:
    label = FEATURE_CONFIG[mat][0]
    material_filters[mat] = st.sidebar.checkbox(
        f"Has {label}", value=False, key=f"filter_{mat}",
    )


# --- Apply filters ---
# Narrow the dataset based on all active sidebar filters
# Each filter is applied sequentially — strength range first,
# then dataset split, then material presence. The result is a
# subset of observations matching every active filter.

filtered = all_obs.copy()

# Keep only observations within the selected strength range
filtered = filtered[filtered["compressive_strength"].between(*strength_range)]

#  Keep only observations from the selected dataset split
if set_filter != "All":
    filtered = filtered[filtered["Set"] == set_filter]

# Keep only observations where checked materials are present (> 0)
for mat, required in material_filters.items():
    if required:
        filtered = filtered[filtered[mat] > 0]

# Show a count of how many observations pass all filters
st.markdown(f"**{len(filtered)}** observations match the current filters.")


# --- Build display table ---
# Create a display-friendly version with strength as the first column
display_columns = {f: f"{FEATURE_CONFIG[f][0]} ({FEATURE_CONFIG[f][1]})" for f in feature_names}
display_columns["compressive_strength"] = "Strength (MPa)"
display_columns["Set"] = "Set"

display_df = filtered.rename(columns=display_columns).reset_index(drop=True)
# Move strength to the first column so users see the target variable immediately
strength_col = display_df.pop("Strength (MPa)")
display_df.insert(0, "Strength (MPa)", strength_col)


# --- Selectable dataframe ---
# Render the table with single-row selection enabled

event = st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    height=250,
)


# --- Resolve selection and fill metric cards ---
# Check if a row is selected, compute values, then fill the
# placeholder container that was reserved at the top of the page

# Check which row (if any) the user clicked in the table
selected_rows = event.selection.rows
has_selection = bool(selected_rows)

if has_selection:
    # Extract the selected observation and run the model on its features
    selected = filtered.iloc[selected_rows[0]]
    feature_vals = {f: selected[f] for f in feature_names}
    actual_strength = selected["compressive_strength"]
    input_df = pd.DataFrame([feature_vals])
    predicted_strength = model.predict(input_df)[0]
    residual = actual_strength - predicted_strength

# Fill the metric card placeholder at the top of the page
with metrics_container:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.4])

    with col1:
        # Show the real measured compressive strength from the dataset
        st.metric(
            label="Actual Strength",
            value=f"{actual_strength:.1f} MPa" if has_selection else "—",
        )

    with col2:
        # Show what the model would predict for this observation's features
        st.metric(
            label="Predicted Strength",
            value=f"{predicted_strength:.1f} MPa" if has_selection else "—",
        )

    with col3:
        # Show the difference between actual and predicted strength

        st.metric(
            label="Residual",
            value=f"{residual:+.1f} MPa" if has_selection else "—",
            help="Actual minus Predicted. Positive means the model under-predicted.",
        )

    with col4:
        # Classify the observation as meeting or missing the UHPC threshold
        if has_selection:
            display_uhpc_metric(actual_strength)
        else:
            st.metric(label="UHPC Classification", value="—")

    if not has_selection:
        # WPrompt the user to interact with the table
        st.info("Select an observation from the table below.")


# --- SHAP explanation (only when a row is selected) ---
# Compute and display per-feature SHAP values for the selected observation

if has_selection:
    st.divider()

    st.subheader("Feature Impact on This Mix Design")
    st.markdown(
        "SHAP values below show how much each feature increases or decreases "
        "the predicted strength."
    )

    # Load training data as SHAP background and create the explainer
    X_train = load_training_data()
    explainer = shap.TreeExplainer(model, data=X_train)
    shap_values = explainer(input_df)

    # Render the SHAP impact table sorted by absolute impact
    display_shap_table(shap_values.values[0], feature_names, feature_vals)


# --- Footer ---
# Display a disclaimer caption at the bottom of the page

st.divider()
st.caption(
    "UHPC Compressive Strength Predictor | "
    "Built on the XGBoost model from notebook 02 | "
    "For exploratory use only"
)
