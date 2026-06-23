"""
Main orchestrator for the null-results-as-signal alignment study.

Runs all phases:
1. Data sampling
2. API experiments (intervention matrix)
3. Statistical analysis
4. Visualization
5. Results saving
"""

import sys
import os
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import (
    RAW_RESULTS_PATH, AGGREGATED_RESULTS_PATH, STATISTICAL_RESULTS_PATH,
    RESULTS_DIR, FIGURES_DIR, LOGS_DIR, RANDOM_SEED, MODELS, INTERVENTION_LEVELS,
)
from src.data_utils import load_advbench, sample_behaviors, save_json
from src.experiments import run_experiment, aggregate_results
from src.stat_analysis import run_full_analysis
from src.visualization import generate_all_figures
from src.evaluation import classify_response

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/main.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def main():
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("NULL RESULTS AS SIGNAL — Alignment Robustness Study")
    logger.info(f"Started: {start_time.isoformat()}")
    logger.info("=" * 60)

    # Phase 1: Data preparation
    logger.info("\n[Phase 1] Loading and sampling behaviors...")
    behaviors = load_advbench()
    sampled = sample_behaviors(behaviors)
    logger.info(f"  Using {len(sampled)} behaviors from AdvBench (seed={RANDOM_SEED})")
    save_json([b["goal"] for b in sampled], f"{RESULTS_DIR}/sampled_behaviors.json")

    # Phase 2: Run experiments
    logger.info("\n[Phase 2] Running intervention matrix experiments...")
    logger.info(f"  Models: {[m['label'] for m in MODELS]}")
    logger.info(f"  Intervention levels: {len(INTERVENTION_LEVELS)}")
    logger.info(f"  Total API calls: {len(MODELS) * len(sampled) * len(INTERVENTION_LEVELS)}")

    results = run_experiment(resume=True)
    logger.info(f"  Collected {len(results)} responses")

    # Phase 3: Aggregate
    logger.info("\n[Phase 3] Aggregating results...")
    aggregated = aggregate_results(results)
    save_json(aggregated, AGGREGATED_RESULTS_PATH)

    # Print summary table
    logger.info("\n  === Refusal Rate Summary ===")
    for model in aggregated:
        rates = [aggregated[model].get(l, {}).get("refusal_rate", 0.0)
                 for l in sorted(aggregated[model].keys())]
        rate_str = " | ".join(f"{r:.2f}" for r in rates)
        logger.info(f"  {model}: {rate_str}")

    # Phase 4: Statistical analysis
    logger.info("\n[Phase 4] Running statistical analysis...")
    statistical_results = run_full_analysis(aggregated)
    save_json(statistical_results, STATISTICAL_RESULTS_PATH)

    logger.info("\n  === Model Classifications ===")
    for model, info in statistical_results["summary"].items():
        logger.info(
            f"  {model}: {info['classification'].upper()} "
            f"(BF₀₁={info['median_bf01']:.2f}, β={info['beta_mean']:.2f}, "
            f"baseline_refusal={info['baseline_refusal_rate']:.2f})"
        )

    # Phase 5: Visualization
    logger.info("\n[Phase 5] Generating figures...")
    figure_paths = generate_all_figures(aggregated, statistical_results)
    logger.info(f"  Generated {len(figure_paths)} figures")

    # Phase 6: Save config and metadata
    metadata = {
        "timestamp": start_time.isoformat(),
        "runtime_seconds": (datetime.now() - start_time).total_seconds(),
        "n_behaviors": len(sampled),
        "n_models": len(MODELS),
        "n_intervention_levels": len(INTERVENTION_LEVELS),
        "n_total_responses": len(results),
        "n_api_successes": sum(1 for r in results if r.get("api_success", False)),
        "seed": RANDOM_SEED,
        "models": [m["label"] for m in MODELS],
        "figure_paths": figure_paths,
        "results_files": {
            "raw_responses": RAW_RESULTS_PATH,
            "aggregated": AGGREGATED_RESULTS_PATH,
            "statistical": STATISTICAL_RESULTS_PATH,
        },
    }
    save_json(metadata, f"{RESULTS_DIR}/metadata.json")

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"\n[COMPLETE] Total runtime: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    logger.info(f"Results saved to: {RESULTS_DIR}/")
    logger.info(f"Figures saved to: {FIGURES_DIR}/")

    return statistical_results, aggregated


if __name__ == "__main__":
    statistical_results, aggregated = main()
