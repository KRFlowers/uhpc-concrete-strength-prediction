# Project: UHPC Compressive Strength Prediction

## Business Case
UHPC became commercially available in the US in 2000. Since 2006, FHWA and state DOTs have deployed it in bridge infrastructure across Florida, Iowa, New York, and Virginia. The market is growing at 7% annually as an emerging solution for climate-resilient infrastructure. UHPC achieves 150+ MPa strength (2x conventional concrete) while reducing carbon emissions through cement replacement with supplementary materials. However, optimizing mix designs requires extensive lab testing, creating a development bottleneck. This is where predictive models can help accelerate the process.

## Problem Statement
Given various mix design inputs, create a machine learning model to help predict UHPC compressive strength.

**Personal motivation:** Firsthand exposure to hurricane impacts on Florida infrastructure motivated an interest in advanced building materials and structural resilience.

## Practical Application
The model serves as a **mix design screening tool** for civil engineers and materials scientists. The intended workflow:
1. Engineer proposes candidate mix formulations by adjusting ingredient ratios
2. Model predicts expected compressive strength with 95% confidence bounds for each candidate
3. Engineer compares predicted strengths to optimize for cost, performance, or material availability
4. Promising formulations proceed to physical lab testing for validation

The model reduces the number of physical tests required to identify high-performance UHPC formulations but does not replace physical validation, which remains necessary for structural certification.

## Success Criteria
R² > 0.92 on test set. 

## Deliverables
**EDA Notebook:**
- Lightweight validation (missing values, negatives, duplicates)
- Univariate, bivariate, multivariate analysis
- Key insights on distributions and correlations

**Model Development Notebook:**
- 5 models: possible Linear Regression (baseline), Ridge, LASSO, Random Forest, XGBoost
- 5-fold cross-validation with RMSE as primary metric
- Hyperparameter tuning 
- Model comparison table (RMSE, MAE, R²)
- Feature importance analysis 
- Bootstrap prediction intervals (200 resamples, 95% CI)

**Possible Visualizations:**
- Cross-validation model comparison (MAE and R²)
- Actual vs Predicted scatter plot (best model)
- Residual plot (best model)
- Feature importance (XGBoost)
- Prediction intervals with confidence bands


## Dataset
**Source:** Mendeley (Kashem et al., 2023)
**Size:** 810 samples, 14 features
**Features:** Cement, water, fly ash, silica fume, nano-silica, quartz powder, limestone powder, aggregate, slag, superplasticizer, fiber, temperature, curing age
**Target:** Compressive strength (MPa)
**Status:** Pre-validated research dataset

**Citation:** Kashem, A., Karim, R., Malo, S.C., Das, P. (2023). Ultra-High-Performance Concrete (UHPC). Mendeley Data, V1. http://dx.doi.org/10.17632/85r7bh4zsz.1

## Limitations
- Analysis will focus on statistical patterns; domain-specific material science interpretation is out of scope


