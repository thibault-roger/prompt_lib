---
title: Dataset onboarding
description: Bring a new data source from raw files to trusted, queryable tables.
tags: [workflow, data]
version: 1.0.0
---

# Dataset onboarding

Use this when a new source lands (a Parquet drop on MinIO, a Dremio table, a CSV export) and you need to know whether it can be trusted before building on it.

| # | Step | Tool | Output |
|---|------|------|--------|
| 1 | Profile | Polars snippet below | Schema, null counts, sample |
| 2 | Audit | `prompts/data/data-quality-audit.md` | Ranked issues, each with a check expression |
| 3 | Clean & load | `data-engineer` agent | Lazy pipeline that fixes or flags each issue, writes Parquet |
| 4 | Test | `test-writer` agent | Tests asserting each audit check now passes |
| 5 | Query | `prompts/data/sql-from-question.md` | First business queries with explicit assumptions |

## Step 1 — profile cheaply

```python
import polars as pl

lf = pl.scan_parquet("path/or/s3/uri/*.parquet")  # add storage_options for MinIO

print(lf.collect_schema())
print(lf.select(pl.all().null_count()).collect())
print(lf.describe())
print(lf.head(10_000).collect().sample(30, seed=0))
```

Paste the outputs into the `profile` and `sample` variables of the audit prompt (mask PII first):

```bash
python3 scripts/render.py prompts/data/data-quality-audit.md \
  --var dataset_purpose="weekly revenue dashboard" \
  --var profile=@profile.txt --var sample=@sample.txt | pbcopy
```

## Step 3 — hand-off to the agent

```text
Use the data-engineer agent. Build a lazy Polars pipeline that reads <source>,
addresses issues 1–N from this audit: <paste table>, and writes to <dest>.
Verify each audit check returns 0 affected rows on the output.
```
