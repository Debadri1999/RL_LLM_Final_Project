# Gu et al. (2024) — A Survey on LLM-as-a-Judge

**Full title:** *A Survey on LLM-as-a-Judge*
**Lead authors:** Jiawei Gu, Xuhui Jiang, Zhichao Shi, et al. (16 authors total)
**arXiv:** 2411.15594
**URL:** https://arxiv.org/abs/2411.15594
**Role in our project:** Background survey (required reading per course brief). Provides the taxonomic overview of LLM-as-a-Judge research we need for the literature review.

---

## Scope

Comprehensive survey of LLM-as-a-Judge methods, covering:
- Method taxonomy
- Bias mitigation strategies
- Reliability and consistency
- Application scenarios

## Key framings

- "Ensuring the reliability of LLM-as-a-Judge systems remains a significant challenge."
- Reliability strategies organized around: consistency improvement, bias mitigation, adaptation to assessment scenarios.

## Relevance to our project

1. **Framing reference** for the literature review section of our NeurIPS report.
2. Provides context that LLM-as-a-Judge systems feed into Arena-style evaluation infrastructure (e.g., automated judges are increasingly used alongside human votes).
3. Confirms that uncertainty quantification for LLM judges is an emerging open problem (reinforces the significance of our contribution).

## What it doesn't do

- Does not emphasize Bradley-Terry-Luce formal modeling.
- Does not address judge noise as a component of statistical uncertainty in rankings.
- Treats bias and uncertainty as separate (rather than noting that bias → a noise term in a formal model).

## How we cite it

As a framing citation for "LLM-as-a-Judge is a substantial research area with known reliability challenges" — not as a direct competitor.
