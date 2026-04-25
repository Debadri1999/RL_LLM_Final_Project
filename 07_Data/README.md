# 07_Data — Dataset folder

This folder holds the arena-140k dataset and any derived parquet files. It is empty at project start; `arena_140k_train.parquet` will be created by the download script below.

## To download arena-140k (on your local machine)

```bash
cd "C:\Users\DOUBLEDO_GAMING\OneDrive\Desktop\PURDUE SPRING'25\MOD-4\MGMT-59000-RL&LLM\Final_Project"
pip install -r 03_Code\requirements.txt
python 03_Code\01_data\download_arena.py
```

Expected result:
- `07_Data/arena_140k/arena_140k_train.parquet` (valid, readable)
- 135,634 rows
- ~500 MB uncompressed parquet (conversations take most of the space)

## After download — produce the cleaned working subset

Follow `03_Code/01_data/exploration_checklist.md` to produce `07_Data/arena_clean.parquet`, which is the filtered subset (top-20 models, English-only, non-tie battles, with derived `category` column) that all downstream analysis uses.

## What lives in this folder after the pipeline runs

```
07_Data/
├── arena_140k/
│   └── arena_140k_train.parquet           ← raw download
├── arena_clean.parquet                    ← cleaned working subset
├── standard_btl_scores.parquet            ← baseline BTL + CIs
├── hierarchical_btl_scores.parquet        ← our model + CIs
├── simulation_results.parquet             ← simulation outputs
├── results/
│   ├── survival_summary.parquet           ← headline: rank-gap survival per category
│   ├── flipped_pairs.parquet              ← specific pairs that flipped significance
│   └── variance_decomposition.parquet     ← per-model 4-component decomposition
└── figures/
    ├── coverage_by_noise_level.png        ← simulation figure
    ├── survival_by_category.png           ← headline figure
    └── ...
```
