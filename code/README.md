# Cloned Repositories

## Repo 1: SAE Post-Intervention Recovery
- **URL**: https://github.com/Mingyuee88/sae-post-intervention-recovery
- **Paper**: "SAE Interventions are Unreliable: Post-Intervention Recovery of Suppressed Behavior" (arXiv 2606.18322)
- **Location**: `code/sae-post-intervention-recovery/`
- **Purpose**: Official implementation of the post-intervention recovery diagnostic. Tests whether SAE feature clamping is a true behavioral bottleneck or bypassable causal handle.
- **Key Files**:
  - `experiments/` — experiment scripts for TPP, WMDP, IOI, and refusal steering
  - `scripts/` — recovery optimization scripts
  - `configs/` — experiment configurations
- **Notes**: The most directly relevant codebase. Implements the null-space projected gradient descent for recovery testing. The recovery rate metric is analogous to the "robustness plateau" metric we aim to formalize statistically.

## Repo 2: Latent Adversarial Training
- **URL**: https://github.com/aengusl/latent-adversarial-training
- **Paper**: "Latent Adversarial Training Improves Robustness to Persistent Harmful Behaviors in LLMs" (arXiv 2407.15549, TMLR 2025)
- **Location**: `code/latent-adversarial-training/`
- **Purpose**: Targeted LAT that perturbs latent activations to train more robust refusal, backdoor removal, and knowledge unlearning.
- **Key Files**:
  - `latent_at/` — main LAT package
  - `notebooks/` — experiment notebooks for jailbreak, backdoor, unlearning experiments
  - `requirements.txt` — dependencies
- **Notes**: Provides both the problem (standard fine-tuning suppresses rather than removes capabilities) and a proposed solution. The "robustness plateau" is the gap LAT aims to close. Can be used to test how much LAT reduces the plateau vs. standard training.

## Repo 3: Representation Engineering
- **URL**: https://github.com/andyzoujm/representation-engineering
- **Paper**: "Representation Engineering: A Top-Down Approach to AI Transparency" (arXiv 2310.01405)
- **Location**: `code/representation-engineering/`
- **Purpose**: Reading vectors from LLM activations and using them to steer model behavior. The primary activation steering intervention technique.
- **Key Files**:
  - `repe/` — core RepE library
  - `examples/` — example scripts for honesty, harmlessness, emotions steering
  - `repe_eval/` — evaluation scripts
- **Notes**: The activation steering magnitude is the primary "intervention strength" variable for our robustness plateau experiments. RepE provides a clean way to parameterize intervention strength from 0 to strong.

## Repo 4: LLM Attacks (AdvBench)
- **URL**: https://github.com/llm-attacks/llm-attacks
- **Paper**: "Universal and Transferable Adversarial Attacks on Aligned Language Models" (Zou et al., 2023)
- **Location**: `code/llm-attacks/`
- **Purpose**: GCG (Greedy Coordinate Gradient) jailbreaking attacks and AdvBench benchmark.
- **Key Files**:
  - `data/advbench/` — AdvBench dataset (harmful_behaviors.csv, harmful_strings.csv)
  - `llm_attacks/` — attack implementation
  - `experiments/` — experiment scripts
- **Notes**: Provides standardized safety evaluation. Can be used to measure attack success rate as the outcome variable for intervention effectiveness tests.

## Repo 5: HarmBench
- **URL**: https://github.com/centerforaisafety/HarmBench
- **Paper**: "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal" (Mazeika et al., 2024)
- **Location**: `code/HarmBench/`
- **Purpose**: Standardized safety evaluation with multiple attack types and a held-out test set.
- **Key Files**:
  - `data/behavior_datasets/` — behavior CSV files
  - `baselines/` — baseline attack implementations (GCG, AutoDAN, etc.)
  - `scripts/` — evaluation scripts
- **Notes**: More comprehensive than AdvBench. Important for cross-benchmark validation of robustness plateau findings.
