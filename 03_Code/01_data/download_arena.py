"""
download_arena.py
-----------------
Download the arena-140k dataset from HuggingFace and cache it locally.

Dataset: lmarena-ai/arena-human-preference-140k
License: CC-BY-4.0 (prompts)
Size: 135,634 rows; 53 models; 126 languages
Schema summary:
    id, model_a, model_b, winner (model_a/model_b/tie/both_bad),
    evaluation_session_id, evaluation_order, conversation_a, conversation_b,
    full_conversation, conv_metadata, category_tag, language, is_code, timestamp

Usage
-----
    python download_arena.py
    # or, with custom cache:
    HF_DATASETS_CACHE=/path/to/cache python download_arena.py

Outputs
-------
- 07_Data/arena_140k/ (parquet, split=train)
- Prints schema summary + row count for verification.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print("ERROR: `datasets` not installed. Run: pip install -r ../requirements.txt")
    sys.exit(1)

# ---- Paths (relative to project root) -------------------------------------
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent       # ../../
DATA_DIR = PROJECT_ROOT / "07_Data" / "arena_140k"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print(f"Downloading lmarena-ai/arena-human-preference-140k ...")
    print(f"Target directory: {DATA_DIR}")
    print()

    ds = load_dataset("lmarena-ai/arena-human-preference-140k")

    print("Splits:", list(ds.keys()))
    train = ds["train"]
    print(f"Rows: {len(train):,}")
    print("Features:")
    for name, ftype in train.features.items():
        print(f"  {name:28s}  {ftype}")

    # Save as parquet for fast reload.
    out_file = DATA_DIR / "arena_140k_train.parquet"
    print(f"\nSaving to {out_file} ...")
    train.to_parquet(str(out_file))
    print(f"Done. File size: {out_file.stat().st_size / 1e6:.1f} MB")

    # Sanity-check expected values
    assert len(train) == 135_634, (
        f"Expected 135,634 rows; got {len(train):,}. "
        "The dataset may have been updated; update docs + downstream expectations."
    )
    print("\nRow count matches the expected 135,634.")


if __name__ == "__main__":
    main()
