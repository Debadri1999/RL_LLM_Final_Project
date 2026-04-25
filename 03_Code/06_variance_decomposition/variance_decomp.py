"""
variance_decomp.py
------------------
Four-component variance decomposition:

    Var(s_hat_i) = V_sampling + V_judge_identity + V_prompt_category + V_pair_distance

Approach: numerical decomposition via ablated refits.

    1. Fit full HierarchicalBTL on the data; get baseline Var(s_hat).
    2. Fit restricted models that zero out each noise component in turn:
         - zero out category effect: alpha_c = 0
         - zero out pair-distance effect: alpha_d = 0
         - zero out all structured noise (reduces to StandardBTL with judge scalar): alpha_0 + alpha_c + alpha_d = 0
    3. The contribution of each component is Var_full - Var_restricted (approximately).

Alternatively, if the closed-form math in the report is clean, substitute that
here. For Phase 2, we prioritize the numerical version because it's robust to
any parameterization choice.

Output
------
- 07_Data/results/variance_decomposition.parquet  — one row per model, columns:
    V_sampling, V_judge_identity, V_prompt_category, V_pair_distance, V_total

TODO:
- Implement once HierarchicalBTL is working.
- Sanity-check that components are non-negative (they should be, under correct specification).
- Cross-check against closed-form delta-method formula (Appendix A of report).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arena_clean", type=Path,
                    default=Path("../../07_Data/arena_clean.parquet"))
    ap.add_argument("--output", type=Path,
                    default=Path("../../07_Data/results/variance_decomposition.parquet"))
    ap.add_argument("--n_boot", type=int, default=500)
    args = ap.parse_args()

    # TODO: load battles, fit full HierarchicalBTL, fit restricted variants,
    # compute per-model variance components.
    print("(stub — implement in Phase 2 of the plan)")


if __name__ == "__main__":
    main()
