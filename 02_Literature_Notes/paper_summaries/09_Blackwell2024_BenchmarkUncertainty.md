# Blackwell, Barry, Cohn (2024) — Quantifying Uncertainty in Benchmark Scores

**Full title:** *Towards Reproducible LLM Evaluation: Quantifying Uncertainty in LLM Benchmark Scores*
**arXiv:** 2410.03492
**URL:** https://arxiv.org/abs/2410.03492
**Role in our project:** Adjacent (non-competing) reference. Cited in literature review on benchmark reproducibility.

---

## Problem

LLMs are stochastic even with temperature=0 and fixed random seeds. Benchmark studies rarely quantify this non-determinism. Authors propose a "simple method for cost-effectively quantifying the uncertainty of a benchmark score."

## Methodology

- Experimental repeats on cardinal-direction reasoning benchmarks.
- Examine how repetition count affects mean score and prediction intervals.
- No Bradley-Terry model. No Arena data. No LLM-as-a-Judge analysis.

## Relevance to our project

- **Non-competing:** This paper's "uncertainty" is about *generation* stochasticity (output variability given fixed inputs). Ours is about *evaluation* stochasticity (judge-induced noise in preference data).
- **Cite as:** Related work on benchmark uncertainty quantification; explicitly distinguished ("Blackwell et al. address generation-side uncertainty from LLM stochasticity; our work addresses evaluation-side uncertainty from structured judge noise in pairwise comparison benchmarks").

## Why it's in our reading list

It's one of the two UQ-for-evaluation papers listed in the course brief. Reading it confirms that UQ for LLM evaluation is an active research area, even though this specific paper doesn't overlap with our contribution.
