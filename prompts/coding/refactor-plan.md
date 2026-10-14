---
title: Refactor plan
description: Turn a refactoring goal into small, independently shippable steps with safety checks.
tags: [coding, refactoring, planning]
variables: [goal, code, constraints]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

I want to refactor some code. Produce a plan, not the final code: big-bang refactors are where regressions hide, so I want a sequence of small steps where the system works after each one.

Goal of the refactor:
<goal>
{{goal}}
</goal>

Current code:
<code>
{{code}}
</code>

Constraints (public APIs to keep, deadlines, test coverage, team conventions):
<constraints>
{{constraints}}
</constraints>

Give me:

1. **Current-state diagnosis** — the specific problems in the code that block the goal (3–6 bullets, each pointing at a location).
2. **Target shape** — a short sketch of the end state (module/function outline, not full code).
3. **Steps** — a numbered list. Each step must be shippable on its own and include:
   - what changes
   - how to verify it (which tests to run or add)
   - risk: low / medium / high, and why
4. **Safety net first** — if test coverage is too thin to refactor safely, make step 1 "add characterization tests" and say which behaviors they must pin down.
5. **What not to touch** — anything tempting but out of scope.

Prefer steps that keep old and new paths side by side (introduce → migrate callers → delete) over in-place rewrites.

## Notes

- **Use when:** the change touches more than one module, or code you did not write.
- Feed each step back with the `code-review` prompt as you implement it.

## Changelog

- 1.0.0 — initial version
