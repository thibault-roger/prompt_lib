---
title: Decision memo
description: One-page memo laying out options, trade-offs and a clear recommendation.
tags: [analysis, decision, writing]
variables: [decision, context, options, criteria]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

Write a one-page decision memo. The reader is the person who has to make the call; they have ten minutes and want a recommendation they can challenge, not a neutral survey.

Decision to make:
<decision>
{{decision}}
</decision>

Context (situation, constraints, deadline, stakeholders):
<context>
{{context}}
</context>

Options under consideration (add a missing obvious option if there is one, and say you added it):
<options>
{{options}}
</options>

Criteria that matter, in rough priority order:
<criteria>
{{criteria}}
</criteria>

Structure:
1. **Recommendation** — first line, one sentence, then the 2–3 reasons that carry it.
2. **Options compared** — a table: options as rows, criteria as columns, short qualitative cells. Bold the deciding cell(s).
3. **What would change my mind** — the conditions or evidence under which a different option wins.
4. **Risks and mitigations** for the recommended option.
5. **Next steps** — the first two concrete actions if the recommendation is accepted.

Separate facts from judgement: when a cell or claim rests on an assumption, mark it `(assumption)`. If the context is too thin to recommend responsibly, give the recommendation conditionally and list what needs confirming.

## Notes

- **Use when:** tooling choices, build-vs-buy, architecture options, hiring/prioritization trade-offs.
- Run it twice with the criteria order swapped to see how sensitive the recommendation is.

## Changelog

- 1.0.0 — initial version
