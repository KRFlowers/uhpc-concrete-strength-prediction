# UHPC Compressive Strength Prediction

This project analyzes a dataset of 810 Ultra-High-Performance Concrete (UHPC) mix designs to build and compare machine learning models that predict compressive strength. Models were evaluated using cross-validation to identify the strongest performer. In addition to predictive performance, I applied interpretable machine learning techniques to better understand how individual mix components influence strength. The project emphasizes both accurate prediction and model interpretability, recognizing that in materials design, understanding how variables influence strength is as important as the prediction itself.

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

---

## Results

Model performance was evaluated using RMSE and R² on a held-out test set.

### Model Performance

- **XGBoost achieved 5.93 MPa RMSE (R² = 0.978)**
- Tree-based models substantially outperformed linear models (RMSE ~8–9 MPa vs ~23 MPa)
- Random Forest performed strongly but slightly below XGBoost

### Feature Importance

Top predictors identified via SHAP:

1. **Age**
2. **Fiber**
3. **Cement**
4. **Silica fume**

### SHAP Insights

- Age had the strongest influence on predicted strength. Higher curing time consistently increased predictions, while low curing time significantly reduced them.
- Fiber, cement, silica fume, and superplasticizer were generally associated with higher predicted strength.
- Higher water and aggregate content were associated with lower predicted strength.
- The variation in SHAP values across samples indicates that the magnitude of a feature’s contribution differs across observations.

---

## Limitations

- Moderate dataset size (792 records after cleaning)
- Limited materials science domain expertise
- Feature engineering was limited and could be expanded with additional domain research
- Interpretation focused on high-level variable influence rather than detailed engineering implications

---

## Next Steps

- Incorporate domain-informed feature engineering (e.g., ratio-based or interaction features)
- Add prediction intervals for uncertainty estimation
- Validate performance on external UHPC datasets
- Explore how the model could support performance-based mix design decisions
- Develop an interactive tool for rapid mix experimentation

---

## Data

- **Source:** Kashem, A., et al. (2023). Ultra-High-Performance Concrete (UHPC). Mendeley Data  
- **Records:** 810 mix designs (792 after duplicate removal)  
- **Features (13):** cement, slag, silica_fume, limestone_powder, quartz_powder, fly_ash, nano_silica, aggregate, water, fiber, superplasticizer, temperature, age  
- **Target:** compressive_strength (MPa)

---

## Tech Stack

- Python 3.12+
- pandas, NumPy
- scikit-learn
- XGBoost
- SHAP
- statsmodels
- matplotlib, seaborn
- Jupyter