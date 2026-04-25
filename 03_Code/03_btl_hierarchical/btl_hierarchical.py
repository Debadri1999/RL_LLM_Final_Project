"""
btl_hierarchical.py
-------------------
Our proposed Pair-Heterogeneous Hierarchical Bradley-Terry-Luce model.

Generative model
----------------
For a battle with models (i, j), prompt category c, and pair distance d = |s_i - s_j|:

    sigma^2_judge(c, d) = exp(alpha_0 + alpha_c + alpha_d * d)
    P(i beats j | battle) = sigmoid((s_i - s_j) / sqrt(1 + sigma^2_judge))

Identifiability pins:
    s_0 = 0           (first model's score)
    alpha_ref = 0     (one reference category coefficient pinned)

Parameters estimated:
    s         length (n_models - 1)
    alpha_0   scalar
    alpha_c   length (n_categories - 1)
    alpha_d   scalar

TODO (Phase 2):
- Replace the placeholder sigma^2 parameterization with the final version after
  cross-checking the variance decomposition math.
- Consider EM as a backup if joint L-BFGS-B fails to converge cleanly.
- Add Fisher-information-based CI as an alternative to bootstrap for faster iteration.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit as sigmoid
from tqdm import tqdm


class HierarchicalBTL:
    """Pair-heterogeneous hierarchical BTL."""

    def __init__(self, models: list[str], categories: list[str]):
        self.models = list(models)
        self.categories = list(categories)
        self.model_to_idx = {m: i for i, m in enumerate(self.models)}
        self.cat_to_idx = {c: i for i, c in enumerate(self.categories)}
        self.n_models = len(self.models)
        self.n_categories = len(self.categories)

        # Parameter vector layout:
        #   s_free         length (n_models - 1)
        #   alpha_0        scalar
        #   alpha_c_free   length (n_categories - 1)
        #   alpha_d        scalar
        self.n_params = (self.n_models - 1) + 1 + (self.n_categories - 1) + 1

        self.scores_: np.ndarray | None = None
        self.alpha_0_: float | None = None
        self.alpha_c_: np.ndarray | None = None
        self.alpha_d_: float | None = None

    def _unpack(self, theta: np.ndarray):
        pos = 0
        s_free = theta[pos:pos + self.n_models - 1]; pos += self.n_models - 1
        alpha_0 = theta[pos]; pos += 1
        alpha_c_free = theta[pos:pos + self.n_categories - 1]; pos += self.n_categories - 1
        alpha_d = theta[pos]
        s = np.concatenate(([0.0], s_free))
        alpha_c = np.concatenate(([0.0], alpha_c_free))
        return s, alpha_0, alpha_c, alpha_d

    def _neg_log_lik(self, theta, i_idx, j_idx, c_idx, y):
        s, alpha_0, alpha_c, alpha_d = self._unpack(theta)
        diff = s[i_idx] - s[j_idx]
        d = np.abs(diff)
        sigma2 = np.exp(alpha_0 + alpha_c[c_idx] + alpha_d * d)
        scale = np.sqrt(1.0 + sigma2)
        logits = diff / scale
        ll = -np.logaddexp(0.0, -logits) * y + (-np.logaddexp(0.0, logits)) * (1 - y)
        return -ll.sum()

    def fit(self, battles: pd.DataFrame) -> "HierarchicalBTL":
        """
        battles: DataFrame with columns ['model_a', 'model_b', 'winner', 'category']
        winner in {'model_a', 'model_b'}
        """
        i_idx = battles["model_a"].map(self.model_to_idx).to_numpy()
        j_idx = battles["model_b"].map(self.model_to_idx).to_numpy()
        c_idx = battles["category"].map(self.cat_to_idx).to_numpy()
        y = (battles["winner"] == "model_a").astype(int).to_numpy()

        theta0 = np.zeros(self.n_params)
        res = minimize(
            self._neg_log_lik, theta0, args=(i_idx, j_idx, c_idx, y),
            method="L-BFGS-B",
            options={"maxiter": 500},
        )
        if not res.success:
            print(f"WARNING: optimizer did not converge cleanly — {res.message}")
        s, alpha_0, alpha_c, alpha_d = self._unpack(res.x)
        self.scores_ = s
        self.alpha_0_ = alpha_0
        self.alpha_c_ = alpha_c
        self.alpha_d_ = alpha_d
        self._theta_ = res.x
        return self

    def sigma2(self, category: str, pair_distance: float) -> float:
        c_idx = self.cat_to_idx[category]
        return float(np.exp(self.alpha_0_ + self.alpha_c_[c_idx] + self.alpha_d_ * pair_distance))

    def scores_df(self) -> pd.DataFrame:
        return pd.DataFrame({"model": self.models, "score": self.scores_})

    def bootstrap_ci(self, battles: pd.DataFrame, n_boot: int = 1000,
                     alpha: float = 0.05, seed: int = 0) -> pd.DataFrame:
        rng = np.random.default_rng(seed)
        n = len(battles)
        all_scores = np.zeros((n_boot, self.n_models))
        for b in tqdm(range(n_boot), desc="bootstrap (hierarchical)"):
            idx = rng.integers(0, n, n)
            sub = battles.iloc[idx]
            m = HierarchicalBTL(self.models, self.categories).fit(sub)
            all_scores[b] = m.scores_
        lo = np.quantile(all_scores, alpha / 2, axis=0)
        hi = np.quantile(all_scores, 1 - alpha / 2, axis=0)
        return pd.DataFrame({
            "model": self.models,
            "score": self.scores_,
            "ci_lower": lo,
            "ci_upper": hi,
            "ci_width": hi - lo,
        })


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--n_boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    battles = pd.read_parquet(args.input)
    battles = battles[battles["winner"].isin(["model_a", "model_b"])]
    # Expect preprocessed 'category' column — if not present, fill with 'general'
    if "category" not in battles.columns:
        battles = battles.assign(category="general")

    models = sorted(set(battles["model_a"]) | set(battles["model_b"]))
    categories = sorted(battles["category"].unique())
    print(f"Models: {len(models)}   Categories: {len(categories)}   Battles: {len(battles):,}")

    m = HierarchicalBTL(models, categories).fit(battles)
    print(f"alpha_0 = {m.alpha_0_:.3f}   alpha_d = {m.alpha_d_:.3f}")
    print("alpha_c:", dict(zip(m.categories, m.alpha_c_)))

    out = m.bootstrap_ci(battles, n_boot=args.n_boot, seed=args.seed)
    out = out.sort_values("score", ascending=False).reset_index(drop=True)
    out.to_parquet(args.output)

    print("\nTop-10 models:")
    print(out.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
