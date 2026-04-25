"""
simulation.py
-------------
Controlled simulation with known ground-truth model scores.

Objective (Phase 3 of the plan)
-------------------------------
Demonstrate that **standard BTL confidence intervals undercover at ~95%
nominal level** when the true data-generating process has pair-heterogeneous
judge noise, while our hierarchical BTL maintains nominal coverage.

This REPLACES the original teammate outline's simulation, whose results
showed standard BTL exactly at 95% coverage (which is not a failure — it's
the target). The fix here: push noise higher, include pair-distance noise,
and use enough battles that standard BTL becomes overconfident.

Protocol
--------
For each noise scenario:
    1. Draw true scores s_i ~ Uniform(0, 3), n_models = 10.
    2. Assign each of n_battles to a random (i, j) pair and a random prompt category.
    3. Generate the win indicator under the true pair-heterogeneous noise model.
    4. Fit standard BTL, compute bootstrap 95% CIs.
    5. Fit hierarchical BTL, compute bootstrap 95% CIs.
    6. Record: coverage_std = fraction of true s_i in [ci_lower_std, ci_upper_std];
               coverage_hier analogously.
Repeat n_trials times per scenario; average.

Scenarios (varying category noise level):
    sigma2_c in {0.05, 0.25, 0.50, 1.00}
    n_battles = 5000 (large enough for standard BTL to "look confident")
    n_trials = 500

TODO:
- Implement the actual simulation once btl_standard and btl_hierarchical are working end-to-end.
- Decide whether bootstrap or asymptotic-Fisher CIs for the hierarchical model (bootstrap is slower but safer).
- Target outcome: standard BTL coverage drops to 70-85% in high-noise scenarios;
  hierarchical coverage stays near 95%.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm


# --------------------------------------------------------------------------- #
# Data-generating process                                                     #
# --------------------------------------------------------------------------- #

def simulate_battles(
    true_scores: np.ndarray,
    n_battles: int,
    n_categories: int,
    sigma2_0: float,
    sigma2_c: np.ndarray,    # length n_categories
    alpha_d: float,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate battles under the pair-heterogeneous noise model."""
    n_models = len(true_scores)
    i_idx = rng.integers(0, n_models, n_battles)
    j_idx = rng.integers(0, n_models, n_battles)
    # re-draw any (i==j)
    mask = i_idx == j_idx
    while mask.any():
        j_idx[mask] = rng.integers(0, n_models, mask.sum())
        mask = i_idx == j_idx
    c_idx = rng.integers(0, n_categories, n_battles)

    diff = true_scores[i_idx] - true_scores[j_idx]
    d = np.abs(diff)
    sigma2 = np.exp(np.log(sigma2_0) + np.log(sigma2_c[c_idx]) + alpha_d * d)
    # Thurstone / probit-style: observe win(i) = 1 if diff + epsilon > 0,
    # epsilon ~ N(0, sigma2). Logistic would also work; probit is cleaner algebraically.
    eps = rng.normal(0.0, np.sqrt(sigma2))
    y = (diff + eps > 0).astype(int)

    return pd.DataFrame({
        "i": i_idx,
        "j": j_idx,
        "category": c_idx,
        "winner_i": y,
    })


# --------------------------------------------------------------------------- #
# Coverage calculation                                                        #
# --------------------------------------------------------------------------- #

def coverage_probability(true_scores, ci_lower, ci_upper) -> float:
    """Fraction of true scores within their CIs."""
    return float(np.mean((ci_lower <= true_scores) & (true_scores <= ci_upper)))


# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_models", type=int, default=10)
    ap.add_argument("--n_battles", type=int, default=5000)
    ap.add_argument("--n_categories", type=int, default=4)
    ap.add_argument("--n_trials", type=int, default=500)
    ap.add_argument("--n_boot", type=int, default=200,
                    help="Bootstrap resamples per fit; use 200 for runtime, 500+ for final.")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    scenarios = [
        {"name": "low_noise",     "sigma2_c_scale": 0.05, "alpha_d": 0.1},
        {"name": "moderate",      "sigma2_c_scale": 0.25, "alpha_d": 0.2},
        {"name": "high_noise",    "sigma2_c_scale": 0.50, "alpha_d": 0.4},
        {"name": "very_high",     "sigma2_c_scale": 1.00, "alpha_d": 0.6},
    ]

    results = []
    for sc in scenarios:
        for trial in tqdm(range(args.n_trials), desc=sc["name"]):
            true_scores = rng.uniform(0, 3, args.n_models)
            sigma2_c = rng.uniform(0.5, 2.0, args.n_categories) * sc["sigma2_c_scale"]
            battles = simulate_battles(
                true_scores, args.n_battles, args.n_categories,
                sigma2_0=1.0, sigma2_c=sigma2_c, alpha_d=sc["alpha_d"], rng=rng,
            )

            # TODO: fit StandardBTL, get bootstrap CIs, measure coverage
            # TODO: fit HierarchicalBTL, get bootstrap CIs, measure coverage
            # results.append({
            #     "scenario": sc["name"],
            #     "trial": trial,
            #     "coverage_standard": coverage_standard,
            #     "coverage_hierarchical": coverage_hierarchical,
            #     "mean_ci_width_standard": ...,
            #     "mean_ci_width_hierarchical": ...,
            # })
            pass

    print("\n(simulation stub — fill in fit calls in Phase 3 of the plan)")
    df = pd.DataFrame(results)
    df.to_parquet(args.output)
    print(f"Saved → {args.output}")


if __name__ == "__main__":
    main()
