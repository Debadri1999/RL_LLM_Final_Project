# Frick et al. (2025) — Prompt-to-Leaderboard (P2L)

**Full title:** *Prompt-to-Leaderboard*
**Authors:** Evan Frick, Connor Chen, Joseph Tennyson, Tianle Li, Wei-Lin Chiang, Anastasios N. Angelopoulos, Ion Stoica
**arXiv:** 2502.14855
**URL:** https://arxiv.org/abs/2502.14855
**Role in our project:** Methodological sibling — a prompt-conditional BTL model. We differ on motivation (they do prompt-conditional *point estimates*; we do prompt-conditional *uncertainty decomposition*).

---

## Problem

Aggregate Arena rankings mask that model performance varies by prompt type. Single global ranking is a lossy summary of a prompt-dependent preference landscape.

## Methodology

- Train an LLM that takes a natural-language prompt as input and outputs a vector of prompt-conditional **Bradley-Terry coefficients** for all models.
- These coefficients produce a per-prompt leaderboard rather than an aggregate one.
- Enables: prompt-specific evaluation, query routing to best model, personalization, strength/weakness detection.

## Key findings

- Per-prompt rankings differ meaningfully from aggregate rankings.
- P2L-trained routers can outperform any single model on the aggregate leaderboard (a P2L router hit #1 on Arena, Jan 2025).
- Power-law scaling in prompt-conditional evaluation quality with data.

## Relevance to our project

- **Delta 1 (pair-heterogeneous noise) connection:** P2L shows that *point estimates* are prompt-dependent. We extend this: if scores are prompt-dependent, then so is their uncertainty — not just the score, but the noise in how judges evaluate that score.
- **Methodological complementarity:** P2L's prompt embedding could be used as a feature in our structured noise model: `σ²_judge(prompt, model_pair) = g(f_prompt(prompt), d(model_pair))`.
- **Different question:** P2L asks "what is the best model *for this prompt*?" We ask "how confident is Arena's aggregate ranking, once we account for the fact that noise varies by prompt type?"

## Literature-review role

Key reference demonstrating that prompt heterogeneity matters for Arena-style evaluation. We position our project as the uncertainty-quantification analog of P2L's point-estimate framework.
