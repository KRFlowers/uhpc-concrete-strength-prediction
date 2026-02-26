# UHPC Project — Next Steps


## Report Expansion Opportunities

These are the 16 enhancements identified in the technical report, sorted by recommended implementation order. Value: 1 = add technical depth to analysis, 10 = nice to have.

| # | Pg | Enhancement | Effort | Rec? | Value | Order |
|---|-----|-------------|--------|------|-------|-------|
| R3 | 12 | Residual distribution plot from final model | Low | Yes | 2 | 1 |
| R9 | 16 | Derived ratio features (w/c, w/b ratios) | Medium | Yes | 2 | 2 |
| R11 | 23 | Segmented residual analysis (by UHPC status, by feature) | Low | Yes | 3 | 3 |
| R6 | 15 | Spearman correlations alongside Pearson | Low | Yes | 4 | 4 |
| R15 | 24 | Importance method comparison table | Low | Yes | 4 | 5 |
| R12 | 23 | Conformal prediction for calibrated uncertainty bounds | High | Yes | 3 | 6 |
| R16 | 28 | SHAP interaction/dependence plots | Medium | Yes | 4 | 7 |
| R8 | 8 | Additional models (Elastic Net, MLP, SVR) | Medium | Yes | 5 | 8 |
| R4 | 13 | Binary UHPC classifier (precision/recall/F1) | Medium | Yes | 5 | 9 |
| R10 | 21 | Expanded tuning with Optuna | Medium | Yes | 5 | 10 |
| R13 | 31 | Multi-seed robustness analysis | Medium | No | 6 | 11 |
| R14 | 31 | External validation on independent dataset | High | No | 6 | 12 |
| R1 | 4 | Literature review of prior ML concrete studies | Medium | No | 7 | 13 |
| R7 | 7 | CV scheme comparison (5-fold vs 10-fold vs repeated) | Low | No | 7 | 14 |
| R5 | 13 | Formalized IQR outlier detection / Cook's distance | Low | No | 8 | 15 |
| R17 | 29 | Mix optimization module (scipy.optimize) | High | No | 8 | 16 |
| R2 | 10 | Multivariate outlier detection (Mahalanobis / isolation forest) | Low | No | 9 | 17 |

Additional:
- Choose "strong" correlation threshold — 0.5 (Cohen's academic standard) or 0.7 (engineering convention)
-  Add normality testing clarification (target normality vs residual normality)

## Future Learning Topics

Areas to study for future projects.

- [ ] **F1:** Domain-specific effect sizes — how do materials science papers report and interpret them?
- [ ] **F2:** Validation range sourcing — use full APA citations for validation references
- [ ] **F3:** Bootstrap prediction intervals — what drives undercoverage (81.8% vs 95% nominal)?
- [ ] **F4:** SHAP deeper dive — force plots, dependence plots, interaction values
- [ ] **F5:** Multicollinearity handling — partial dependence, feature ratios, dimensionality reduction

---

*Generated: February 2026*
