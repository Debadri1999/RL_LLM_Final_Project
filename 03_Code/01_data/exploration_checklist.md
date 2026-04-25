# Data exploration checklist — arena-140k

Use this as a menu of cells to run in `exploration.ipynb`. Goal: understand the data before any modeling.

## Loading

```python
import pandas as pd
df = pd.read_parquet("../../07_Data/arena_140k/arena_140k_train.parquet")
print(df.shape)     # expect (135634, ~14)
df.head(3)
```

## Columns to inspect

- [ ] `df["winner"].value_counts()` — how many ties, both_bad, model_a, model_b wins?
- [ ] `df["model_a"].nunique()` and `df["model_b"].nunique()` — should both be 53
- [ ] Battles per model: `pd.concat([df["model_a"], df["model_b"]]).value_counts().head(25)`
- [ ] Category coverage: expand `df["category_tag"]` (dict) → flat dataframe, then value_counts
- [ ] Language distribution: `df["language"].value_counts().head(20)`
- [ ] `df["is_code"].value_counts()`
- [ ] Timestamp coverage: `df["timestamp"].min()`, `df["timestamp"].max()`

## Working-subset definition (document the filter in the notebook)

Recommended filter:
```python
# 1. Non-tie, non-both-bad (we want clean i-beats-j signal)
df = df[df["winner"].isin(["model_a", "model_b"])]

# 2. English only for Phase 4 (remove multilingual heterogeneity for now)
df = df[df["language"] == "English"]

# 3. Top-K models by total battle count (K=20 default)
from collections import Counter
counts = Counter(df["model_a"]) + Counter(df["model_b"])
top_models = [m for m, _ in counts.most_common(20)]
df = df[df["model_a"].isin(top_models) & df["model_b"].isin(top_models)]

print(f"Working subset: {len(df):,} battles across {len(top_models)} models")
```

Expected working-subset size: order of 60–80K battles.

## Deriving the simplified category column

`category_tag` is a dict. For our hierarchical BTL we need a single categorical
"category" per row. Proposed mapping:

```python
def extract_category(tag_dict: dict) -> str:
    if tag_dict is None or len(tag_dict) == 0:
        return "general"
    # priority order — pick the most specific tag
    for key in ["math", "creative_writing", "hard_prompt", "instruction_following", "coding"]:
        if tag_dict.get(key):
            return key
    return "general"
df["category"] = df["category_tag"].apply(extract_category)
```

## Persist

```python
df.to_parquet("../../07_Data/arena_clean.parquet", index=False)
```

## Sanity checks before modeling

- [ ] All battles have `winner in {model_a, model_b}`
- [ ] All `model_a`, `model_b` are in `top_models`
- [ ] No nulls in `category`
- [ ] Battles per model ≥ 1000 for all models in the subset (ensures BTL is well-conditioned)
