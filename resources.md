# Resources Catalog

## Summary

This document catalogs all resources gathered for "When Null Results Are the Signal: A Meta-Experimental Approach to Diagnosing Hidden Robustness in Alignment Interventions."

---

## Papers

Total papers downloaded: 28

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| SAE Interventions are Unreliable | Cui, Shen, Yang | 2026 | papers/2606.18322v1_SAE_Interventions_Unreliable_Post_Recovery.pdf | Robustness plateaus via post-intervention recovery; 95.8% recovery rate |
| Confirming the Null: Equivalence Testing | Dale | 2024 | papers/2405.16331v1_Confirming_Null_Equivalence_Testing.pdf | Formal topology of null confirmation; TOST model of severe testing |
| Replication of null results | Pawel et al. | 2023 | papers/2305.04587v3_Replication_Null_Results_Absence_Evidence.pdf | TOST + BF₀₁ for null result analysis; RPCB data analysis |
| Computational Safety GenAI | Multiple | 2025 | papers/2502.12445v2_Computational_Safety_GenAI_Hypothesis_Testing.pdf | AI safety as hypothesis testing |
| Latent Adversarial Training | Sheshadri et al. | 2024/25 | papers/2407.15549v3_Latent_Adversarial_Training_Robustness_LLM.pdf | Suppression vs removal; targeted LAT improves robustness |
| Sleeper Agents | Hubinger et al. | 2024 | papers/2401.05566v3_Sleeper_Agents_Deceptive_LLMs_Safety_Training.pdf | Safety training fails to remove deceptive behaviors |
| Fine-tuning Compromises Safety | Qi et al. | 2023 | papers/2310.03693v1_Finetuning_Aligned_LLMs_Compromises_Safety.pdf | Benign fine-tuning degrades alignment |
| Representation Engineering | Zou et al. | 2023 | papers/2310.01405v4_Representation_Engineering_AI_Transparency.pdf | RepE reading vectors; activation steering technique |
| Constitutional AI | Anthropic | 2022 | papers/2212.08073v1_Constitutional_AI_Harmlessness.pdf | CAI: self-critique alignment method |
| InstructGPT / RLHF | Ouyang et al. | 2022 | papers/2203.02155v1_InstructGPT_RLHF_Training.pdf | Foundational RLHF alignment |
| Direct Preference Optimization | Rafailov et al. | 2023 | papers/2305.18290v3_DPO_Direct_Preference_Optimization.pdf | DPO: simpler RLHF alternative |
| Safety Alignment >Few Tokens Deep | Qi et al. | 2024 | papers/2406.05946v1_Safety_Alignment_More_Than_Few_Tokens_Deep.pdf | Safety shortcuts; first-token pattern matching |
| LoRA Undoes Safety Training | Lermen et al. | 2023 | papers/2310.20624v2_LoRA_Undoes_Safety_Training_Llama2.pdf | $200 removes 70B safety alignment |
| Meta-analysis of Bayesian Analyses | Multiple | 2019 | papers/1904.04484v2_Meta_Analysis_Bayesian_Analyses.pdf | Framework for combining Bayesian posteriors |
| Bayes Factors for Peri-Null | Multiple | 2021 | papers/2102.07162v2_Bayes_Factors_Peri_Null_Hypotheses.pdf | BF for near-null hypotheses |
| Bayes Factor and ROPE | Multiple | 2019 | papers/1903.03153v2_Bayes_Factor_ROPE_Interval_Null.pdf | TOST/ROPE dual approach |
| Safety Training Persists in Agents | Multiple | 2026 | papers/2603.02229v1_Safety_Training_Persists_Helpfulness_Optimization.pdf | Counter-example: safety persists in agentic settings |
| Geometry of Alignment Collapse | Multiple | 2026 | papers/2602.15799v1_Geometry_Alignment_Collapse_Finetuning_Safety.pdf | Geometric mechanism of safety collapse |
| Why Safety Guardrails Collapse | Multiple | 2025 | papers/2506.05346v1_Why_LLM_Safety_Guardrails_Collapse_Finetuning.pdf | Similarity analysis of alignment vs fine-tuning |
| LLM Probability Concentration | Multiple | 2025 | papers/2506.17871v3_LLM_Probability_Concentration_Alignment.pdf | Alignment shrinks generative diversity |
| Control RL Token Steering SAE | Multiple | 2026 | papers/2506.18322v1_Control_RL_Token_Steering_LLMs_SAE.pdf | RL-based SAE feature steering |
| Safety Layers Key to Security | Multiple | 2024 | papers/2408.17003v5_Safety_Layers_Aligned_LLMs_Key_Security.pdf | Layer-specific safety storage |
| Reverse-Bayes Evidence Assessment | Multiple | 2021 | papers/2102.13443v2_Reverse_Bayes_Evidence_Assessment_Research_Synthesis.pdf | Prior sensitivity for null confirmation |
| Accuracy Bayes Factor Tests | Multiple | 2024 | papers/2406.08022v2_Accuracy_Bayes_Factor_Null_Hypothesis_Tests.pdf | Simulation validation of BF methods |
| Baseline Defenses Adversarial LLMs | Jain et al. | 2023 | papers/2309.00614v2_Baseline_Defenses_Adversarial_Attacks_Aligned_LLMs.pdf | Perplexity filter and other defenses |
| Safety-Tuned LLaMAs | Bianchi et al. | 2023 | papers/2309.07875v3_Safety_Tuned_LLaMAs_Improving_Safety.pdf | Systematic safety tuning study |
| How to Use Activation Patching | Multiple | 2024 | papers/2404.15255v1_How_Use_Interpret_Activation_Patching.pdf | Mechanistic intervention methodology |
| LLM-as-Judge Evaluation | Multiple | 2024 | papers/2408.13006v2_Systematic_Evaluation_LLM_as_Judge_Alignment.pdf | Automated alignment evaluation |

See papers/README.md for detailed descriptions.

---

## Datasets

Total datasets downloaded: 6

| Name | Source | Size | Task | Location | Status |
|------|--------|------|------|----------|--------|
| Anthropic HH-RLHF | HuggingFace | 160,800 train | Safety preference learning | datasets/hh_rlhf/samples.json | Samples saved; full via HF |
| PKU-SafeRLHF | HuggingFace | 73,907 train | Safety-aware preference | datasets/pku_safe_rlhf/samples.json | Samples saved; full via HF |
| TruthfulQA | HuggingFace | 817 validation | Truthfulness evaluation | datasets/truthfulqa/samples.json | Samples saved; full via HF |
| Toxic-Chat | HuggingFace | 10,165 total | Toxicity detection | datasets/toxic_chat/samples.json | Samples saved; full via HF |
| AdvBench | GitHub CSV | 520 behaviors | Safety red-teaming | datasets/advbench/harmful_behaviors.csv | ✓ LOCALLY AVAILABLE |
| HarmBench | GitHub CSV | 1,214 behaviors | Comprehensive safety eval | datasets/harmbench/harmbench_test.csv | ✓ LOCALLY AVAILABLE |

See datasets/README.md for detailed descriptions and download instructions.

---

## Code Repositories

Total repositories cloned: 5

| Name | URL | Purpose | Location | Key Files |
|------|-----|---------|----------|-----------|
| sae-post-intervention-recovery | github.com/Mingyuee88/sae-post-intervention-recovery | Official impl of post-intervention recovery diagnostic (CORE) | code/sae-post-intervention-recovery/ | experiments/, scripts/, configs/ |
| latent-adversarial-training | github.com/aengusl/latent-adversarial-training | Targeted LAT for robust alignment | code/latent-adversarial-training/ | latent_at/, notebooks/ |
| representation-engineering | github.com/andyzoujm/representation-engineering | RepE activation steering | code/representation-engineering/ | repe/, examples/ |
| llm-attacks | github.com/llm-attacks/llm-attacks | GCG attacks + AdvBench | code/llm-attacks/ | data/advbench/, llm_attacks/ |
| HarmBench | github.com/centerforaisafety/HarmBench | Comprehensive safety evaluation | code/HarmBench/ | data/behavior_datasets/, baselines/ |

See code/README.md for detailed descriptions.

---

## Resource Gathering Notes

### Search Strategy
- Used arXiv Python library to search 16 targeted queries across: alignment intervention robustness, SAE/activation interventions, Bayesian null hypothesis testing, equivalence testing, safety fine-tuning fragility, meta-analysis methods
- Manual lookup of foundational papers by known arXiv ID (InstructGPT, DPO, Constitutional AI, Representation Engineering, Sleeper Agents)
- GitHub search for repositories from paper code links
- HuggingFace datasets search for standard alignment benchmarks

### Selection Criteria
Papers were selected for:
1. **Direct relevance**: Papers about alignment intervention effectiveness, robustness, or null result statistical methods
2. **Methodological value**: Papers providing techniques usable in the experiment (activation steering, SAE clamping, Bayes factors, TOST)
3. **Foundational importance**: Seminal alignment papers (InstructGPT, DPO, ConstitutionalAI) as experimental baselines
4. **Recency**: Preferring 2023-2026 papers for state-of-the-art

### Challenges Encountered
- Paper-finder service not available; used direct arXiv API
- Some datasets (walledai/AdvBench) gated on HuggingFace; obtained AdvBench via GitHub directly
- WMDP benchmark requires Anthropic/WMDP download which requires authentication; not downloaded but documented

### Gaps and Workarounds
- **WMDP dataset**: The Weapons of Mass Destruction Proxy benchmark used in the LAT paper would be ideal; download requires HF authentication. Experiment runner should download with `load_dataset("cais/wmdp")`
- **SAEBench**: The SAE evaluation benchmark from the SAE interventions paper; not publicly available yet as of search date

---

## Recommendations for Experiment Design

### 1. Primary Datasets
- **AdvBench** (locally at datasets/advbench/harmful_behaviors.csv): 520 behaviors, standard safety benchmark
- **HarmBench** (locally at datasets/harmbench/harmbench_test.csv): 1,214 behaviors, comprehensive categories
- Use **Attack Success Rate (ASR)** as primary dependent variable

### 2. Intervention Axes to Vary Systematically
- **DPO training**: β ∈ {0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0} on Llama3-8B
- **Activation Steering (RepE)**: α (coefficient) ∈ {0, 1, 5, 10, 20, 50, 100} using representation-engineering repo
- **SAE Feature Clamping**: K (number of features) ∈ {1, 5, 10, 20, 50} using sae-post-intervention-recovery repo

### 3. Statistical Analysis Pipeline
For each (model, intervention_type, strength_level):
1. Compute ASR on AdvBench/HarmBench
2. Compute Cohen's d effect size vs. no-intervention baseline
3. Apply TOST with Δ = 0.05 (5% practical equivalence) to test for evidence of null
4. Compute BF₀₁ with half-normal prior (σ = 0.2) on |d| under H₁
5. Classify: BF₀₁ > 3 → robustness plateau; BF₀₁ < 1/3 → dose-responsive

### 4. Meta-Analysis
- Aggregate BF₀₁ values across strength levels within each (model, intervention_type) pair
- Use hierarchical Bayesian model to estimate robustness probability as a latent variable
- Test predictive validity: does plateau for DPO predict plateau for activation steering?

### 5. Code to Adapt
- Start with `code/sae-post-intervention-recovery/experiments/` for the SAE intervention arm
- Start with `code/representation-engineering/examples/` for activation steering arm
- Implement DPO training arm from scratch using `transformers + trl`
