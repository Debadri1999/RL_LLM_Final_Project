# Code — MGMT 590 Final Project

All Python code for the project. Organized by pipeline stage; each subfolder is a self-contained module.

## Setup

```bash
cd 03_Code
pip install -r requirements.txt
```

Requires Python 3.10+. Tested with NumPy 1.26, pandas 2.1, SciPy 1.11.

## Pipeline order

| Folder | Stage | Entry point |
|---|---|---|
| `01_data/` | Download and explore arena-140k | `download_arena.py`, `exploration.ipynb` |
| `02_btl_standard/` | Standard Bradley-Terry baseline | `btl_standard.py` |
| `03_btl_hierarchical/` | Our proposed pair-heterogeneous hierarchical BTL | `btl_hierarchical.py` |
| `04_simulation/` | Controlled simulation with known ground truth | `simulation.py` |
| `05_real_data_analysis/` | Arena-140k rank-gap survival analysis (headline result) | `arena_survival_analysis.py` |
| `06_variance_decomposition/` | Four-component variance decomposition | `variance_decomp.py` |
| `07_results/` | Output tables and figures used in report | (populated by scripts above) |

## End-to-end run (reference)

```bash
# Phase 0: Data
python 01_data/download_arena.py
jupyter notebook 01_data/exploration.ipynb       # interactive: produces arena_clean.parquet

# Phase 1: Baseline
python 02_btl_standard/btl_standard.py --input ../07_Data/arena_clean.parquet \
    --output ../07_Data/standard_btl_scores.parquet

# Phase 2: Hierarchical
python 03_btl_hierarchical/btl_hierarchical.py --input ../07_Data/arena_clean.parquet \
    --output ../07_Data/hierarchical_btl_scores.parquet

# Phase 3: Simulation
python 04_simulation/simulation.py --output ../07_Data/simulation_results.parquet

# Phase 4: Real data analysis + variance decomposition
python 05_real_data_analysis/arena_survival_analysis.py
python 06_variance_decomposition/variance_decomp.py
```

All output parquets land in `07_Data/` (gitignored). All figures land in `07_Data/figures/`.

## Notes

- The `datasets` library caches arena-140k in `~/.cache/huggingface/`. On Colab, set `HF_DATASETS_CACHE` to a Drive location to persist across session resets.
- Bootstrap CIs default to 1000 resamples. For quick testing use `--n_boot=100`. For final report use `--n_boot=2000`.
- All scripts are idempotent: safe to re-run; they check for cached outputs before recomputing.
