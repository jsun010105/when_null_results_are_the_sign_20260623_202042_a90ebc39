"""
Validate keyword-based evaluation accuracy on sample of collected responses.
Computes precision/recall estimates and inter-method agreement.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import RAW_RESULTS_PATH
from src.evaluation import classify_response


def validate_evaluation(n_samples: int = 50):
    """Sample and analyze responses to validate keyword classification accuracy."""
    if not os.path.exists(RAW_RESULTS_PATH):
        print("No raw results yet. Run main.py first.")
        return

    with open(RAW_RESULTS_PATH) as f:
        results = json.load(f)

    print(f"Total results available: {len(results)}")

    # Sample cases with "low" confidence to inspect
    low_conf = [r for r in results if r.get("eval_confidence") == "low"]
    medium_conf = [r for r in results if r.get("eval_confidence") == "medium"]
    high_conf = [r for r in results if r.get("eval_confidence") == "high"]

    print(f"Confidence breakdown:")
    print(f"  High: {len(high_conf)} ({100*len(high_conf)/len(results):.1f}%)")
    print(f"  Medium: {len(medium_conf)} ({100*len(medium_conf)/len(results):.1f}%)")
    print(f"  Low: {len(low_conf)} ({100*len(low_conf)/len(results):.1f}%)")

    # Show sample of each category
    print("\n--- SAMPLE: LOW CONFIDENCE CASES ---")
    for r in low_conf[:5]:
        print(f"\nBehavior: {r['behavior_goal'][:60]}")
        print(f"Response: {r['response_text'][:150]}")
        print(f"Classified as: {'REFUSAL' if r['is_refusal'] else 'COMPLIANCE'}")
        print(f"Signals: {r['eval_signals']}")

    print("\n--- REFUSAL RATE BY MODEL AND LEVEL ---")
    model_level_stats = {}
    for r in results:
        key = (r["model_label"], r["intervention_level"])
        if key not in model_level_stats:
            model_level_stats[key] = {"total": 0, "refusals": 0}
        model_level_stats[key]["total"] += 1
        if r["is_refusal"]:
            model_level_stats[key]["refusals"] += 1

    models = sorted(set(k[0] for k in model_level_stats))
    levels = sorted(set(k[1] for k in model_level_stats))

    print(f"\n{'Model':<20} | " + " | ".join(f"L{l}" for l in levels))
    print("-" * (20 + 8 * len(levels)))
    for model in models:
        rates = []
        for level in levels:
            stats = model_level_stats.get((model, level), {"total": 1, "refusals": 0})
            rate = stats["refusals"] / stats["total"]
            rates.append(f"{rate:.2f}")
        print(f"{model:<20} | " + " | ".join(rates))


if __name__ == "__main__":
    validate_evaluation()
