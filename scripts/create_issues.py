"""
Create GitHub issues for UHPC enhancement plan.
Repo: KRFlowers/uhpc-concrete-strength-prediction

Usage: python scripts/create_issues.py

Requires: gh CLI installed and authenticated (gh auth login)
"""

import subprocess

REPO = "KRFlowers/uhpc-concrete-strength-prediction"

# --- Labels -----------------------------------------------------------
LABELS = [
    {"name": "statistical-analysis", "color": "0E8A16", "desc": "Residual diagnostics, significance testing, normality testing, correlations"},
    {"name": "feature-engineering",  "color": "1D76DB", "desc": "Derived ratio features, outlier detection methods"},
    {"name": "model-evaluation",     "color": "D93F0B", "desc": "Additional models, CV scheme comparison, robustness analysis, Optuna tuning"},
    {"name": "interpretability",     "color": "5319E7", "desc": "SHAP plots, importance method comparison, conformal prediction"},
    {"name": "enhancement",          "color": "A2EEEF", "desc": "General improvements"},
    {"name": "research",             "color": "F9D0C4", "desc": "Literature review, external validation dataset"},
]

# --- Issues ------------------------------------------------------------
# Each issue: (title, label, effort, order, extra_note)
ISSUES = [
    ("R3: Residual distribution plot from final model",
     "statistical-analysis", "Low", 1, ""),

    ("R9: Derived ratio features (w/c, w/b ratios)",
     "feature-engineering", "Medium", 2, ""),

    ("R18: Statistical significance testing between models",
     "statistical-analysis", "Low", 3,
     "Paired t-test or Wilcoxon signed-rank test on CV fold scores to formally validate model differences."),

    ("R19: Learning curves (training vs validation error by dataset size)",
     "model-evaluation", "Low", 4, ""),

    ("R20: Bias-variance decomposition",
     "model-evaluation", "Low", 5,
     "Pairs with learning curves (R19)."),

    ("R11: Segmented residual analysis (by UHPC status, by feature)",
     "statistical-analysis", "Low", 6, ""),

    ("R6: Spearman correlations alongside Pearson",
     "statistical-analysis", "Low", 7, ""),

    ("R15: Importance method comparison table",
     "interpretability", "Low", 8, ""),

    ("R12: Conformal prediction for calibrated uncertainty bounds",
     "interpretability", "High", 9, ""),

    ("R16: SHAP interaction/dependence plots",
     "interpretability", "Medium", 10, ""),

    ("R8: Additional models (Elastic Net, MLP, SVR)",
     "model-evaluation", "Medium", 11, ""),

    ("R4: Binary UHPC classifier (precision/recall/F1)",
     "model-evaluation", "Medium", 12, ""),

    ("R10: Expanded tuning with Optuna",
     "model-evaluation", "Medium", 13, ""),

    ("R13: Multi-seed robustness analysis",
     "model-evaluation", "Medium", 14, ""),

    ("R14: External validation on independent dataset",
     "research", "High", 15, ""),

    ("R1: Literature review of prior ML concrete studies",
     "research", "Medium", 16, ""),

    ("R7: CV scheme comparison (5-fold vs 10-fold vs repeated)",
     "model-evaluation", "Low", 17, ""),

    ("R5: Formalized IQR outlier detection / Cook's distance",
     "feature-engineering", "Low", 18, ""),

    ("R17: Mix optimization module (scipy.optimize)",
     "enhancement", "High", 19, ""),

    ("R2: Multivariate outlier detection (Mahalanobis / isolation forest)",
     "feature-engineering", "Low", 20, ""),

    ("Choose correlation threshold (Cohen 0.5 vs engineering 0.7)",
     "statistical-analysis", "Low", "Additional",
     "Decide between 0.5 (Cohen's academic standard) or 0.7 (engineering convention) for 'strong' correlation threshold."),

    ("Add normality testing clarification (target vs residual normality)",
     "statistical-analysis", "Low", "Additional", ""),
]


def run_gh(args):
    """Run a gh CLI command and return the result."""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
    return result


def create_labels():
    """Create all labels on the repo."""
    print("=== Creating labels ===\n")
    for label in LABELS:
        print(f"  {label['name']}")
        run_gh([
            "label", "create", label["name"],
            "--repo", REPO,
            "--color", label["color"],
            "--description", label["desc"],
            "--force",
        ])
    print()


def create_issues():
    """Create all issues on the repo."""
    print("=== Creating issues ===\n")
    for title, label, effort, order, note in ISSUES:
        body = f"**Effort:** {effort}\n**Reference:** `docs/PROJECT_ENHANCEMENT_PLAN.md` — Order {order}"
        if note:
            body += f"\n\n{note}"

        print(f"  Creating: {title}")
        result = run_gh([
            "issue", "create",
            "--repo", REPO,
            "--title", title,
            "--label", label,
            "--body", body,
        ])
        if result.returncode == 0:
            url = result.stdout.strip()
            print(f"  -> {url}")
    print()


if __name__ == "__main__":
    create_labels()
    create_issues()
    print("=== Done — created 22 issues ===")
