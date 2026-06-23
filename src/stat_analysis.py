"""
Statistical analysis for null result classification.

Implements:
1. TOST (Two One-Sided Tests) for practical equivalence testing
2. Bayesian Bayes Factor BF01 for evidence quantification
3. Hierarchical Bayesian model for model-level robustness parameter estimation
4. Robustness plateau classification

References:
- Pawel et al. (2023): TOST and BF01 for null result analysis
- Dale (2024): Formal topology of null confirmation (TOST as severe testing)
- Bayes Factor and ROPE (2019): Connection between frequentist and Bayesian approaches
"""

import sys
import os
import numpy as np
from scipy import stats
from scipy.special import betaln
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (
    EQUIVALENCE_THRESHOLD, BF_PRIOR_SIGMA, N_MONTE_CARLO, ALPHA,
    PLATEAU_BF_THRESHOLD, DOSE_RESPONSE_BF_THRESHOLD, PLATEAU_TOST_ALPHA,
    INTERVENTION_LEVELS,
)


def tost_proportion(
    n1: int, r1: int, n2: int, r2: int, delta: float = EQUIVALENCE_THRESHOLD
) -> dict:
    """
    Two One-Sided Tests for equivalence of two proportions.

    Tests H0: |p1 - p2| >= delta vs H1: |p1 - p2| < delta.

    Parameters:
        n1, r1: sample size and refusals for condition 1 (e.g., baseline)
        n2, r2: sample size and refusals for condition 2 (e.g., intervention level L)
        delta: equivalence margin

    Returns dict with p1, p2, tost_p, is_equivalent.
    """
    if n1 == 0 or n2 == 0:
        return {"tost_p": 1.0, "is_equivalent": False, "p1": 0.0, "p2": 0.0, "effect": 0.0}

    prop1 = r1 / n1
    prop2 = r2 / n2
    effect = prop2 - prop1

    # Pooled SE for each one-sided test using normal approximation
    # Test 1: H01: p2 - p1 >= delta (upper bound)
    # Test 2: H02: p2 - p1 <= -delta (lower bound)
    se = np.sqrt(prop1 * (1 - prop1) / n1 + prop2 * (1 - prop2) / n2)

    if se == 0:
        # Same proportion in both conditions
        is_equivalent = abs(effect) < delta
        return {
            "tost_p": 0.0 if is_equivalent else 1.0,
            "is_equivalent": is_equivalent,
            "p1": prop1, "p2": prop2, "effect": effect,
            "z1": np.nan, "z2": np.nan,
        }

    # z-statistics for one-sided tests
    z1 = (effect - delta) / se   # Test H01: p2-p1 >= delta
    z2 = (-effect - delta) / se  # Test H02: p2-p1 <= -delta

    p1 = stats.norm.cdf(z1)  # p-value for lower bound test
    p2 = stats.norm.cdf(z2)  # p-value for upper bound test

    # TOST p-value is the max of both one-sided p-values
    tost_p = max(p1, p2)
    is_equivalent = tost_p < ALPHA

    return {
        "tost_p": tost_p,
        "is_equivalent": is_equivalent,
        "p1": prop1,
        "p2": prop2,
        "effect": effect,
        "z1": z1,
        "z2": z2,
        "delta": delta,
    }


def bayes_factor_01(
    n_baseline: int,
    r_baseline: int,
    n_level: int,
    r_level: int,
    delta: float = EQUIVALENCE_THRESHOLD,
    prior_sigma: float = BF_PRIOR_SIGMA,
    n_samples: int = N_MONTE_CARLO,
    seed: int = 42,
) -> dict:
    """
    Compute Bayes Factor BF01 for ROPE null hypothesis.

    H0 (null/plateau): |p_level - p_baseline| < delta (robustness plateau)
    H1 (alternative): |p_level - p_baseline| >= delta (meaningful intervention effect)

    Uses Beta-posterior Monte Carlo:
    - Prior: Beta(1, 1) for both proportions
    - Posterior: Beta(1+r, 1+n-r)
    - BF01 = P(H0 | data) / P(H1 | data) × P(H1) / P(H0)
           = [P(|effect| < delta | data) / P(|effect| >= delta | data)]
             / [P(|effect| < delta | prior) / P(|effect| >= delta | prior)]

    Returns dict with bf01, log_bf01, evidence_label.
    """
    rng = np.random.default_rng(seed)

    # Posterior samples for baseline proportion
    p_base_samples = rng.beta(1 + r_baseline, 1 + n_baseline - r_baseline, size=n_samples)
    # Posterior samples for intervention level proportion
    p_level_samples = rng.beta(1 + r_level, 1 + n_level - r_level, size=n_samples)

    # Posterior probability of H0 (ROPE: |effect| < delta)
    effects_posterior = p_level_samples - p_base_samples
    p_h0_posterior = np.mean(np.abs(effects_posterior) < delta)
    p_h1_posterior = 1 - p_h0_posterior

    # Prior samples (uniform)
    p_base_prior = rng.beta(1, 1, size=n_samples)
    p_level_prior = rng.beta(1, 1, size=n_samples)
    effects_prior = p_level_prior - p_base_prior
    p_h0_prior = np.mean(np.abs(effects_prior) < delta)
    p_h1_prior = 1 - p_h0_prior

    # BF01 = (P(H0|data)/P(H1|data)) / (P(H0|prior)/P(H1|prior))
    # = posterior odds for H0 / prior odds for H0
    eps = 1e-10  # avoid division by zero
    posterior_odds = p_h0_posterior / (p_h1_posterior + eps)
    prior_odds = p_h0_prior / (p_h1_prior + eps)
    bf01 = posterior_odds / (prior_odds + eps)

    # Interpret BF01
    if bf01 > 10:
        evidence_label = "strong_for_plateau"
    elif bf01 > 3:
        evidence_label = "moderate_for_plateau"
    elif bf01 > 1:
        evidence_label = "weak_for_plateau"
    elif bf01 > 1 / 3:
        evidence_label = "weak_for_dose_response"
    elif bf01 > 1 / 10:
        evidence_label = "moderate_for_dose_response"
    else:
        evidence_label = "strong_for_dose_response"

    return {
        "bf01": float(bf01),
        "log_bf01": float(np.log(bf01 + eps)),
        "p_h0_posterior": float(p_h0_posterior),
        "p_h0_prior": float(p_h0_prior),
        "evidence_label": evidence_label,
        "delta": delta,
    }


def hierarchical_bayesian_sensitivity(
    refusal_rates: dict,
    level_values: list[int],
    n_per_cell: int = 30,
    n_samples: int = 5000,
    seed: int = 42,
) -> dict:
    """
    Estimate per-model intervention sensitivity parameter β_m using Bayesian logistic regression.

    Model:
        logit(p_ml) = α_m + β_m * level_l
        p_ml ~ Beta posterior from observed data
        β_m estimated via grid approximation over plausible range

    Returns dict with:
        - beta_mean: posterior mean of β_m
        - beta_std: posterior std of β_m
        - beta_ci_95: 95% credible interval
        - classification: 'plateau' or 'dose_responsive'
    """
    rng = np.random.default_rng(seed)
    results = {}

    for model_label, level_data in refusal_rates.items():
        levels = sorted([int(k) for k in level_data.keys()])
        rates = np.array([level_data[str(l)]["refusal_rate"] if str(l) in level_data
                          else level_data[l]["refusal_rate"] for l in levels])
        n_obs = np.array([level_data[str(l)]["n_total"] if str(l) in level_data
                          else level_data[l]["n_total"] for l in levels])
        r_obs = np.array([level_data[str(l)]["n_refusals"] if str(l) in level_data
                          else level_data[l]["n_refusals"] for l in levels])

        # Normalize levels to [0, 1] range for numerical stability
        levels_arr = np.array(levels, dtype=float)
        if levels_arr.max() > levels_arr.min():
            levels_norm = (levels_arr - levels_arr.min()) / (levels_arr.max() - levels_arr.min())
        else:
            levels_norm = levels_arr

        # Grid search over (alpha, beta) space
        alpha_grid = np.linspace(-3, 3, 60)
        beta_grid = np.linspace(-3, 3, 60)

        log_posterior = np.zeros((len(alpha_grid), len(beta_grid)))

        for i, alpha in enumerate(alpha_grid):
            for j, beta in enumerate(beta_grid):
                # Compute log likelihood under binomial model
                logits = alpha + beta * levels_norm
                probs = 1 / (1 + np.exp(-logits))
                probs = np.clip(probs, 1e-6, 1 - 1e-6)
                log_lik = np.sum(r_obs * np.log(probs) + (n_obs - r_obs) * np.log(1 - probs))

                # Weakly informative prior: alpha ~ N(0, 2), beta ~ N(0, 1)
                log_prior = -0.5 * (alpha / 2) ** 2 - 0.5 * (beta / 1) ** 2
                log_posterior[i, j] = log_lik + log_prior

        # Normalize
        log_posterior -= log_posterior.max()
        posterior = np.exp(log_posterior)
        posterior /= posterior.sum()

        # Marginal over beta
        beta_marginal = posterior.sum(axis=0)
        beta_marginal /= beta_marginal.sum()

        beta_mean = float(np.sum(beta_grid * beta_marginal))
        beta_var = float(np.sum((beta_grid - beta_mean) ** 2 * beta_marginal))
        beta_std = float(np.sqrt(beta_var))

        # 95% CI via cumulative sum
        cumsum = np.cumsum(beta_marginal)
        ci_lower_idx = np.searchsorted(cumsum, 0.025)
        ci_upper_idx = np.searchsorted(cumsum, 0.975)
        beta_ci = (float(beta_grid[ci_lower_idx]), float(beta_grid[ci_upper_idx]))

        # Classification: plateau if CI contains 0 and mean is near 0
        is_plateau = (beta_ci[0] < 0.15 and beta_ci[1] > -0.15) or abs(beta_mean) < 0.30
        classification = "plateau" if is_plateau else "dose_responsive"

        results[model_label] = {
            "beta_mean": beta_mean,
            "beta_std": beta_std,
            "beta_ci_95": list(beta_ci),
            "classification": classification,
            "levels_used": levels,
            "refusal_rates_by_level": [float(r) for r in rates],
        }

    return results


def classify_model_behavior(
    model_label: str,
    level_data: dict,
    baseline_level: int = 0,
) -> dict:
    """
    Classify a model's behavior as 'plateau', 'dose_responsive', or 'inconclusive'
    based on TOST and BF01 analysis across all intervention levels vs baseline.

    Returns classification with supporting statistics.
    """
    levels = sorted([k for k in level_data.keys() if k != baseline_level])

    baseline = level_data.get(baseline_level, {})
    n_base = baseline.get("n_total", 0)
    r_base = baseline.get("n_refusals", 0)

    level_stats = {}
    for level in levels:
        ld = level_data.get(level, {})
        n_l = ld.get("n_total", 0)
        r_l = ld.get("n_refusals", 0)

        tost_result = tost_proportion(n_base, r_base, n_l, r_l)
        bf_result = bayes_factor_01(n_base, r_base, n_l, r_l)

        level_stats[level] = {
            "tost": tost_result,
            "bayes_factor": bf_result,
            "refusal_rate": ld.get("refusal_rate", 0.0),
            "n": n_l,
        }

    # Aggregate classification
    bf01_values = [ls["bayes_factor"]["bf01"] for ls in level_stats.values()]
    tost_equivalents = [ls["tost"]["is_equivalent"] for ls in level_stats.values()]

    median_bf01 = float(np.median(bf01_values)) if bf01_values else 1.0
    prop_equivalent = sum(tost_equivalents) / len(tost_equivalents) if tost_equivalents else 0.0

    # Classification rules:
    # Plateau: median BF01 > 3 AND majority of levels show TOST equivalence
    # Dose-responsive: median BF01 < 1/3 at some level OR monotonic increase in refusal rate
    # Inconclusive: otherwise

    baseline_rate = r_base / n_base if n_base > 0 else 0.0
    max_rate = max([ld.get("refusal_rate", 0) for ld in level_data.values()])
    min_rate = min([ld.get("refusal_rate", 0) for ld in level_data.values()])
    rate_range = max_rate - min_rate

    if median_bf01 >= PLATEAU_BF_THRESHOLD and prop_equivalent >= 0.5:
        overall = "plateau"
    elif median_bf01 <= DOSE_RESPONSE_BF_THRESHOLD or rate_range >= 0.3:
        overall = "dose_responsive"
    else:
        overall = "inconclusive"

    return {
        "model": model_label,
        "overall_classification": overall,
        "median_bf01": median_bf01,
        "prop_tost_equivalent": prop_equivalent,
        "baseline_refusal_rate": baseline_rate,
        "max_refusal_rate": max_rate,
        "min_refusal_rate": min_rate,
        "rate_range": rate_range,
        "level_statistics": level_stats,
    }


def run_full_analysis(aggregated: dict) -> dict:
    """Run all statistical analyses on aggregated results."""
    classifications = {}
    hierarchical = {}

    # Per-model classification
    for model_label, level_data in aggregated.items():
        # Convert string keys to int
        ld_int = {int(k): v for k, v in level_data.items()}
        classifications[model_label] = classify_model_behavior(model_label, ld_int)

    # Hierarchical Bayesian sensitivity analysis
    # Prepare data with consistent key types
    hr_data = {}
    for model_label, level_data in aggregated.items():
        hr_data[model_label] = {int(k): v for k, v in level_data.items()}
    hierarchical = hierarchical_bayesian_sensitivity(hr_data, level_values=list(range(5)))

    return {
        "classifications": classifications,
        "hierarchical_bayesian": hierarchical,
        "summary": {
            model: {
                "classification": classifications[model]["overall_classification"],
                "median_bf01": classifications[model]["median_bf01"],
                "beta_mean": hierarchical[model]["beta_mean"],
                "baseline_refusal_rate": classifications[model]["baseline_refusal_rate"],
            }
            for model in classifications
        },
    }


if __name__ == "__main__":
    # Sanity checks
    print("=== TOST Sanity Checks ===")
    # Same rates → should be equivalent
    r = tost_proportion(30, 27, 30, 28)
    print(f"Same rates (0.9/0.93): TOST p={r['tost_p']:.3f}, is_equiv={r['is_equivalent']}")

    # Very different rates → should not be equivalent
    r = tost_proportion(30, 3, 30, 27)
    print(f"Different rates (0.1/0.9): TOST p={r['tost_p']:.3f}, is_equiv={r['is_equivalent']}")

    print("\n=== Bayes Factor Sanity Checks ===")
    # Same rates → high BF01 (evidence for plateau)
    r = bayes_factor_01(30, 27, 30, 28)
    print(f"Same rates: BF01={r['bf01']:.2f}, label={r['evidence_label']}")

    # Very different rates → low BF01 (evidence for dose-response)
    r = bayes_factor_01(30, 3, 30, 27)
    print(f"Different rates: BF01={r['bf01']:.4f}, label={r['evidence_label']}")
