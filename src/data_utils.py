"""
Data loading and sampling utilities for AdvBench dataset.
"""

import csv
import random
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import ADVBENCH_PATH, N_BEHAVIORS, RANDOM_SEED


def load_advbench(path: str = ADVBENCH_PATH) -> list[dict]:
    """Load all behaviors from AdvBench CSV."""
    behaviors = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            behaviors.append({"id": i, "goal": row["goal"], "target": row.get("target", "")})
    return behaviors


def sample_behaviors(behaviors: list[dict], n: int = N_BEHAVIORS, seed: int = RANDOM_SEED) -> list[dict]:
    """Sample n behaviors from AdvBench for the experiment."""
    rng = random.Random(seed)
    # Use all 520 but stratify by position to get diverse coverage across the dataset
    step = len(behaviors) // n
    sampled = []
    for i in range(n):
        idx = i * step + rng.randint(0, step - 1)
        idx = min(idx, len(behaviors) - 1)
        sampled.append(behaviors[idx])
    return sampled


def save_json(data, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    behaviors = load_advbench()
    print(f"Loaded {len(behaviors)} behaviors from AdvBench")
    sampled = sample_behaviors(behaviors)
    print(f"Sampled {len(sampled)} behaviors:")
    for b in sampled[:5]:
        print(f"  [{b['id']}] {b['goal'][:80]}")
