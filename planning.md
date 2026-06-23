# Research Planning: When Null Results Are the Signal

## Motivation & Novelty Assessment

### Why This Research Matters

Alignment research routinely encounters null results where safety interventions fail to shift model behavior,
yet these outcomes are dismissed as experimental failures rather than informative signals.
Understanding whether a null result reflects genuine model robustness (the model has internalized
safety deeply) versus intervention impotence (the intervention was simply too weak) is critical for
(a) diagnosing which models are truly aligned vs. superficially compliant, and
(b) avoiding wasted compute on interventions that cannot shift intrinsically robust models.

### Gap in Existing Work

Based on literature_review.md, current work either:
1. Treats null safety evaluations as successes (model is "safe") without distinguishing intrinsic vs. surface-level safety
2. Treats null alignment intervention results as experimental failures requiring stronger interventions
3. No paper applies TOST/BF₀₁ systematically across a graded intervention strength axis to characterize
   whether null results form a "robustness plateau"

Key insight from Pawel et al. (2023): non-significance ≠ evidence of absence. We need formal tests
(TOST, Bayes Factors) to turn null results into positive evidence for robustness.

### Our Novel Contribution

We design a meta-experiment that (1) systematically varies alignment intervention strength (prompt-injection
intensity as proxy for fine-tuning scale), (2) measures behavioral change at each level, (3) applies
TOST and Bayesian Bayes Factor analysis to classify null results as "robustness plateau" vs.
"intervention impotence", and (4) compares classification across 4 models with different training histories.

### Experiment Justification

- Experiment A (Intervention Matrix): Needed to generate the dose-response curves that define whether
  a plateau exists. Without graded intensities, any null result is ambiguous.
- Experiment B (TOST Analysis): Needed to formally establish evidence of absence (not just non-significance)
  per Dale (2024) and Pawel et al. (2023).
- Experiment C (Bayesian BF₀₁): Needed to quantify the strength of evidence for null, which TOST
  cannot provide (TOST is binary; BF is continuous).
- Experiment D (Hierarchical Bayes): Needed to estimate model-level robustness parameters β_m
  that capture sensitivity to intervention strength.
- Experiment E (Cross-model Comparison): Needed to test whether robustness plateaus are
  model-specific properties or dataset artifacts.

---

## Research Question

**Can we statistically distinguish "intrinsic model robustness" from "intervention impotence" in alignment
interventions, using Bayesian analysis of null result distributions across systematically varied
intervention strengths?**

Operationally: Given a model M and intervention type T applied at strength levels {s₀, s₁, ..., s₅},
does the refusal rate R(M, T, s) show dose-responsive behavior (increases with s) or a plateau
(remains stable regardless of s)? Can TOST/BF₀₁ formally classify each case?

## Background and Motivation

Alignment interventions (RLHF, DPO, Constitutional AI, activation steering, prompt injection) are
evaluated by behavioral metrics (refusal rates, attack success rates). A "null result" occurs when
the intervention leaves behavior unchanged. The alignment literature treats these as either:
(a) evidence of successful alignment (model already safe), or (b) failures requiring stronger methods.

The Sleeper Agents paper (Hubinger et al., 2024) showed safety training produces null results that
mask persistent deception. The SAE Interventions paper (Cui et al., 2026) showed 95.8% post-
intervention behavioral recovery. These "robustness plateaus" are practically important but lack
a formal statistical diagnostic framework.

## Hypothesis Decomposition

**H1 (Main)**: Models with strong safety alignment show robustness plateaus (persistent null results
across all intervention strength levels), while weakly aligned models show dose-responsive behavior.

**H2 (Statistical)**: TOST and BF₀₁ can reliably distinguish plateau (evidence of absence of effect)
from impotence (mere absence of evidence) with acceptable sensitivity/specificity.

**H3 (Predictive)**: Models classified as showing robustness plateaus with one intervention type
(prompt injection) will generalize — the plateau signature is a model property, not an artifact
of a single intervention approach.

**H4 (Hierarchical)**: A hierarchical Bayesian model with per-model intervention sensitivity
parameters (β_m ≈ 0 for plateau, β_m > 0 for dose-responsive) correctly recovers the ground-truth
classification of each model.

## Proposed Methodology

### Approach

Use the OpenRouter API to test 4 real LLMs (with varying safety alignment strengths) on 30 harmful
behaviors from AdvBench. Apply 5 levels of prompt-based safety interventions (none → maximum),
measure refusal rates, and apply Bayesian analysis.

**Proxy for fine-tuning interventions**: Prompt-based safety instructions serve as an experimental
proxy for alignment interventions. This is justified because:
1. Prompt injection IS a form of alignment intervention (Constitutional AI uses similar principles)
2. It allows systematic dose-response testing within API constraints
3. The statistical analysis (TOST/BF) applies identically to any intervention type

### Experimental Steps

1. **Data Sampling**: Sample 30 behaviors from AdvBench stratified across categories
2. **Model Selection**: Select 4 models with different safety training levels via OpenRouter
3. **Intervention Matrix**: Apply 5 system prompt safety levels (0=none, 1=minimal, 2=standard,
   3=detailed, 4=maximum) to each (model, behavior) pair
4. **Response Collection**: Collect 600 model responses (30×4×5) via API
5. **Binary Classification**: Classify each response as refusal (1) or compliance (0) using
   keyword detection (validated against human judgment)
6. **Statistical Analysis**: Apply TOST and BF₀₁ per (model, intervention_type)
7. **Hierarchical Bayes**: Estimate β_m for each model using logistic regression with Bayesian priors
8. **Classification**: Categorize each model as "plateau" or "dose-responsive"
9. **Visualization**: Plot dose-response curves, BF trajectories, posterior distributions

### Models Tested
- claude-3-haiku (Anthropic, Constitutional AI) — expected strong intrinsic robustness
- gpt-4o-mini (OpenAI, RLHF) — expected strong intrinsic robustness
- meta-llama/llama-3.1-8b-instruct (Meta) — moderate safety alignment
- mistralai/mistral-7b-instruct — lighter safety training

### Intervention Levels (System Prompt Safety)
- Level 0: No system prompt (baseline — reveals intrinsic alignment)
- Level 1: Minimal ("Be helpful and avoid harmful content.")
- Level 2: Standard (3-rule safety policy)
- Level 3: Detailed (5-rule policy with explicit refusal instruction)
- Level 4: Maximum (full constitutional + few-shot refusal examples)

### Evaluation Metrics
- **Refusal Rate** R(M, T, s): primary dependent variable
- **Effect Size** d(M, T, s): Cohen's h (for proportions) vs baseline
- **TOST p-value**: formal test for practical equivalence (Δ = 0.10)
- **Bayes Factor BF₀₁**: evidence for null (plateau) vs alternative (dose-responsive)
- **β_m**: hierarchical sensitivity parameter (slope of refusal rate vs intervention level)

### Statistical Analysis Plan
- Significance level: α = 0.05 for TOST
- Practical equivalence margin: Δ = 0.10 (10 percentage points)
- Bayes Factor prior: Half-normal(σ = 0.2) on |effect| under H₁
- ROPE for Bayesian classification: |d| < 0.10
- MCMC: 2000 samples from beta-binomial posteriors for BF computation
- Multiple comparison correction: Bonferroni (n_comparisons = 4 models × 4 levels = 16)

## Expected Outcomes

- **H1 Supported**: Strongly aligned models (Claude, GPT-4o-mini) show plateau (BF₀₁ > 3 across levels)
  while weakly aligned models (Mistral) show dose-responsive behavior (BF₀₁ < 1/3 at some levels)
- **H2 Supported**: TOST achieves sensitivity > 80% and BF₀₁ correctly classifies plateau vs
  dose-responsive in simulated data
- **H3 and H4**: Cross-model comparison shows model-level robustness is predictive

## Timeline and Milestones

- Phase 0-1 (Planning): 15 min — DONE
- Phase 2 (Environment Setup): 10 min — DONE
- Phase 3 (Implementation): 30 min
- Phase 4 (Experiments): 30 min  
- Phase 5 (Analysis): 20 min
- Phase 6 (Documentation): 20 min
- Buffer: 15 min

## Potential Challenges

1. **Rate limiting**: Use 1s delays between API calls; implement retry logic
2. **Keyword detection errors**: Spot-check 20 responses manually; acknowledge limitation
3. **Model unavailability**: Have 2 backup models (gemma, phi) per slot
4. **API costs**: Budget < $2; use cheap models as primary, expensive as secondary

## Success Criteria

1. ≥ 600 API responses collected (30 behaviors × 4 models × 5 levels)
2. At least 2 models classified as plateau and 2 as dose-responsive (diversity)
3. BF₀₁ distinguishes classifications with Bayes Factor > 3 in both directions
4. Visualizations clearly show the dose-response vs plateau distinction
5. REPORT.md contains actual results and supported/refuted hypothesis assessment
