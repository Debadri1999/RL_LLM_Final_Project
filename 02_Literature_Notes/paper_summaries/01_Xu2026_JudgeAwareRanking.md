# Xu, Tan, Wu, Zhou (2026) — Judge-Aware Ranking Framework

**Full title:** *A Judge-Aware Ranking Framework for Evaluating Large Language Models without Ground Truth*
**arXiv:** 2601.21817
**URL:** https://arxiv.org/abs/2601.21817
**Role in our project:** Primary reference paper. Our proposal extends / diverges from this paper.

---

## Problem

Existing pairwise-comparison LLM leaderboards treat all judges (human annotators or LLM judges) as equally reliable. Xu et al. argue that "judge LLMs differ substantially in reliability; treating all judges equally can yield biased leaderboards and misleading uncertainty estimates."

## Methodology

Extends the standard Bradley-Terry-Luce (BTL) model by introducing **judge-specific discrimination parameters**. The model jointly estimates (a) latent model quality scores `s_i` and (b) judge reliability parameters `β_j` from pairwise comparisons, without requiring reference labels.

Effectively: `P(i beats j | judge k) = σ(β_k · (s_i − s_j))`, where `β_k` is the judge's discrimination / reliability coefficient.

## Key contributions

1. Joint estimation framework for model quality and judge reliability
2. Calibrated uncertainty quantification for LLM rankings
3. Empirical validation on "multiple public benchmarks and a newly collected dataset"

## Limitations / what they DON'T do

- **Pair-heterogeneous noise:** Noise is modeled as a per-judge scalar β_k; they do not model noise varying by prompt category or by model-pair distance.
- **Analytical variance decomposition:** Paper focuses on corrected point estimates rather than decomposing total rank uncertainty into interpretable components.
- **Chatbot Arena empirical analysis:** Abstract says "multiple public benchmarks and a newly collected dataset" — Arena is not emphasized. And even if it were, arena-140k does not provide judge IDs, so their per-judge β_k cannot be estimated on Arena at all.

## Relevance to our three deltas

- **Delta 1 (pair-heterogeneous noise):** Directly opened up by the fact that arena-140k lacks judge IDs → `β_k` is unidentifiable → we must model noise at a different granularity.
- **Delta 2 (variance decomposition):** Xu et al. compute corrected CIs; we decompose where the CI width comes from.
- **Delta 3 (arena audit):** Xu et al. don't publish an arena-specific rank-gap survival rate; we do.

## Open questions they leave

- How should judge-noise structure be modeled when judge identities are unobserved? (Directly motivates our Delta 1.)
- How does the correction behave on different benchmark data-generating processes?
