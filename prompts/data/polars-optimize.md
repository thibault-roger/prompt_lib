---
title: Optimize with Polars
description: Rewrite pandas or eager Polars code as idiomatic, memory-efficient lazy Polars.
tags: [data, polars, performance]
variables: [code, data_size, constraints]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

Rewrite the following data-processing code as idiomatic Polars (>= 1.0) using the lazy API. The goal is lower runtime and peak memory on a single machine, with identical results.

<code>
{{code}}
</code>

Data size and shape: {{data_size}}
Constraints (environment, output format, libraries that must stay): {{constraints}}

Apply, where they fit:
- Start from `pl.scan_*` instead of `read_*`, so projection and predicate pushdown reach the file reader.
- Replace row-wise Python (`apply`, `map_elements`, loops, `iterrows`) with native expressions; if a UDF is genuinely unavoidable, say why.
- Combine multiple passes into one `select` / `with_columns` / `group_by().agg()`.
- Use window expressions (`.over()`) instead of group-then-join.
- Use the streaming engine (`collect(engine="streaming")` or `sink_parquet`) when data may exceed memory.
- Pick appropriate dtypes (`Categorical`/`Enum`, smaller ints, `Date` vs `Datetime`).

Return:
1. The rewritten code, runnable as is.
2. A short table: original pattern → replacement → why it is faster or lighter.
3. Any place where results could differ (null handling, sort stability, float precision, join semantics) and how to verify equivalence, e.g. with `polars.testing.assert_frame_equal`.
4. How to confirm the gain: `lf.explain()` to check pushdown, `lf.profile()` for per-node timing.

## Notes

- **Use when:** migrating pandas jobs, or an eager Polars script runs out of memory.
- Pairs with the `data-engineer` agent when the rewrite spans several files.
- See the companion `polars/` learning repo for the reasoning behind each pattern.

## Changelog

- 1.0.0 — initial version
