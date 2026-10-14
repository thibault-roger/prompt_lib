---
title: Code review
description: Severity-ranked review of a diff that surfaces real bugs before style nits.
tags: [coding, review]
variables: [language, context, diff]
version: 1.0.0
tested_with: [claude-opus-5-5, claude-sonnet-5-5]
---

## Prompt

Review the following {{language}} change. The reader is the author, who will fix what you flag before merging, so every finding should be something worth their time.

Context about the change (purpose, constraints, related code):
<context>
{{context}}
</context>

<diff>
{{diff}}
</diff>

Work in this order:
1. Understand what the change is trying to do. If the intent is unclear, say so first — a review against the wrong intent is worse than none.
2. Look for correctness problems: logic errors, unhandled edge cases (empty, null, very large, concurrent), broken error handling, resource leaks, security issues (injection, secrets, unsafe deserialization), and behavior changes the author may not have intended.
3. Only then look at maintainability: naming, duplication, missing tests for new behavior.

For each finding, give:
- **Severity**: `blocker` (wrong results, data loss, security), `major` (likely bug or significant risk), `minor` (maintainability), `nit` (optional)
- **Location**: file and line or function
- **Problem**: what goes wrong, with a concrete input or scenario that triggers it
- **Fix**: the smallest change that resolves it, as a code snippet when that is clearer than prose

Rank findings most severe first. Report only issues you can justify with a concrete scenario; if you are unsure, mark it `(uncertain)` and say what would confirm it. Skip praise and skip restating what the diff does. If you find nothing above `nit`, say so plainly in one line.

## Notes

- **Use when:** reviewing your own change before a PR, or a colleague's PR you lack time to read line-by-line.
- **Avoid when:** the diff is over ~1,500 lines — split it, or use the `code-reviewer` agent, which can read surrounding files.
- **Failure modes:** without `context`, the model may flag intended behavior changes as bugs. Pass at least one sentence of intent.
- Leave `context` as "none" rather than empty if you have nothing to add.

## Changelog

- 1.0.0 — initial version
