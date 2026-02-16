# Decision Log — UHPC Compressive Strength Prediction

Quick reference of key decisions made during the project and why.

---

## Data Quality

### DQ-1: Removed 18 duplicate rows (810 → 792)
- Identical mix designs with identical values — data entry duplication, not repeated experiments

### DQ-2: No imputation needed
- Zero missing values in the pre-validated research dataset

### DQ-3: Kept zero-heavy features as-is
- 7 features are zero-inflated (slag, fly ash, nano-silica, etc.) — zeros mean "not used in this mix"
- Real and meaningful values, not missing data

---

## Target Variable

### TV-1: No target transformation
- Compressive strength skewness of 0.03 — close enough to normal, no transform needed

### TV-2: 150 MPa as UHPC threshold
- FHWA-defined minimum for UHPC (FHWA-HRT-18-036)
- 73.5% of samples below, 26.5% above

---

## Feature Analysis

### FA-1: Used |r| > 0.7 for "strong" correlation
- Cohen's 0.5 threshold is too permissive for engineering data where physical relationships are stronger
- Acknowledged Cohen's conventions in notebook

### FA-2: Used 0.7 threshold for multicollinearity flagging
- Features sharing >70% variance are effectively redundant
- Standard threshold across fields, distinct from effect size classification

---

## Multicollinearity

### MC-1: Retained high-VIF features instead of dropping
- Water (VIF 72.7), cement (VIF 59.1), aggregate (VIF 13.4) all exceeded threshold of 10
- Handled through model choice: Ridge/LASSO penalize redundancy, tree models split on most informative feature

### MC-2: Removed PCA from EDA
- Only 13 features — not a high-dimensional problem
- PCA destroys feature interpretability, which matters for materials science context

---

## Model Selection

### MS-1: Included linear models despite expected underperformance
- Establishes a baseline to quantify how much non-linearity matters
- ~3x improvement from tree-based models (RMSE 8 vs 23 MPa) makes the case

### MS-2: Selected XGBoost as final model
- Best performance on both CV and test set (RMSE 5.93 MPa, R² 0.978)
- Gradient boosting's sequential error correction outperformed Random Forest's parallel averaging

### MS-3: 5-fold cross-validation
- Averages performance across multiple splits for reliable estimates
- 5 folds is standard for ~792 samples

### MS-4: Stratified train/test split (80/20)
- 26.5% of samples exceed 150 MPa — stratification ensures representative proportions in both sets

---

## Evaluation & Uncertainty

### EU-1: RMSE as primary metric over MAE
- Penalizes large errors more heavily — important for safety-critical engineering applications
- MAE and R² as supporting metrics

### EU-2: Bootstrap prediction intervals (200 resamples, 95% CI)
- Engineers need confidence bounds, not just point predictions
- Bootstrap doesn't assume normality — appropriate for tree-based models
- Known limitation: 81.8% coverage vs nominal 95%

---

## Interpretation

### IN-1: Brief SHAP demonstration, not comprehensive analysis
- Limited to global feature importance (beeswarm, bar) and individual explanations (waterfall)
- Comprehensive SHAP analysis deferred as a next step

### IN-2: TreeSHAP over model-agnostic SHAP
- Exact and efficient for tree-based models (polynomial vs exponential time)

---

## Documentation & Style

### DS-1: Plain-language voice over academic tone
- Target audience: recruiters, hiring managers, engineers
- Write like explaining to a smart colleague, not submitting to a journal

### DS-2: Interpretation blocks after every output
- Markdown cell after every analytical output explaining what the result means
- "Modeling Note" labels when findings directly affect model decisions

---

*Last updated: February 2026*
