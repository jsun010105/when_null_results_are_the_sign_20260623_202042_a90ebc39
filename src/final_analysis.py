"""
Final analysis script: re-aggregates all 4 models and regenerates figures + stats.
Run this after all experiment data is collected.
"""

import json
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.experiments import aggregate_results
from src.stat_analysis import run_full_analysis
from src.visualization import (
    plot_dose_response_curves,
    plot_bayes_factors,
    plot_hierarchical_beta,
    plot_classification_summary,
    plot_tost_results,
)


def make_serializable(obj):
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    return obj


def main():
    logger.info("Loading raw responses from checkpoint...")
    with open("results/raw_responses.json") as f:
        results = json.load(f)

    logger.info(f"Total results: {len(results)}")

    # Validate completeness
    from collections import Counter
    model_level_counts = Counter(
        (r["model_label"], r["intervention_level"]) for r in results
    )
    logger.info("Results per model/level:")
    for (model, level), count in sorted(model_level_counts.items()):
        logger.info(f"  {model} | Level {level}: {count}")

    # Aggregate
    logger.info("Aggregating results...")
    aggregated = aggregate_results(results)

    logger.info("Aggregated refusal rates:")
    for model, levels in sorted(aggregated.items()):
        rates = [f"L{l}={levels[str(l)]['refusal_rate']:.3f}" for l in range(5) if str(l) in levels]
        logger.info(f"  {model}: {', '.join(rates)}")

    # Save aggregated
    with open("results/aggregated_results.json", "w") as f:
        json.dump(aggregated, f, indent=2, default=str)
    logger.info("Saved aggregated_results.json")

    # Statistical analysis
    logger.info("Running statistical analysis...")
    stat_results = run_full_analysis(aggregated)

    logger.info("Classification summary:")
    for model, info in stat_results["summary"].items():
        logger.info(
            f"  {model}: {info['classification'].upper()} "
            f"(BF01={info['median_bf01']:.2f}, beta={info['beta_mean']:.3f}, "
            f"baseline={info['baseline_refusal_rate']:.3f})"
        )

    with open("results/statistical_analysis.json", "w") as f:
        json.dump(make_serializable(stat_results), f, indent=2, default=str)
    logger.info("Saved statistical_analysis.json")

    # Regenerate all figures
    logger.info("Generating figures...")
    os.makedirs("figures", exist_ok=True)

    plot_dose_response_curves(aggregated, save_path="figures/dose_response_curves.png")
    logger.info("  dose_response_curves.png")

    plot_bayes_factors(stat_results, save_path="figures/bayes_factors_heatmap.png")
    logger.info("  bayes_factors_heatmap.png")

    plot_hierarchical_beta(stat_results, save_path="figures/hierarchical_beta_forest.png")
    logger.info("  hierarchical_beta_forest.png")

    plot_classification_summary(stat_results, aggregated, save_path="figures/classification_summary.png")
    logger.info("  classification_summary.png")

    plot_tost_results(stat_results, save_path="figures/tost_results.png")
    logger.info("  tost_results.png")

    logger.info("Final analysis complete.")
    return stat_results, aggregated


if __name__ == "__main__":
    main()
