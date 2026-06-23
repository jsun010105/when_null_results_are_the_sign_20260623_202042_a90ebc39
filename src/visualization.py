"""
Visualization for the null-results-as-signal study.

Generates publication-quality figures for the REPORT.md.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats


def proportion_confint(count, nobs, alpha=0.05, method="wilson"):
    """Wilson confidence interval for a proportion."""
    z = stats.norm.ppf(1 - alpha / 2)
    p = count / nobs if nobs > 0 else 0.5
    if nobs == 0:
        return (0.0, 1.0)
    denom = 1 + z**2 / nobs
    center = (p + z**2 / (2 * nobs)) / denom
    margin = z * (p * (1 - p) / nobs + z**2 / (4 * nobs**2)) ** 0.5 / denom
    return (max(0.0, center - margin), min(1.0, center + margin))

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import FIGURES_DIR, INTERVENTION_LEVELS, MODELS, EQUIVALENCE_THRESHOLD

# Style
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Color palette for models
MODEL_COLORS = {
    "Claude-3-Haiku": "#D55E00",
    "GPT-4o-Mini": "#0072B2",
    "Llama-3.1-8B": "#009E73",
    "Mistral-7B": "#CC79A7",
}
MODEL_MARKERS = {
    "Claude-3-Haiku": "o",
    "GPT-4o-Mini": "s",
    "Llama-3.1-8B": "^",
    "Mistral-7B": "D",
}

LEVEL_LABELS = [cfg["label"] for cfg in INTERVENTION_LEVELS]
LEVEL_SHORT = ["L0\n(None)", "L1\n(Minimal)", "L2\n(Standard)", "L3\n(Detailed)", "L4\n(Maximum)"]


def plot_dose_response_curves(aggregated: dict, save_path: str = None) -> str:
    """Plot refusal rate vs intervention level for all models (dose-response curves)."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for model_cfg in MODELS:
        model_label = model_cfg["label"]
        if model_label not in aggregated:
            continue
        level_data = aggregated[model_label]
        levels = sorted(int(k) for k in level_data.keys())
        rates = [level_data[l]["refusal_rate"] for l in levels]
        ns = [level_data[l]["n_total"] for l in levels]
        # 95% Wilson confidence intervals for proportions
        cis = []
        for r_val, n_val in zip(
            [level_data[l]["n_refusals"] for l in levels], ns
        ):
            r_ci = proportion_confint(r_val, n_val, alpha=0.05, method="wilson")
            cis.append(r_ci)

        color = MODEL_COLORS.get(model_label, "gray")
        marker = MODEL_MARKERS.get(model_label, "o")
        yerr_lower = [max(0.0, rates[i] - cis[i][0]) for i in range(len(rates))]
        yerr_upper = [max(0.0, cis[i][1] - rates[i]) for i in range(len(rates))]

        ax.errorbar(
            levels, rates,
            yerr=[yerr_lower, yerr_upper],
            color=color, marker=marker,
            label=model_label,
            linewidth=2, markersize=8, capsize=4, capthick=1.5,
        )

    # Add horizontal band for equivalence region reference
    if levels:
        ax.axhspan(0.0, EQUIVALENCE_THRESHOLD, alpha=0.06, color="gray", label=f"Δ={EQUIVALENCE_THRESHOLD} (TOST margin)")

    ax.set_xlabel("Intervention Level (Prompt Safety Strength)")
    ax.set_ylabel("Refusal Rate (fraction of behaviors refused)")
    ax.set_title("Dose-Response Curves: Refusal Rate vs. Intervention Strength\n"
                 "(Flat = robustness plateau; Rising = dose-responsive)")
    ax.set_xticks(range(len(LEVEL_SHORT)))
    ax.set_xticklabels(LEVEL_SHORT, fontsize=9)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc="lower right", framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.axhline(1.0, color="gray", linestyle=":", alpha=0.4)

    fig.tight_layout()
    if save_path is None:
        save_path = f"{FIGURES_DIR}/dose_response_curves.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_bayes_factors(statistical_results: dict, save_path: str = None) -> str:
    """Plot BF01 per model × intervention level as a heatmap."""
    classifications = statistical_results.get("classifications", {})
    if not classifications:
        return ""

    models = list(classifications.keys())
    levels = [1, 2, 3, 4]  # Levels compared against baseline (0)
    level_labels = ["L1\nvs L0", "L2\nvs L0", "L3\nvs L0", "L4\nvs L0"]

    bf_matrix = np.zeros((len(models), len(levels)))
    for i, model in enumerate(models):
        level_stats = classifications[model].get("level_statistics", {})
        for j, level in enumerate(levels):
            if level in level_stats:
                bf_matrix[i, j] = level_stats[level]["bayes_factor"]["bf01"]
            elif str(level) in level_stats:
                bf_matrix[i, j] = level_stats[str(level)]["bayes_factor"]["bf01"]
            else:
                bf_matrix[i, j] = 1.0

    # Log-scale BF for visualization
    log_bf = np.log10(np.clip(bf_matrix, 1e-3, 1e3))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)  # Blue=plateau, Red=dose-response
    im = ax.imshow(log_bf, cmap=cmap, vmin=-2, vmax=2, aspect="auto")

    # Annotate cells with BF values
    for i in range(len(models)):
        for j in range(len(levels)):
            val = bf_matrix[i, j]
            text_color = "white" if abs(log_bf[i, j]) > 1 else "black"
            ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                    fontsize=10, color=text_color, fontweight="bold")

    ax.set_xticks(range(len(levels)))
    ax.set_xticklabels(level_labels)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_title("Bayes Factor BF₀₁ per Model × Intervention Level\n"
                 "(Blue > 3: evidence for plateau; Red < 0.33: evidence for dose-response)")

    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("log₁₀(BF₀₁)")
    cbar.set_ticks([-2, -1, 0, 1, 2])
    cbar.set_ticklabels(["-100", "-10", "1", "10", "100"])

    # Add boundary lines
    ax.axvline(-0.5, color="gray", linewidth=0.5)
    ax.set_xlim(-0.5, len(levels) - 0.5)

    fig.tight_layout()
    if save_path is None:
        save_path = f"{FIGURES_DIR}/bayes_factors_heatmap.png"
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_hierarchical_beta(hierarchical_results: dict, save_path: str = None) -> str:
    """Plot posterior distributions of β_m (sensitivity to intervention) for each model."""
    fig, ax = plt.subplots(figsize=(8, 4.5))

    models = list(hierarchical_results.keys())
    beta_means = [hierarchical_results[m]["beta_mean"] for m in models]
    beta_stds = [hierarchical_results[m]["beta_std"] for m in models]
    beta_cis = [hierarchical_results[m]["beta_ci_95"] for m in models]
    classifications = [hierarchical_results[m]["classification"] for m in models]

    colors = [MODEL_COLORS.get(m, "gray") for m in models]

    # Plot as horizontal forest plot
    y_positions = range(len(models))
    for i, (model, mean, std, ci, cls) in enumerate(
        zip(models, beta_means, beta_stds, beta_cis, classifications)
    ):
        color = colors[i]
        ax.errorbar(
            mean, i,
            xerr=[[mean - ci[0]], [ci[1] - mean]],
            color=color, marker="o", markersize=9,
            linewidth=2, capsize=5, capthick=2,
        )
        ax.text(
            ci[1] + 0.05, i,
            f"{cls.replace('_', '-')}",
            va="center", ha="left", fontsize=9,
            color=color, style="italic",
        )

    ax.axvline(0, color="black", linestyle="-", linewidth=1.5, alpha=0.7)
    ax.axvspan(-0.15, 0.15, alpha=0.1, color="gray", label="Near-zero (plateau region)")
    ax.set_yticks(y_positions)
    ax.set_yticklabels(models)
    ax.set_xlabel("Intervention Sensitivity β_m (Normalized)\n"
                  "(β≈0: robustness plateau; β>0: dose-responsive)")
    ax.set_title("Hierarchical Bayesian Sensitivity Parameter β_m\n"
                 "(95% Credible Intervals — Forest Plot)")
    ax.legend(loc="upper left")
    ax.grid(True, axis="x", alpha=0.3, linestyle="--")
    ax.set_xlim(-1.5, 1.5)

    fig.tight_layout()
    if save_path is None:
        save_path = f"{FIGURES_DIR}/hierarchical_beta_forest.png"
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_classification_summary(statistical_results: dict, aggregated: dict, save_path: str = None) -> str:
    """Summary plot: classification results per model with refusal rate overview."""
    summary = statistical_results.get("summary", {})
    if not summary:
        return ""

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: Baseline vs Max intervention refusal rates
    ax = axes[0]
    models = list(summary.keys())
    baseline_rates = [summary[m]["baseline_refusal_rate"] for m in models]
    max_rates = []
    for m in models:
        if m in aggregated:
            levels = aggregated[m]
            all_rates = [v["refusal_rate"] for v in levels.values()]
            max_rates.append(max(all_rates))
        else:
            max_rates.append(0.0)

    x = np.arange(len(models))
    w = 0.35
    bars1 = ax.bar(x - w / 2, baseline_rates, w, label="Baseline (Level 0)", alpha=0.8,
                   color=[MODEL_COLORS.get(m, "gray") for m in models], edgecolor="black")
    bars2 = ax.bar(x + w / 2, max_rates, w, label="Maximum Intervention (Level 4)", alpha=0.5,
                   color=[MODEL_COLORS.get(m, "gray") for m in models], edgecolor="black",
                   hatch="//")

    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("-", "-\n") for m in models], fontsize=9)
    ax.set_ylabel("Refusal Rate")
    ax.set_title("Baseline vs. Maximum Intervention\nRefusal Rates")
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", alpha=0.3)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

    # Right: Classification and BF01 summary
    ax = axes[1]
    median_bfs = [summary[m]["median_bf01"] for m in models]
    cls_colors = {
        "plateau": "#2196F3", "dose_responsive": "#F44336", "inconclusive": "#9E9E9E"
    }
    bar_colors = [cls_colors.get(summary[m]["classification"], "gray") for m in models]
    bars = ax.bar(
        models, np.log10(np.clip(median_bfs, 0.001, 100)),
        color=bar_colors, edgecolor="black", alpha=0.85
    )
    ax.axhline(np.log10(3), color="#2196F3", linestyle="--", alpha=0.7, linewidth=1.5,
               label=f"BF₀₁=3 (plateau threshold)")
    ax.axhline(np.log10(1 / 3), color="#F44336", linestyle="--", alpha=0.7, linewidth=1.5,
               label=f"BF₀₁=0.33 (dose-response threshold)")
    ax.axhline(0, color="black", linestyle="-", linewidth=1, alpha=0.5)

    # Legend for classifications
    patches = [
        mpatches.Patch(color="#2196F3", alpha=0.85, label="Plateau (BF₀₁>3)"),
        mpatches.Patch(color="#F44336", alpha=0.85, label="Dose-Responsive (BF₀₁<0.33)"),
        mpatches.Patch(color="#9E9E9E", alpha=0.85, label="Inconclusive"),
    ]
    ax.legend(handles=patches, fontsize=8, loc="upper right")
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels([m.replace("-", "-\n") for m in models], fontsize=9)
    ax.set_ylabel("Median log₁₀(BF₀₁)")
    ax.set_title("Model Classification by Median BF₀₁\n(Plateau vs. Dose-Responsive)")
    ax.grid(True, axis="y", alpha=0.3)

    for i, (bar, val) in enumerate(zip(bars, median_bfs)):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"BF={val:.1f}\n({summary[models[i]]['classification'][:3]})",
            ha="center", va="bottom", fontsize=8,
        )

    fig.suptitle(
        "Robustness Plateau Detection: Statistical Classification Summary",
        fontsize=13, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    if save_path is None:
        save_path = f"{FIGURES_DIR}/classification_summary.png"
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_tost_results(statistical_results: dict, save_path: str = None) -> str:
    """Plot TOST p-values per model × level."""
    classifications = statistical_results.get("classifications", {})
    if not classifications:
        return ""

    models = list(classifications.keys())
    levels = [1, 2, 3, 4]

    tost_matrix = np.zeros((len(models), len(levels)))
    for i, model in enumerate(models):
        level_stats = classifications[model].get("level_statistics", {})
        for j, level in enumerate(levels):
            if level in level_stats:
                tost_matrix[i, j] = level_stats[level]["tost"]["tost_p"]
            elif str(level) in level_stats:
                tost_matrix[i, j] = level_stats[str(level)]["tost"]["tost_p"]
            else:
                tost_matrix[i, j] = 0.5

    fig, ax = plt.subplots(figsize=(8, 4.5))
    cmap = sns.color_palette("RdYlGn", as_cmap=True)
    im = ax.imshow(tost_matrix, cmap=cmap, vmin=0, vmax=0.2, aspect="auto")

    for i in range(len(models)):
        for j in range(len(levels)):
            val = tost_matrix[i, j]
            text = f"p={val:.3f}"
            marker = "✓" if val < 0.05 else "✗"
            ax.text(j, i, f"{marker}\n{text}", ha="center", va="center",
                    fontsize=8.5, fontweight="bold",
                    color="white" if val < 0.03 else "black")

    ax.set_xticks(range(len(levels)))
    ax.set_xticklabels([f"L{l} vs L0" for l in levels])
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_title("TOST P-values per Model × Intervention Level\n"
                 "(✓ p<0.05: evidence for equivalence/plateau; ✗ not significant)")

    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("TOST p-value (green=equivalent, red=not)")
    cbar.ax.axhline(0.05, color="black", linewidth=2)

    fig.tight_layout()
    if save_path is None:
        save_path = f"{FIGURES_DIR}/tost_results.png"
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def generate_all_figures(aggregated: dict, statistical_results: dict) -> list[str]:
    """Generate all visualization figures."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    saved_paths = []

    print("Generating figures...")
    saved_paths.append(plot_dose_response_curves(aggregated))
    saved_paths.append(plot_bayes_factors(statistical_results))
    saved_paths.append(plot_hierarchical_beta(statistical_results.get("hierarchical_bayesian", {})))
    saved_paths.append(plot_classification_summary(statistical_results, aggregated))
    saved_paths.append(plot_tost_results(statistical_results))

    return [p for p in saved_paths if p]
