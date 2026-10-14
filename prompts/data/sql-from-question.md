---
title: SQL from a business question
description: Translate a business question into SQL against a given schema, with assumptions made explicit.
tags: [data, sql]
variables: [dialect, schema, question]
version: 1.0.0
tested_with: [claude-opus-5-5, claude-sonnet-5-5]
---

## Prompt

Write a {{dialect}} query that answers the business question below, using only the tables and columns in the schema. The result will be used to make a decision, so a query that runs but answers a slightly different question is the worst outcome — surface every interpretation choice.

<schema>
{{schema}}
</schema>

<question>
{{question}}
</question>

Respond with:

1. **Interpretation** — restate the question as a precise metric definition: grain (one row per what?), filters, time window, how to treat nulls, duplicates and cancelled/test records.
2. **Assumptions** — every choice the question leaves open, numbered, so I can correct them by number.
3. **Query** — readable SQL: CTEs over nested subqueries, one CTE per logical step, a short comment on each CTE. Reference only columns that exist in the schema.
4. **Sanity checks** — 2–3 small queries I can run to verify the result (row counts, a known total, a spot-check on one entity).

If the schema cannot answer the question, say which data is missing instead of approximating silently.

## Notes

- **Use when:** ad-hoc analysis, or drafting a metric definition with stakeholders.
- Paste the schema as `CREATE TABLE` statements or `table(column type, …)` lines; include a few sample rows if column semantics are ambiguous.
- Works for Dremio, DuckDB, Postgres, BigQuery, Snowflake — name the dialect, as date functions differ.

## Changelog

- 1.0.0 — initial version
