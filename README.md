# UHPC Compressive Strength Prediction

This project builds and compares five regression models (Linear Regression, Ridge, LASSO, Random Forest, and XGBoost) to predict UHPC compressive strength from 13 mix design features. Models were evaluated using 5-fold cross-validation with RMSE as the primary metric, followed by hyperparameter tuning via GridSearchCV. The final XGBoost model achieved an RMSE of 5.93 MPa (R² = 0.978) on a held-out test set. SHAP analysis was applied to interpret feature contributions at both global and individual prediction levels.

---

## Business Context

Ultra-High-Performance Concrete (UHPC) is used in high-strength structural applications such as bridge components and hurricane-resistant construction. Predicting compressive strength from mix design variables can reduce costly laboratory testing cycles and support decision-making before physical batching. This project explores how a data-driven model can estimate strength while also providing insight into which mix components most meaningfully impact results.

---

## Approach

The project is organized as a notebook-based pipeline.

- **01_exploratory_analysis.ipynb**  
  Validated data quality, removed duplicate records (810 → 792), examined feature distributions, assessed correlations, and evaluated multicollinearity using VIF.

- **02_model_development.ipynb**  
  Compared Linear Regression, Ridge, LASSO, Random Forest, and XGBoost using cross-validation. Selected the best-performing model and evaluated it on a held-out test set.

- **03_model_interpretation.ipynb**
  Applied SHAP to the final XGBoost model to assess global feature importance and examine how key variables influence predicted compressive strength.

- **Streamlit App** — Interactive tool for prediction and exploration (see [below](#streamlit-app))

---

## Results

Model performance was evaluated using RMSE and R² on a held-out test set.

### Model Performance

- **XGBoost achieved 5.93 MPa RMSE (R² = 0.978)**
- Tree-based models substantially outperformed linear models (RMSE ~8–9 MPa vs ~23 MPa)
- Random Forest performed strongly but slightly below XGBoost

![Cross-Validation Model Comparison](images/cv_model_comparison.png)

### Feature Importance

Top predictors identified via SHAP:

1. **Age**
2. **Fiber**
3. **Cement**
4. **Silica fume**

### SHAP Insights

![SHAP Beeswarm Plot](images/shap_summary_beeswarm.png)

- Age had the strongest influence on predicted strength. Higher curing time consistently increased predictions, while low curing time significantly reduced them.
- Fiber, cement, silica fume, and superplasticizer were generally associated with higher predicted strength.
- Higher water and aggregate content were associated with lower predicted strength.
- The variation in SHAP values across samples indicates that the magnitude of a feature's contribution differs across observations.

---

## Streamlit App

The project includes an interactive two-page Streamlit app built on the trained XGBoost model.

![Strength Predictor](images/app_strength_predictor.png)

- **Strength Predictor** — Adjust mix design sliders to get a predicted compressive strength with per-feature SHAP explanation
- **Observation Explorer** — Browse all 792 observations, filter by strength range or material presence, and select any row to see the model's prediction and feature-level impact

Run locally:

    streamlit run app/app.py

---

## Limitations

- Moderate dataset size (792 records after cleaning) with no external validation dataset
- Bootstrap prediction intervals achieved 81.8% coverage vs. the 95% nominal target, suggesting the need for an alternative uncertainty method
- Analysis used raw mix design features only; feature engineering was not explored

---

## Next Steps

A detailed analysis report was created that identified the possible enhancements below. These were captured in an enhancement roadmap located in [`docs/`](docs/).

- Engineer domain-informed features such as water-to-cement and water-to-binder ratios
- Replace bootstrap intervals with conformal prediction for more accurate uncertainty bounds
- Add Spearman correlations and segmented residual analysis to strengthen diagnostic coverage
- Explore use of variable correlation thresholds to better identify feature relationships
- Implement repeated k-fold cross-validation
- Compare feature importance methods (SHAP vs. permutation vs. gain-based) and add SHAP dependence plots
- Evaluate additional models (Elastic Net, MLP, SVR) and Bayesian hyperparameter tuning via Optuna
- Compare model performance against published ML concrete strength studies to benchmark results in the broader literature

---

## Data

- **Source:** Kashem, A., et al. (2023). Ultra-High-Performance Concrete (UHPC). Mendeley Data  
- **Records:** 810 mix designs (792 after duplicate removal)  
- **Features (13):** cement, slag, silica_fume, limestone_powder, quartz_powder, fly_ash, nano_silica, aggregate, water, fiber, superplasticizer, temperature, age  
- **Target:** compressive_strength (MPa)

---

## Tech Stack

- Python 3.14
- pandas, NumPy
- scikit-learn
- XGBoost
- SHAP
- statsmodels
- matplotlib, seaborn
- Streamlit
- Jupyter