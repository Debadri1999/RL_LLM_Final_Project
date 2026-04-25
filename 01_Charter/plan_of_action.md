# Master Plan of Action

**Project:** Pair-Heterogeneous Uncertainty in LLM Arena Leaderboards
**Team:** Debadri Sanyal + 1 teammate
**Timeline:** April 19 → May 1, 2026 (presentation April 27 or 29)
**Status at authoring:** Charter locked, literature review drafted, novelty audit complete, paper summaries written, code scaffolding created.

This document is the end-to-end execution plan. It covers everything from data collection through submission, with each phase having: **objective, inputs, outputs, owner, check-before-moving-on criteria.**

---

## Phase 0 — Environment and data (Day 1: Apr 20)

### 0.1 Environment setup (both teammates, ~1 hour)

**Objective:** Working Python environment identical on both laptops.

- Install Python 3.10+ (Colab already ships this).
- Install requirements: `pip install -r 03_Code/requirements.txt`.
- Key packages: `datasets` (HuggingFace), `pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`, `tqdm`, `jupyter`.
- Colab: mount Google Drive for persistent storage of arena-140k.
- Test: `python -c "from datasets import load_dataset; print('ok')"`

**Output:** Both teammates can import `datasets`, `pandas`, `scipy`, `statsmodels` successfully.

### 0.2 Arena-140k download (one teammate, ~15 min)

**Objective:** Local copy of arena-140k, cached for all downstream work.

- Run `03_Code/01_data/download_arena.py`. This downloads `lmarena-ai/arena-human-preference-140k` from HuggingFace and caches it to `07_Data/arena_140k/`.
- Expected size: 135,634 rows, ~500MB compressed (much more uncompressed because conversations).

**Output:** Parquet / Arrow cache in `07_Data/arena_140k/`. Row count verified = 135,634.

### 0.3 Data exploration notebook (one teammate, ~2 hours)

**Objective:** Understand the data structure before writing models.

- Load dataset → pandas DataFrame.
- Answer: How many unique models? (53) How many battles per model? Which top-20 models have the most battles? Distribution of `winner` outcomes? Distribution of `category_tag`? Distribution of `language`? Timestamp coverage?
- Create a filtered subset: top-20 models by battle count, English-only, non-tie outcomes. This is our **working subset** for all downstream analysis. Document the filter in a cell.

**Output:** `03_Code/01_data/exploration.ipynb` with summary statistics and one saved `arena_clean.parquet` in `07_Data/`.

### ✅ Gate before Phase 1

- [ ] Arena-140k downloaded and cached
- [ ] Working subset defined and documented
- [ ] Both teammates can load the data on their laptops

---

## Phase 1 — Baseline BTL (Days 2–3: Apr 21–22)

### 1.1 Standard BTL point estimation (Teammate A)

**Objective:** Reproduce the standard Chatbot Arena scoring pipeline. This is the baseline against which our hierarchical correction will be compared.

**Algorithm:**
- Model each battle `(i, j, y)` where `y ∈ {0, 1}` indicates whether model `i` wins.
- Likelihood: `L = Π_k σ(s_{i_k} − s_{j_k})^{y_k} · (1 − σ(...))^{1−y_k}`
- Maximize log-likelihood via scipy.optimize (L-BFGS-B) or custom gradient descent.
- Fix one model's score to 0 for identifiability.

**Implementation plan:**
- File: `03_Code/02_btl_standard/btl_standard.py`
- Class `StandardBTL` with methods: `fit(battles)`, `scores()`, `predict_prob(i, j)`, `bootstrap_ci(n_boot=1000)`.

**Validation:** Fit on arena subset. Check that top-5 scores roughly match the public Arena leaderboard (±small deviation due to subsetting).

### 1.2 Standard BTL confidence intervals (Teammate A)

**Objective:** Implement bootstrap CIs as the baseline uncertainty method.

**Algorithm:** Sample battles with replacement, re-fit BTL, record scores. Repeat 1000 times. Compute 2.5% and 97.5% quantiles per model.

**Output:** A dataframe with `model, score, ci_lower, ci_upper`. This is our baseline leaderboard.

**Validation:** CI widths should be tiny for top-ranked models (many battles) and wider for tail models (few battles) — check this qualitatively.

### ✅ Gate before Phase 2

- [ ] Standard BTL reproduces recognizable Arena-style ranking
- [ ] Bootstrap CIs computed
- [ ] "Significant rank gap" pairs list defined: pairs (i, j) where `ci_lower(i) > ci_upper(j)`. Count them — this is our baseline `N_sig`.

---

## Phase 2 — Hierarchical BTL model (Days 3–4: Apr 22–23)

### 2.1 Math derivation (Teammate B / you, 2–3 hours)

**Objective:** Write down the pair-heterogeneous hierarchical BTL model formally.

**Proposed generative model:**

```
s_i ~ arbitrary (to be estimated)
σ²_judge(prompt_category, pair_distance) = exp(α_0 + α_c · 1[category=c] + α_d · |s_i − s_j|)
ε_k | (prompt, model pair) ~ N(0, σ²_judge)
P(i beats j | battle k) = Φ((s_i − s_j) / √(1 + σ²_judge(...)))
```

where Φ is the standard normal CDF (Thurstone formulation) or we keep σ in a logistic formulation. The key structural claim: **σ²_judge is a function of prompt category and pair distance**, not a per-judge scalar.

Write derivation into `04_Report/section2_derivation.tex` (LaTeX).

### 2.2 Implementation (Teammate B / you, 4–6 hours)

**Objective:** Fit the hierarchical BTL model on arena data.

- File: `03_Code/03_btl_hierarchical/btl_hierarchical.py`
- Class `HierarchicalBTL` with methods: `fit(battles, prompt_categories, ...)`, `scores()`, `noise_variance_for(category, pair_distance)`, `bootstrap_ci(n_boot=1000)`.
- Optimize jointly over `(s, α)` using scipy L-BFGS-B. May need EM if direct joint optimization is unstable.
- Identifiability: fix one model's score to 0 and fix one reference category for α.

**Output:** Fitted model plus a new CI table for the arena subset.

### 2.3 Variance decomposition (Teammate B / you, 2–3 hours)

**Objective:** Produce the four-component decomposition of `Var(ŝ_i)`.

- Numerical decomposition: refit the model with each noise component zeroed out; record how `Var(ŝ_i)` changes. Use delta-method or bootstrap if cleaner.
- File: `03_Code/06_variance_decomposition/variance_decomp.py`
- Output: Per-model table with columns `V_sampling, V_judge_identity, V_prompt_category, V_pair_distance, V_total`.

### ✅ Gate before Phase 3

- [ ] Hierarchical BTL converges on arena subset
- [ ] Variance decomposition runs and numbers look sensible (all non-negative, sum approximately to total)

---

## Phase 3 — Simulation with known ground truth (Day 4: Apr 23)

### 3.1 Build controlled simulation (Teammate B / you, 3–4 hours)

**Objective:** Rebuild the original outline's simulation so that standard BTL *visibly* undercovers at realistic noise.

**Setup:**
- 10 models with true scores drawn from `Uniform(0, 3)` (covers realistic Elo range in log-odds).
- 4 prompt categories with category-specific noise levels `σ²_c ∈ {0.05, 0.25, 0.50, 1.00}`.
- 5000 battles per trial (vs 400 in original outline — more battles make standard BTL *more* confident, amplifying the undercoverage story).
- 500 trials per noise-level scenario.

**Hypothesis to demonstrate:** Under pair-heterogeneous noise, standard BTL coverage drops below 95%. With sufficient noise and battle count, we should see 70–85% coverage for standard BTL vs ~95% for our hierarchical correction.

**Output:** `03_Code/04_simulation/simulation.py` with a table of coverage-probability results across scenarios and a coverage-comparison plot saved to `03_Code/04_simulation/figures/`.

### ✅ Gate before Phase 4

- [ ] Simulation shows standard BTL undercovers (clear gap below 95%) in the high-noise regime
- [ ] Hierarchical BTL stays at nominal coverage (~95%)
- [ ] Coverage table and plot saved

---

## Phase 4 — Real-data analysis on arena-140k (Days 5–6: Apr 24–25)

### 4.1 Headline experiment: rank-gap survival (both teammates, 4–6 hours)

**Objective:** Compute our headline empirical claim.

**Procedure:**
1. Using standard BTL + bootstrap on arena subset → list of "significant" pairs: `N_sig_standard = |{(i,j) : ci_lower_i > ci_upper_j}|`.
2. Using hierarchical BTL + bootstrap on same subset → `N_sig_hierarchical`.
3. Rank-gap survival rate = `N_sig_hierarchical / N_sig_standard`.
4. List the top-20 model pairs that flip from significant-to-not-significant — this is the tables we show in the report.

**File:** `03_Code/05_real_data_analysis/arena_survival_analysis.py`.

**Expected output:** A headline number like "Only X% of currently-significant pairwise rank gaps on Chatbot Arena survive the hierarchical correction." We don't know X yet; the project is genuinely empirical.

### 4.2 Subgroup analysis (both teammates, 2–3 hours)

**Objective:** Show how rank-gap survival varies by prompt category.

- For each category in `{math, creative writing, hard prompts, instruction following, code}`, recompute the analysis on the category subset.
- Output: A per-category table of rank-gap survival rates.
- Expected: survival rate is *lower* in close/high-noise categories, *higher* in high-signal categories.

### 4.3 Noise-component attribution (both teammates, 2 hours)

**Objective:** For each of the top-20 "flipped" pairs, report which noise component dominates.

- Use the variance decomposition output to identify: for each flipped pair, is its high `Var(ŝ_i − ŝ_j)` primarily driven by prompt-category noise, pair-distance noise, or unmodeled judge-identity noise?
- Practitioner upshot: which pairs could be resolved by more data vs. which are structurally ambiguous.

### ✅ Gate before Phase 5

- [ ] Headline survival-rate number computed
- [ ] Subgroup breakdown computed
- [ ] At least one compelling figure produced: "Pair X was significant; after correction it isn't; here's why"

---

## Phase 5 — Writing (Days 7–9: Apr 26–28)

Schedule the writing phase to overlap with the presentation. The presentation is due April 27 or 29; the final report is due May 1. Delivering a polished presentation first is the priority because it also forces tightening of the narrative.

### 5.1 Slide deck (Teammate A lead, Teammate B review, Day 7)

**Objective:** 10-minute talk deck for Apr 27 or 29 presentation.

**Structure (8–10 slides):**
1. **Opener hook** — "2 Elo points between GPT-4o and Claude — can you trust the gap?"
2. **What standard BTL assumes** — the implicit IID noiseless-judgment assumption
3. **Why it's wrong** — empirical evidence from prior work (rank fragility, position bias, quality-gap-dependent noise)
4. **Our contribution** — pair-heterogeneous hierarchical BTL, in one slide with the model picture
5. **Simulation evidence** — coverage-probability plot
6. **Arena evidence** — the headline number: survival rate
7. **Which pairs flipped** — concrete examples
8. **What it means** — practitioner takeaway
9. **Future work** — real per-judge heterogeneity when judge IDs are available; extension to tournament / round-robin leaderboards
10. **Q&A holding slide**

**File:** `05_Presentation/slides.pptx` or Google Slides; export final PDF for submission.

### 5.2 Report draft (both teammates, Days 7–8)

**NeurIPS 2026 template** — copy `Formatting_Instructions_For_NeurIPS_2026/neurips_2026.tex` into `04_Report/main.tex` and start editing.

**Section allocation (≤8 pages, excluding references and appendix):**

| § | Section | Pages | Owner | Status |
|---|---|---|---|---|
| 1 | Introduction and contributions | 0.75 | B | Pending |
| 2 | Background: BTL and Arena | 1.0 | A | Pending |
| 3 | Paper summary: Xu et al. (2026) | 1.25 | B | Pending |
| 4 | New research direction | 1.25 | B | Pending |
| 5 | Proposed solution — methodology | 1.5 | B | Pending |
| 6 | Literature review | 1.25 | A | In progress (draft in `02_Literature_Notes/literature_review.md`) |
| 7 | Preliminary evidence — simulation + arena | 0.75 | A | Pending |
| 8 | Conclusion and future work | 0.25 | A | Pending |
| References | (doesn't count toward 8-page limit) | — | A | Pending |
| Appendix A | Variance decomposition derivation | — | B | Pending |
| Appendix B | Simulation full tables | — | A | Pending |

### 5.3 Verification pass (Day 9)

Use the `verification-before-completion` discipline:
- [ ] Every citation checked against `bibliography.md`
- [ ] Every number in the text matches the actual simulation/analysis output
- [ ] Math derivation cross-checked against simulation output numerically
- [ ] Page count checked (≤ 8 excluding references / appendix)
- [ ] NeurIPS template formatting preserved (no manual style tweaks breaking paper compile)

### ✅ Gate before Phase 6

- [ ] All sections have at least a rough draft
- [ ] Headline result and one compelling figure are in the report
- [ ] Slides are rehearsed once end-to-end under 10 min

---

## Phase 6 — Submission (Apr 30 – May 1)

### 6.1 Final polish (both teammates, Apr 30)

- Incorporate presentation feedback from class
- Proofread entire report
- Regenerate all figures at publication quality (300 DPI, consistent fonts)
- Verify BibTeX references compile cleanly in LaTeX
- Compile final PDF; check no warnings

### 6.2 Submit (May 1)

- Upload final PDF to Brightspace
- Archive final submission state in `08_Final_Submission/` folder (create on this day)
- Commit complete codebase if you want a post-course artifact

---

## Parallel workstreams and dependencies

```
Day 1 ─┬─ Environment setup  (both)
       └─ Arena download  (A)
            │
Day 2 ─┬─ Data exploration  (A)
       ├─ Standard BTL implementation  (A)
       └─ Hierarchical BTL math derivation  (B)
            │
Day 3 ─┬─ Standard BTL bootstrap CIs  (A)
       └─ Hierarchical BTL implementation  (B)
            │
Day 4 ─┬─ Variance decomposition  (B)
       └─ Simulation setup  (B)
            │
Day 5 ─┬─ Simulation runs and analysis  (B)
       └─ Real-data survival analysis  (A)
            │
Day 6 ─── Subgroup + noise-attribution analysis  (both)
            │
Day 7 ─┬─ Slides v1  (A)
       └─ Report sections 1, 3, 4, 5  (B)
            │
Day 8 ─┬─ Present! (Apr 27 or 29)
       └─ Report sections 2, 6, 7, 8  (A)
            │
Day 9 ─── Verification + revisions  (both)
            │
Day 10 ── Submit final report (May 1)
```

---

## Risk register (continuously monitored)

| Risk | Mitigation |
|---|---|
| arena-140k too large for Colab memory | Stream-load and subset to top-20 models, English-only, non-tie |
| Hierarchical BTL fails to converge | Use warm start from standard BTL scores; try EM as backup; reduce parameter count |
| Simulation still shows standard BTL hitting 95% coverage | Push noise higher; try heavy-tailed noise; check whether pair-distance dependence itself dominates |
| Novelty overlap discovered after reading full Xu et al. text | Pivot framing to variance decomposition + arena audit (Deltas 2+3 are sufficient independently) |
| Variance decomposition math is incorrect | Numerical validation via simulation; fall back to Monte-Carlo decomposition if closed-form fails |
| Time slip on writing | Cut Appendix B to one table; skip subgroup-level analysis if Phase 4.1 alone is strong |

---

## Daily check-in protocol

Every day, both teammates exchange a 3-line status message:
- **Yesterday:** what got done
- **Today:** what I'll finish
- **Blockers:** anything I'm stuck on

Status file: `06_Notes/daily_status.md` — append-only, newest on top.

---

## Quality bar

**For a strong A-grade submission:**
- Report tells a single focused story from hook to headline number (no survey drift)
- At least one *quotable* finding (the rank-gap survival percentage)
- Every math claim is numerically checked
- Xu et al. (2026) is explicitly cited and differentiated on all three deltas
- Presentation is under 10 minutes and well-rehearsed

**Non-negotiables:**
- arena-140k empirical analysis is shipped (not optional)
- Variance decomposition is computed and reported (not just claimed)
- Simulation visibly shows standard BTL undercoverage (original outline table is fixed)
