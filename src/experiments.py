"""
Experiment runner: apply intervention matrix to models and collect responses.
"""

import json
import os
import sys
import time
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (
    MODELS, INTERVENTION_LEVELS, N_BEHAVIORS, RANDOM_SEED,
    RAW_RESULTS_PATH, RESULTS_DIR, LOGS_DIR,
)
from src.data_utils import load_advbench, sample_behaviors, save_json
from src.api_client import build_client, query_model
from src.evaluation import classify_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/experiments.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def run_experiment(
    resume: bool = True,
    checkpoint_every: int = 10,
) -> list[dict]:
    """
    Run the full intervention matrix experiment.

    For each (model, behavior, intervention_level), query the model and record:
    - Raw response text
    - Classification (refusal/compliance)
    - Metadata (timing, tokens, etc.)

    Returns list of result dicts.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Load and sample behaviors
    behaviors = load_advbench()
    sampled = sample_behaviors(behaviors, n=N_BEHAVIORS, seed=RANDOM_SEED)
    logger.info(f"Sampled {len(sampled)} behaviors from AdvBench")

    # Check for existing results (resume capability)
    existing_results = []
    if resume and os.path.exists(RAW_RESULTS_PATH):
        try:
            existing_results = json.load(open(RAW_RESULTS_PATH))
            logger.info(f"Resuming from {len(existing_results)} existing results")
        except Exception as e:
            logger.warning(f"Could not load existing results: {e}")

    # Build lookup of already-completed (model, behavior_id, level)
    completed = {
        (r["model_id"], r["behavior_id"], r["intervention_level"])
        for r in existing_results
    }

    all_results = list(existing_results)
    client = build_client()

    total_calls = len(MODELS) * len(sampled) * len(INTERVENTION_LEVELS)
    call_count = len(existing_results)

    logger.info(f"Total API calls planned: {total_calls}, already done: {call_count}")
    logger.info(f"Models: {[m['label'] for m in MODELS]}")
    logger.info(f"Intervention levels: {[l['label'] for l in INTERVENTION_LEVELS]}")

    for model_cfg in MODELS:
        model_id = model_cfg["id"]
        model_label = model_cfg["label"]

        for level_cfg in INTERVENTION_LEVELS:
            level = level_cfg["level"]
            system_prompt = level_cfg["system_prompt"]

            for behavior in sampled:
                behavior_id = behavior["id"]
                key = (model_id, behavior_id, level)

                if key in completed:
                    continue  # Skip already completed

                call_count += 1
                logger.info(
                    f"[{call_count}/{total_calls}] {model_label} | Level {level} | "
                    f"Behavior #{behavior_id}: {behavior['goal'][:60]}..."
                )

                t_start = time.time()
                response = query_model(
                    client,
                    model_id=model_id,
                    user_message=behavior["goal"],
                    system_prompt=system_prompt,
                )
                elapsed = time.time() - t_start

                if not response["success"]:
                    logger.warning(f"  API call failed: {response.get('error', 'unknown')}")

                classification = classify_response(
                    response["content"], behavior["goal"]
                )

                result = {
                    "model_id": model_id,
                    "model_label": model_label,
                    "behavior_id": behavior_id,
                    "behavior_goal": behavior["goal"],
                    "intervention_level": level,
                    "intervention_label": level_cfg["label"],
                    "response_text": response["content"][:500],  # Truncate for storage
                    "is_refusal": classification["is_refusal"],
                    "eval_confidence": classification["confidence"],
                    "eval_signals": classification["signals"],
                    "api_success": response["success"],
                    "elapsed_seconds": round(elapsed, 2),
                    "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                    "timestamp": datetime.now().isoformat(),
                }
                all_results.append(result)

                # Checkpoint periodically
                if len(all_results) % checkpoint_every == 0:
                    save_json(all_results, RAW_RESULTS_PATH)
                    logger.info(f"  Checkpoint saved ({len(all_results)} results)")

    # Final save
    save_json(all_results, RAW_RESULTS_PATH)
    logger.info(f"Experiment complete: {len(all_results)} results saved to {RAW_RESULTS_PATH}")
    return all_results


def aggregate_results(results: list[dict]) -> dict:
    """
    Aggregate raw results into refusal rate tables per (model, level).

    Returns dict:
        aggregated[model_label][level] = {
            "refusal_rate": float,
            "n_refusals": int,
            "n_total": int,
            "n_api_success": int,
        }
    """
    aggregated = {}
    for r in results:
        m = r["model_label"]
        l = r["intervention_level"]
        if m not in aggregated:
            aggregated[m] = {}
        if l not in aggregated[m]:
            aggregated[m][l] = {"n_refusals": 0, "n_total": 0, "n_api_success": 0}

        aggregated[m][l]["n_total"] += 1
        aggregated[m][l]["n_api_success"] += int(r["api_success"])
        if r["is_refusal"]:
            aggregated[m][l]["n_refusals"] += 1

    # Compute rates
    for m in aggregated:
        for l in aggregated[m]:
            n = aggregated[m][l]["n_total"]
            r = aggregated[m][l]["n_refusals"]
            aggregated[m][l]["refusal_rate"] = r / n if n > 0 else 0.0

    return aggregated


if __name__ == "__main__":
    import sys
    results = run_experiment(resume=True)
    agg = aggregate_results(results)
    print("\n=== Aggregated Refusal Rates ===")
    for model, levels in agg.items():
        print(f"\n{model}:")
        for level in sorted(levels.keys()):
            d = levels[level]
            print(f"  Level {level}: {d['refusal_rate']:.2f} ({d['n_refusals']}/{d['n_total']})")
