# UHPC Compressive Strength Prediction

Predicting compressive strength of Ultra-High Performance Concrete (UHPC) using machine learning.

## Overview

This project analyzes 810 UHPC mix designs to understand the relationship between mix components and compressive strength, with a focus on identifying formulations that meet hurricane-resistant thresholds (≥150 MPa).

## Project Structure

```
├── data/
│   └── uhpc_dataset.csv
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   └── 02_model_development.ipynb
├── images/
└── README.md
```

## Notebooks

1. **01_exploratory_analysis.ipynb** - Data validation, distribution analysis, feature-target correlations, and multicollinearity assessment
2. **02_model_development.ipynb** - Model training, evaluation, and comparison

## Dataset

- **Source:** Kashem, A., et al. (2023). Ultra-High-Performance Concrete (UHPC). Mendeley Data.
- **Records:** 810 UHPC mix designs
- **Features:** 13 variables (cement, slag, silica_fume, limestone_powder, quartz_powder, fly_ash, nano_silica, aggregate, water, fiber, superplasticizer, temperature, age)
- **Target:** compressive_strength (MPa)

## Further Reading

New to UHPC? These resources provide helpful background:

**Articles**
- [Title](link) - Brief description
- [Title](link) - Brief description

**Videos**
- [Title](link) - Brief description
- [Title](link) - Brief description

## Requirements

- Python 3.x
- pandas, numpy, matplotlib, seaborn, scipy, statsmodels
