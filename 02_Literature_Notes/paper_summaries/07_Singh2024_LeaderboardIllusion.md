# Singh et al. (2024) — The Leaderboard Illusion

**Full title:** *The Leaderboard Illusion*
**Authors:** Shivalika Singh, Yiyang Nan, Alex Wang, Daniel D'Souza, Sayash Kapoor, Ahmet Üstün, Sanmi Koyejo, Yuntian Deng, Shayne Longpre, Noah A. Smith, Beyza Ermis, Marzieh Fadaee, Sara Hooker
**arXiv:** 2504.20879
**URL:** https://arxiv.org/abs/2504.20879
**Role in our project:** Structural critique — provides the meta-argument that arena leaderboards have systematic distortions beyond sampling noise.

---

## Core argument

Chatbot Arena has several structural distortions that bias the leaderboard beyond what sampling-noise-based CIs capture:

1. **Private variant testing:** Providers test many private model variants and disclose only the best (Meta tested 27 private Llama-4 variants).
2. **Sampling asymmetry:** Google and OpenAI received ~19-20% of total arena data; 83 open-weight models shared only ~30%.
3. **Retention asymmetry:** Fewer closed models are removed from the arena than open alternatives.
4. **Selection effects:** Providers can choose when to publicly submit a model.

## Key quantitative finding

Access to arena data yields up to **112% relative performance gains** on arena-distribution tasks with conservative estimates.

## Proposed remedies

Reform recommendations for arena evaluation methodology — though specific recommendations not detailed in the abstract.

## Relevance to our project

- **Structural context:** Our project addresses one specific kind of systematic bias (judge noise structure). The Leaderboard Illusion provides a broader context that Arena-style rankings have multiple systematic distortions.
- **Complementary framing:** We cite this paper as evidence that "the Arena leaderboard is less reliable than its reported CIs suggest," then narrow to our specific contribution (properly modeling judge noise).
- **Not a direct competitor:** Their issues (private testing, sampling bias) are about data collection; our issue (structured judge noise) is about model specification.

## Literature-review role

One of the major critique papers to cite; pairs naturally with Huang et al. (Dropping Handful). Together they motivate the broader claim: "something is wrong with Arena CIs, and our work provides one principled fix."
