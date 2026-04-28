# MGMT 590 Final Project — Working Folder

**Track:** 2 (LLM Evaluation)
**Project title:** Pair-Heterogeneous Uncertainty in LLM Arena Leaderboards
**Team size:** 2 (Debadri Sanyal + teammate)
**Deadlines:** Presentation Apr 27 or 29 · Final report May 1, 2026

---

## Locked one-sentence problem statement

> Once judge noise in Chatbot Arena is modeled as a structured function of prompt category and model-pair distance (rather than as a per-judge scalar), **what fraction of the leaderboard's currently-"significant" pairwise rank gaps survive?**

Full charter: `01_Charter/MGMT590_Final_Project_Charter.docx`
Master execution plan: `01_Charter/plan_of_action.md`

---

## Folder structure

| Folder | Contents |
|---|---|
| `01_Charter/` | Locked problem statement (.docx) + master plan of action (.md). Single source of truth for scope and timeline. |
| `02_Literature_Notes/` | Bibliography (`bibliography.md`), full literature review (`literature_review.md`), 9 individual paper summaries in `paper_summaries/`, novelty audit (`novelty_analysis.md`), classical refs notes, and `download_papers.sh` to bulk-fetch PDFs. |
| `03_Code/` | All Python source. Subfolders: `01_data/`, `02_btl_standard/`, `03_btl_hierarchical/`, `04_simulation/`, `05_real_data_analysis/`, `06_variance_decomposition/`, `07_results/`. See `03_Code/README.md` for the full pipeline. |
| `04_Report/` | NeurIPS 2026 LaTeX report (working drafts and final PDF). Empty until Phase 5. |
| `05_Presentation/` | 10-minute slide deck for Apr 27 or 29. Empty until Phase 5. |
| `06_Notes/` | Misc notes including the teammate's original outline preserved for diff. |
| `07_Data/` | arena-140k dataset (downloaded by `03_Code/01_data/download_arena.py`) and any derived parquet files. |
| `Formatting_Instructions_For_NeurIPS_2026/` | Official NeurIPS 2026 LaTeX template (do not modify in place — copy into `04_Report/`). |
| `Final Project.pdf` | Original course brief. |

---

## What's already done (as of April 19, 2026)

- ✅ Track selected: LLM Evaluation (Track 2)
- ✅ Problem statement locked and signed off internally
- ✅ Novelty audit vs Xu et al. (2026) complete
- ✅ Comprehensive literature review drafted (`02_Literature_Notes/literature_review.md`)
- ✅ Bibliography of all required papers with direct URLs (`02_Literature_Notes/bibliography.md`)
- ✅ Helper script for bulk-downloading paper PDFs (`02_Literature_Notes/download_papers.sh`)
- ✅ 9 individual paper summaries in `02_Literature_Notes/paper_summaries/`
- ✅ Master plan of action with 10-day day-by-day schedule (`01_Charter/plan_of_action.md`)
- ✅ Code scaffolding for all pipeline stages (`03_Code/`)
- ✅ Arena-140k download script ready (`03_Code/01_data/download_arena.py`)
- ✅ Standard BTL baseline implemented (`03_Code/02_btl_standard/btl_standard.py`) — runnable
- ✅ Hierarchical BTL skeleton implemented (`03_Code/03_btl_hierarchical/btl_hierarchical.py`) — runnable, model spec needs final cross-check vs derivation
- ✅ Simulation harness scaffolded (`03_Code/04_simulation/simulation.py`) — needs fitting calls wired in (Phase 3 of the plan)
- ✅ Real-data survival analysis stub (`03_Code/05_real_data_analysis/arena_survival_analysis.py`)

## Immediate next actions

For you (and your teammate):

1. **Read** `01_Charter/MGMT590_Final_Project_Charter.docx` and `01_Charter/plan_of_action.md`. Get teammate sign-off on the sharpened direction.
2. **Run on your local machine** (not in this Cowork sandbox):
   - `bash 02_Literature_Notes/download_papers.sh` → downloads all paper PDFs into `02_Literature_Notes/pdfs/`
   - `pip install -r 03_Code/requirements.txt`
   - `python 03_Code/01_data/download_arena.py` → downloads arena-140k into `07_Data/`
3. **Open the Day-1 work**: `03_Code/01_data/exploration_checklist.md` walks through the data exploration cells you should run.
4. Once teammate signs off, ping Claude to:
   - Draft Section 2 ("New Research Direction") of the NeurIPS report in LaTeX
   - Wire up the simulation fitting calls (Phase 3)
   - Begin the real-data analysis once Day 1–4 of the plan is done

---

## Non-negotiables (locked)

1. **arena-140k real-data analysis is the headline differentiator.** Any final report without an arena-140k empirical result is a C-grade submission.
2. **Xu et al. (2026) must be cited and explicitly differentiated** in every version of the report, on all three deltas (pair-heterogeneous noise, variance decomposition, arena audit).
3. **The simulation must actually demonstrate undercoverage.** The original outline's table showed standard BTL hitting 95% nominal coverage — the rebuilt simulation in `03_Code/04_simulation/simulation.py` is designed to produce a 70–85% coverage failure for standard BTL.

---

## Quick reference: where things live

| You want to... | Open this |
|---|---|
| Read the locked problem statement | `01_Charter/MGMT590_Final_Project_Charter.docx` |
| See the day-by-day execution plan | `01_Charter/plan_of_action.md` |
| Read the literature review | `02_Literature_Notes/literature_review.md` |
| Get the bibliography / paper URLs | `02_Literature_Notes/bibliography.md` |
| Bulk-download paper PDFs | `bash 02_Literature_Notes/download_papers.sh` |
| Read summaries of individual papers | `02_Literature_Notes/paper_summaries/` |
| See why our project is novel vs Xu et al. | `02_Literature_Notes/novelty_analysis.md` |
| Set up the Python environment | `pip install -r 03_Code/requirements.txt` |
| Download arena-140k | `python 03_Code/01_data/download_arena.py` |
| Explore the dataset | `03_Code/01_data/exploration_checklist.md` |
| Run the standard BTL baseline | `python 03_Code/02_btl_standard/btl_standard.py` (after exploration step) |
| Read the code pipeline overview | `03_Code/README.md` |

---

## Quality bar (from the master plan)

A strong A-grade submission will have:

- A single focused story from hook to headline number (no survey drift)
- At least one quotable empirical finding (the rank-gap survival percentage on Arena)
- Every math claim cross-checked numerically
- Xu et al. (2026) explicitly cited and differentiated on all three deltas
- A ≤10-minute presentation that has been rehearsed end-to-end

---

## Interactive Dashboard (GitHub Pages)

An interactive, presentation-ready dashboard is available in `docs/` and can be
hosted directly with GitHub Pages.

### Features

- Glassmorphism light UI with animated neural-network background
- Left-side control panel for confidence level, model count, model focus, and variance view
- Interactive plots for:
  - Significant-pair survival sensitivity
  - Variance decomposition by model
  - Flipped-pair fragility hotspots
- Arena-style model-vs-model matchup explorer with live duel inference
- Scroll-based storytelling cards with reveal animation for presentation flow
- Staged intro animation timeline for a cinematic opening sequence
- Color and spacing micro-tuning for projector contrast in presentation mode
- One-click presentation mode (or press `P`) optimized for classroom demo screens
- Dedicated TA/Professor Quick Tour auto-scroll flow (button or press `T`)
- Speaker notes overlay for live presenting (auto-updates by section, press `N` to toggle)
- Auto-generated inference text that adapts to selected parameters

### Local preview

From repository root, run a static file server and open `docs/index.html`:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/docs/`.

### Deploy on GitHub Pages

1. Push the repository to GitHub.
2. In the repository settings, open **Pages**.
3. Set source to **Deploy from a branch**.
4. Select your branch (typically `main`) and folder **`/docs`**.
5. Save; your dashboard will be published automatically.
