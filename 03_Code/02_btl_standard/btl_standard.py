"""
btl_standard.py
---------------
Standard Bradley-Terry-Luce (BTL) fit for arena-style pairwise preference data.
This is the BASELINE our hierarchical model will be compared against.

Model
-----
For a battle between model i and model j with winner y (y=1 if i wins, 0 otherwise):

    P(i beats j) = sigmoid(s_i - s_j)

Assumes IID noiseless judgments (the assumption our project critiques).

Identifiability: s_0 = 0 (first model's score pinned).

Usage
-----
    python btl_standard.py --input ../07_Data/arena_clean.parquet \\
                           --output ../07_Data/standard_btl_scores.parquet \\
                           --n_boot 1000
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit as sigmoid
from tqdm import tqdm


# --------------------------------------------------------------------------- #
# Model                                                                       #
# --------------------------------------------------------------------------- #

class StandardBTL:
    """Plain Bradley-Terry-Luce model with MLE estimation."""

    def __init__(self, models: list[str]):
        self.models = list(models)
        self.model_to_idx = {m: i for i, m in enumerate(self.models)}
        self.n_models = len(self.models)
        self.scores_: np.ndarray | None = None

    def _neg_log_lik(self, s_free: np.ndarray, i_idx: np.ndarray,
                    j_idx: np.ndarray, y: np.ndarray) -> float:
        # Insert s_0 = 0 for identifiability.
        s = np.concatenate(([0.0], s_free))
        logits = s[i_idx] - s[j_idx]
        # log P(y | logits) = y*log(sigm) + (1-y)*log(1-sigm)
        # numerically stable form
        ll = -np.logaddexp(0.0, -logits) * y + (-np.logaddexp(0.0, logits)) * (1 - y)
        return -ll.sum()

    def _grad_neg_log_lik(self, s_free, i_idx, j_idx, y):
        s = np.concatenate(([0.0], s_free))
        p = sigmoid(s[i_idx] - s[j_idx])
        resid = (y - p)                               # shape (n_battles,)
        grad = np.zeros(self.n_models)
        np.add.at(grad, i_idx, -resid)
        np.add.at(grad, j_idx,  resid)
        return grad[1:]                               # drop s_0

    def fit(self, battles: pd.DataFrame) -> "StandardBTL":
        """
        battles: DataFrame with columns ['model_a', 'model_b', 'winner']
        where winner in {'model_a', 'model_b'} (we drop ties upstream).
        """
        i_idx = battles["model_a"].map(self.model_to_idx).to_numpy()
        j_idx = battles["model_b"].map(self.model_to_idx).to_numpy()
        y = (battles["winner"] == "model_a").astype(int).to_numpy()

        s0 = np.zeros(self.n_models - 1)
        res = minimize(
            self._neg_log_lik, s0, args=(i_idx, j_idx, y),
            jac=self._grad_neg_log_lik,
            method="L-BFGS-B",
        )
        self.scores_ = np.concatenate(([0.0], res.x))
        return self

    def scores_df(self) -> pd.DataFrame:
        return pd.DataFrame({"model": self.models, "score": self.scores_})

    def bootstrap_ci(self, battles: pd.DataFrame, n_boot: int = 1000,
                     alpha: float = 0.05, seed: int = 0) -> pd.DataFrame:
        """Nonparametric bootstrap confidence intervals."""
        rng = np.random.default_rng(seed)
        n = len(battles)
        all_scores = np.zeros((n_boot, self.n_models))
        for b in tqdm(range(n_boot), desc="bootstrap"):
            idx = rng.integers(0, n, n)
            sub = battles.iloc[idx]
            m = StandardBTL(self.models).fit(sub)
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
    ap.add_argument("--input", required=True, type=Path,
                    help="parquet of cleaned arena battles")
    ap.add_argument("--output", required=True, type=Path,
                    help="parquet for scores with bootstrap CIs")
    ap.add_argument("--n_boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    battles = pd.read_parquet(args.input)
    # Expect columns at minimum: model_a, model_b, winner
    battles = battles[battles["winner"].isin(["model_a", "model_b"])]  # drop ties
    models = sorted(set(battles["model_a"]) | set(battles["model_b"]))
    print(f"Models: {len(models)}   Battles: {len(battles):,}")

    m = StandardBTL(models).fit(battles)
    out = m.bootstrap_ci(battles, n_boot=args.n_boot, seed=args.seed)
    out = out.sort_values("score", ascending=False).reset_index(drop=True)
    out.to_parquet(args.output)

    print("\nTop-10 models:")
    print(out.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
