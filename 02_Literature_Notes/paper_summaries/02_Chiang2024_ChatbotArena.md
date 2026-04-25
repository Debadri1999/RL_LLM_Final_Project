# Chiang et al. (2024) — Chatbot Arena

**Full title:** *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*
**Authors:** Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle Li, Dacheng Li, Hao Zhang, Banghua Zhu, Michael Jordan, Joseph E. Gonzalez, Ion Stoica
**arXiv:** 2403.04132
**URL:** https://arxiv.org/abs/2403.04132
**Role in our project:** Background foundational paper (required reading per course brief). Defines the evaluation system our project audits.

---

## Problem

Evaluating LLM alignment with human preferences is hard: traditional benchmarks (MMLU, HELM, etc.) score narrow capabilities, not holistic open-ended quality. The paper introduces an open platform for crowdsourced pairwise human evaluation.

## Methodology

- Anonymous pairwise comparison: user submits a prompt, sees responses from two randomly-sampled models, votes for preferred (or tie / both bad).
- Battles aggregated across users to fit a Bradley-Terry-Luce (BTL) model producing latent quality scores `s_i`.
- Confidence intervals via standard BTL machinery (bootstrap / CLT).
- Scale at submission: 240K+ votes.

## Key contributions

1. Open-platform infrastructure for continuous LLM evaluation
2. Demonstration that crowdsourced votes agree with expert raters
3. Public leaderboard adopted industry-wide

## Statistical assumptions (that our project challenges)

- **IID preferences:** Each vote is an independent draw from the true preference distribution.
- **Noiseless judgment:** `P(i beats j) = σ(s_i − s_j)` — no judge noise term.
- **Interchangeable judges:** All voters weighted equally.

## Limitations acknowledged / later critiqued

The original paper notes some limitations but subsequent work (Leaderboard Illusion, Dropping Handful, Prompt-to-Leaderboard) has surfaced:
- Sampling bias across models
- Rank fragility to preference perturbations
- Prompt-category heterogeneity masked by aggregate ranking
- Private variant testing by providers

## Relevance to our project

Chatbot Arena is the system we are auditing. Our proposal corrects the "noiseless judgment" assumption by adding a structured judge-noise term. Our real-data analysis uses arena-140k, a 135,634-vote public release.
