# Literature Review

**Project:** Pair-Heterogeneous Uncertainty in LLM Arena Leaderboards
**Purpose:** Comprehensive synthesis of relevant prior work, organized for direct use as Section 6 of the final report. Draft quality — will be trimmed, tightened, and reformatted into NeurIPS style in the next pass.

---

## 1. Overview and organization

The problem we study — uncertainty quantification for pairwise LLM leaderboards — sits at the intersection of four literatures:

1. **Arena-style evaluation and Bradley-Terry modeling** (Chiang et al., 2024; Frick et al., 2025).
2. **LLM-as-a-Judge and automated evaluation** (Zhu et al., 2023; Gu et al., 2024; Shi et al., 2024).
3. **Critiques and robustness analyses of leaderboard rankings** (Huang et al., 2025; Singh et al., 2024; Xu et al., 2026).
4. **Classical crowdsourcing and hierarchical annotator models** (Dawid & Skene, 1979; Raykar et al., 2010; Whitehill et al., 2009; Chen et al., 2013).

We cover each in turn, ending with an explicit gap statement positioning our contribution.

---

## 2. Arena-style evaluation and the Bradley-Terry foundation

Chiang et al. (2024) introduced Chatbot Arena, the open pairwise-comparison platform that has become the industry standard for LLM evaluation. Their methodology is deceptively simple: users submit a prompt, see responses from two anonymous models sampled at random, and vote for the preferred response (or declare a tie). Votes are aggregated across users and fit to a Bradley-Terry-Luce (BTL) model, which assigns each model a latent quality score. Confidence intervals are computed via bootstrap.

The BTL model (Bradley & Terry, 1952) assumes:

```
P(model i beats model j) = σ(s_i − s_j)
```

where `s_i` is the latent quality score for model `i`, `σ` is the logistic sigmoid, and crucially — **each observed preference is treated as an independent, unbiased sample** from this distribution. Under this assumption, the usual statistical machinery applies: MLE gives consistent point estimates, and bootstrap gives valid confidence intervals.

Frick et al. (2025) extend BTL to the prompt-conditional setting. Their Prompt-to-Leaderboard (P2L) model takes a prompt as input and produces a prompt-specific BTL score vector. This is a substantial generalization: it shows that the aggregate leaderboard is a lossy summary of a prompt-dependent preference landscape. A P2L-based router reached #1 on the Arena leaderboard in January 2025, empirically confirming that a single prompt-aware model can out-perform any fixed model averaged across all prompts.

However, neither Chiang et al. nor Frick et al. address the question of whether the judge process itself introduces structured noise that invalidates the IID assumption.

---

## 3. LLM-as-a-Judge: biases and automated evaluation

A parallel research thread studies automated LLM judges (Zhu et al., 2023; Gu et al., 2024). Zhu et al. (2023) introduced JudgeLM, a family of fine-tuned judge models (7B, 13B, 33B) that agree with GPT-4 ratings at >90% — surpassing human-to-human agreement. They identify three systematic bias categories:

1. **Position bias** — favoring the first or second response regardless of quality
2. **Knowledge bias** — over-weighting responses that match the judge's factual priors
3. **Format bias** — preferring specific formatting (length, markdown, structure)

Gu et al. (2024) surveyed the rapidly growing LLM-as-a-Judge literature and identified reliability as the central unsolved challenge. They catalog a broader range of biases and mitigation strategies but do not embed these biases in a formal statistical framework.

Shi et al. (2024) focused specifically on position bias with a large-scale empirical study (15 judges × 22 tasks × ~40 candidate models × 150K+ evaluations). They make two empirical findings that are directly relevant to our work:

1. **Position bias is non-random** — it is statistically structured and varies substantially across judges and tasks.
2. **Quality-gap sensitivity** — position bias is *strongest when the two candidates are close in quality*. Close battles are noisier.

This second finding is, to our knowledge, the first published evidence that judge noise depends on what is being judged — specifically on the model-pair distance. It is an empirical antecedent for our pair-heterogeneous noise hypothesis. However, Shi et al. do not embed this finding in a BTL-based leaderboard framework; their analysis is at the individual-judgment level, not the rank level.

Collectively, the LLM-as-a-Judge literature has documented substantial, structured judge bias but has not been integrated into the BTL/leaderboard framework of Chiang et al.

---

## 4. Critiques and robustness of leaderboards

Three recent papers have shown that Arena-style rankings are less reliable than their reported confidence intervals suggest.

**Huang, Shen, Wei & Broderick (2025)** demonstrated that **dropping just 0.003% of human preferences — roughly 4 out of 135K — can flip the top-ranked model** on Chatbot Arena. Using influence-function-based worst-case analysis, they identify the specific preferences responsible. MT-Bench is notably more robust, suggesting that expert annotation reduces fragility. Their paper is diagnostic: it demonstrates the problem exists but does not propose a principled statistical correction.

**Singh et al. (2024)**, "The Leaderboard Illusion," identifies structural distortions beyond preference-level fragility. Providers engage in undisclosed variant testing (Meta tested 27 private Llama-4 variants before release); sampling is asymmetric (Google and OpenAI receive 19–20% of Arena data vs 83 open models sharing 30%); retention of closed models is higher than open. Privileged access to Arena data yields up to 112% relative performance gains. This paper's critique is structural rather than statistical, but it reinforces the broader claim that Arena CIs underestimate true uncertainty.

**Xu, Tan, Wu & Zhou (2026)** — our primary reference — propose the most direct statistical remedy: extend BTL with judge-specific reliability parameters. Their model jointly estimates latent model quality and a per-judge discrimination coefficient `β_j` from pairwise data without reference labels. This produces better-calibrated confidence intervals.

Xu et al.'s framework is a significant advance but has two limitations relevant to our project. First, it models judge noise as a per-judge scalar, which presumes judges are repeat annotators. In Chatbot Arena, the public dataset (arena-140k) does not expose judge identities, and in practice most voters contribute only a handful of votes — `β_j` is not identifiable at the level the model requires. Second, the paper focuses on corrected point estimates and does not decompose *where* total rank uncertainty comes from, which limits its diagnostic utility for practitioners.

---

## 5. Classical crowdsourcing foundations

The idea of modeling annotator noise explicitly in aggregation is not new. **Dawid & Skene (1979)** introduced the first latent-class model for annotator reliability, using EM to jointly estimate true labels and per-annotator error matrices. **Whitehill et al. (2009)** generalized this to GLAD, which jointly models item difficulty and annotator expertise. **Raykar et al. (2010)** extended the framework to supervised learning from multiple noisy annotators. **Chen et al. (2013)** specifically addressed pairwise ranking aggregation in a crowdsourced setting, embedding annotator reliability directly in a BTL-style model.

This is important context: hierarchical BTL with annotator-noise terms is a well-established statistical framework. **Our contribution is not this framework itself.** It is the specific pair-heterogeneous noise structure required when judge identities are unobserved (as in arena-140k), the analytical variance decomposition framed as a practitioner diagnostic, and the first empirical audit of how this correction affects published Arena rank gaps.

---

## 6. Explicit gap statement

Combining these literatures surfaces a specific, unaddressed gap:

> Arena-style leaderboards report BTL confidence intervals under an IID-noiseless-judgment assumption that is empirically known to be false (Shi et al., 2024; Huang et al., 2025). The closest principled correction (Xu et al., 2026) models judge noise as a per-judge scalar, which is not identifiable in the standard public Arena release where judge identities are withheld. Meanwhile, empirical evidence (Shi et al., 2024) indicates that judge noise in pairwise LLM evaluation is structurally dependent on *what is being judged* — specifically on model-pair quality distance — rather than being a property of individual judges. No prior work has (a) formalized this pair-heterogeneous noise structure in a BTL-compatible framework, (b) derived a variance decomposition making the total rank uncertainty diagnostic, or (c) quantified how many of the currently "significant" rank gaps on the public Arena leaderboard survive such a correction.

These three contributions define our project.

---

## 7. Relationship to prior work — a compact table

| Paper | Addresses judge noise? | Pair-heterogeneous? | Variance decomp? | Arena-140k analysis? |
|---|---|---|---|---|
| Chiang et al. 2024 (Arena) | No — IID assumption | No | No | Base data source |
| Zhu et al. 2023 (JudgeLM) | Identifies bias types | No | No | No |
| Gu et al. 2024 (survey) | Discusses reliability | No | No | No |
| Shi et al. 2024 (Position Bias) | Yes — position-level | Empirically yes (by pair) | No | No |
| Frick et al. 2025 (P2L) | No | Point estimates only | No | Yes, but for point est |
| Huang et al. 2025 (Dropping) | Implicitly — robustness | No | No | Yes |
| Singh et al. 2024 (Illusion) | Structural, not statistical | No | No | Meta-analysis |
| Xu et al. 2026 (Judge-Aware) | Yes — per judge | No | No | Unclear / not emphasized |
| **Our project** | **Yes — structured** | **Yes — by pair + prompt** | **Yes — 4-component** | **Yes — rank-gap survival** |

---

## 8. References (APA-style for internal use; convert to NeurIPS format for submission)

Blackwell, R. E., Barry, J., & Cohn, A. G. (2024). Towards reproducible LLM evaluation: Quantifying uncertainty in LLM benchmark scores. *arXiv:2410.03492*.

Bradley, R. A., & Terry, M. E. (1952). Rank analysis of incomplete block designs: I. The method of paired comparisons. *Biometrika*, 39(3/4), 324–345.

Chen, X., Bennett, P. N., Collins-Thompson, K., & Horvitz, E. (2013). Pairwise ranking aggregation in a crowdsourced setting. *WSDM*.

Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhang, H., Zhu, B., Jordan, M., Gonzalez, J. E., & Stoica, I. (2024). Chatbot Arena: An open platform for evaluating LLMs by human preference. *arXiv:2403.04132*.

Dawid, A. P., & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates using the EM algorithm. *Journal of the Royal Statistical Society, Series C*, 28(1), 20–28.

Frick, E., Chen, C., Tennyson, J., Li, T., Chiang, W.-L., Angelopoulos, A. N., & Stoica, I. (2025). Prompt-to-Leaderboard. *arXiv:2502.14855*.

Gu, J., Jiang, X., Shi, Z., et al. (2024). A survey on LLM-as-a-Judge. *arXiv:2411.15594*.

Huang, J. Y., Shen, Y., Wei, D., & Broderick, T. (2025). Dropping just a handful of preferences can change top large language model rankings. *arXiv:2508.11847*.

Raykar, V. C., Yu, S., Zhao, L. H., Valadez, G. H., Florin, C., Bogoni, L., & Moy, L. (2010). Learning from crowds. *Journal of Machine Learning Research*, 11, 1297–1322.

Shi, L., Ma, C., Liang, W., Diao, X., Ma, W., & Vosoughi, S. (2024). Judging the judges: A systematic study of position bias in LLM-as-a-Judge. *arXiv:2406.07791*.

Singh, S., Nan, Y., Wang, A., et al. (2024). The leaderboard illusion. *arXiv:2504.20879*.

Whitehill, J., Wu, T.-f., Bergsma, J., Movellan, J., & Ruvolo, P. (2009). Whose vote should count more: Optimal integration of labels from labelers of unknown expertise. *NeurIPS*.

Xu, M., Tan, X., Wu, J., & Zhou, D. (2026). A judge-aware ranking framework for evaluating large language models without ground truth. *arXiv:2601.21817*.

Zhu, L., Wang, X., & Wang, X. (2023). JudgeLM: Fine-tuned large language models are scalable judges. *arXiv:2310.17631*.
