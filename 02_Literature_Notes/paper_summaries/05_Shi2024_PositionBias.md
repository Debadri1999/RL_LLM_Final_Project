# Shi et al. (2024) — Judging the Judges: Position Bias

**Full title:** *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*
**Authors:** Lin Shi, Chiyu Ma, Wenhua Liang, Xingjian Diao, Weicheng Ma, Soroush Vosoughi
**arXiv:** 2406.07791
**URL:** https://arxiv.org/abs/2406.07791
**Role in our project:** Related advanced paper (alternative topic in course brief). We cite it in our literature review as evidence that judge noise is real, structured, and varies by context.

---

## Problem

Position bias — the tendency of LLM judges to favor a solution based on its position in the prompt — systematically distorts pairwise evaluations. Prior studies characterize bias informally; this paper measures it rigorously.

## Methodology

Three bias metrics:
1. **Repetition stability** — consistency across repeated evaluations of same pair
2. **Position consistency** — fairness across different orderings
3. **Preference fairness** — balanced treatment of candidates

Experimental scale: 15 LLM judges × 22 tasks (MTBench + DevBench) × ~40 solution-generating models = 150K+ evaluation instances.

## Key empirical findings

- **Position bias is non-random** and varies substantially across judges and tasks.
- **Quality gap matters:** bias is stronger when the two candidates are closer in quality (close battles = noisier judgments). **This is a direct empirical antecedent for our pair-distance-heterogeneous noise hypothesis.**
- **Prompt length has weak effects;** prompt content / task type has strong effects.
- Different judges exhibit position bias differently — bias is not a universal judge property.

## Proposed mitigations

Dataset modifications (e.g., randomized presentation order). Specific techniques not fully detailed in abstract.

## Relevance to our project

- **Empirical justification for Delta 1 (pair-heterogeneous noise):** Their finding that quality gap controls bias magnitude *is* our pair-distance-dependent noise hypothesis, observed in a different setting.
- **Evidence for prompt-category heterogeneity:** Bias varies across tasks (MTBench vs DevBench), suggesting σ²_judge varies with prompt type — another piece of our structured-noise argument.

## What they don't do

- Don't embed position bias as a noise term in a BTL model.
- Don't quantify how bias propagates to rank-level uncertainty.
- Don't address arena-scale evaluation.
