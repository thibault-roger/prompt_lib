---
title: Data quality audit
description: Inspect a dataset profile and sample to list concrete, checkable quality issues.
tags: [data, quality, profiling]
variables: [dataset_purpose, profile, sample]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

Audit the quality of a dataset before it is used for: {{dataset_purpose}}.

Column profile (types, null counts, distinct counts, min/max — e.g. the output of `df.describe()` or `df.schema` plus null counts):
<profile>
{{profile}}
</profile>

Sample rows:
<sample>
{{sample}}
</sample>

Look for issues that would distort the stated purpose — not every theoretical imperfection. Check in particular:
- **Types**: numbers or dates stored as strings, mixed formats, wrong precision
- **Completeness**: nulls, empty strings or sentinel values (`-1`, `9999-12-31`, `"N/A"`) standing in for missing data
- **Validity**: out-of-range values, impossible dates, negative quantities, inconsistent categories (`"FR"`, `"France"`, `"fr"`)
- **Uniqueness**: likely key columns that are not unique, duplicated rows
- **Consistency**: columns that should agree but may not (start ≤ end, total = sum of parts)

Return a table with columns: `#`, `column(s)`, `issue`, `evidence` (the specific value or stat you saw), `impact on purpose`, `check` (a Polars expression or SQL predicate that counts affected rows). Order by impact. After the table, list what you could *not* assess from a profile and sample alone.

## Notes

- **Use when:** onboarding a new source, or before building a model or dashboard on unfamiliar data.
- Generate the profile cheaply with Polars: `lf.describe()` and `lf.select(pl.all().null_count()).collect()`; sample with `lf.collect().sample(30, seed=0)` on a manageable slice.
- Never paste sensitive rows; mask PII before sampling.

## Changelog

- 1.0.0 — initial version
