"""
arena_survival_analysis.py
--------------------------
HEADLINE EXPERIMENT: compute the fraction of currently-"significant" pairwise
rank gaps on Chatbot Arena (arena-140k) that survive after applying our
pair-heterogeneous hierarchical BTL correction.

Pipeline
--------
1. Load cleaned arena-140k (top-20 models, English-only, non-tie).
2. Fit StandardBTL on the full subset; bootstrap CIs. Record "significant pairs":
   pairs (i,j) where ci_lower_i > ci_upper_j (i ranks above j with 95% confidence).
3. Fit HierarchicalBTL on the same subset; bootstrap CIs. Recompute significant pairs.
4. Compute: survival_rate = |sig_hier| / |sig_standard|.
5. Report the specific pairs that flipped (standard-significant → hierarchical-not-significant).
6. Repeat per prompt category to produce a category-level breakdown.

Outputs
-------
- 07_Data/results/survival_summary.parquet  — one row per category (plus 'all')
- 07_Data/results/flipped_pairs.parquet     — the pairs that became non-significant
- 07_Data/figures/survival_by_category.png  — headline figure

TODO:
- Wire this up once btl_standard and btl_hierarchical are implemented and validated.
- Decide: use bootstrap CIs end-to-end, or switch to Fisher-info for speed on full arena.
- Write a notebook version for interactive debugging (07_results/arena_analysis.ipynb).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))   # project code root
# from btl_standard import StandardBTL
# from btl_hierarchical import HierarchicalBTL


def significant_pairs(ci_df: pd.DataFrame) -> set[tuple[str, str]]:
    """Return set of (i, j) pairs where i is significantly above j."""
    pairs = set()
    models = ci_df["model"].tolist()
    for a in range(len(models)):
        for b in range(len(models)):
            if a == b:
                continue
            if ci_df.iloc[a]["ci_lower"] > ci_df.iloc[b]["ci_upper"]:
                pairs.add((models[a], models[b]))
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arena_clean", type=Path,
                    default=Path("../../07_Data/arena_clean.parquet"))
    ap.add_argument("--results_dir", type=Path,
                    default=Path("../../07_Data/results"))
    ap.add_argument("--n_boot", type=int, default=500)
    args = ap.parse_args()

    args.results_dir.mkdir(parents=True, exist_ok=True)

    battles = pd.read_parquet(args.arena_clean)
    print(f"Loaded {len(battles):,} battles across {battles['category'].nunique()} categories")

    # ------------------------------------------------------------- #
    # 1. Overall survival
    # ------------------------------------------------------------- #
    # TODO: uncomment once btl_standard and btl_hierarchical ready
    # models = sorted(set(battles["model_a"]) | set(battles["model_b"]))
    # categories = sorted(battles["category"].unique())
    #
    # std_model = StandardBTL(models).fit(battles)
    # std_cis   = std_model.bootstrap_ci(battles, n_boot=args.n_boot)
    # sig_std   = significant_pairs(std_cis)
    #
    # hier_model = HierarchicalBTL(models, categories).fit(battles)
    # hier_cis   = hier_model.bootstrap_ci(battles, n_boot=args.n_boot)
    # sig_hier   = significant_pairs(hier_cis)
    #
    # flipped   = sig_std - sig_hier
    # survival  = len(sig_hier) / max(1, len(sig_std))
    # print(f"Survival rate overall: {survival*100:.1f}%")
    # print(f"Flipped pairs: {len(flipped)}")

    # ------------------------------------------------------------- #
    # 2. Per-category breakdown
    # ------------------------------------------------------------- #
    # TODO: per-category loop

    print("(stub — wire up models in Phase 4 of the plan)")


if __name__ == "__main__":
    main()
