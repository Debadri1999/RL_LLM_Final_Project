# Huang, Shen, Wei, Broderick (2025) — Dropping Just a Handful of Preferences

**Full title:** *Dropping Just a Handful of Preferences Can Change Top Large Language Model Rankings*
**arXiv:** 2508.11847
**URL:** https://arxiv.org/abs/2508.11847
**Role in our project:** Direct antecedent. Motivates our project's framing: if dropping 0.003% of preferences flips the top rank, standard BTL CIs are deeply overconfident.

---

## Core claim

"Dropping just 0.003% of human preferences can change the top-ranked model on Chatbot Arena." That is **~4 preferences out of ~135K**. Rank fragility is empirical, dramatic, and concentrated.

## Methodology

- Robustness evaluation on Bradley-Terry model variants.
- Worst-case subset removal: identify minimum-size preference subset whose removal flips the top-k ranking.
- Efficient computation using influence functions / approximate leave-k-out analysis.

## Datasets analyzed

- Chatbot Arena
- MT-Bench
- Derivatives using both crowdsourced human and LLM-as-a-judge preferences

## Findings

- Arena is highly fragile (0.003%).
- MT-Bench is notably more robust — expert annotation improves stability.
- Fragility concentrated in "close" model-pair comparisons.

## Proposed remedies

Not explicit — paper is primarily diagnostic. Suggests expert annotation and careful prompt construction as directional improvements.

## Relevance to our project

1. **Core motivation:** The fact that rank gaps are fragile to preference perturbations is prima facie evidence that CIs are underestimating true uncertainty. Our project identifies *why* — misspecified judge-noise model — and provides a principled correction rather than an adversarial sensitivity analysis.
2. **Methodological complementarity:** Their influence-function machinery can be repurposed in our variance decomposition (which preferences contribute most to `V_judge` vs `V_sampling`).
3. **Close battles are more fragile** — exactly our pair-distance-dependent noise claim.

## Explicit distinction from our work

- Huang et al. ask: "How many preferences must be dropped to flip rankings?"
- We ask: "How much of the apparent rank certainty disappears when we correctly model the noise in the first place?"
- These are two sides of the same coin but have different statistical framings (adversarial robustness vs model-based uncertainty correction).
