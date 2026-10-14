---
title: Debug — root cause analysis
description: Hypothesis-driven diagnosis of a bug from symptoms, error output and code.
tags: [coding, debugging]
variables: [symptom, error, code, already_tried]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

Help me find the root cause of a bug. I want the cause, not a patch that hides the symptom — a fix that makes the error disappear without explaining it usually resurfaces elsewhere.

What I observe:
<symptom>
{{symptom}}
</symptom>

Error output / logs:
<error>
{{error}}
</error>

Relevant code:
<code>
{{code}}
</code>

What I have already tried:
<already_tried>
{{already_tried}}
</already_tried>

Respond in this structure:

1. **Reading of the evidence** — what the error and symptom actually tell us, and what they rule out. Quote the specific lines that matter.
2. **Hypotheses** — up to four candidate causes, most likely first. For each: why it fits the evidence, what does not fit, and one cheap check (a print, an assertion, a one-line command) that would confirm or eliminate it.
3. **Most likely cause** — your best call and your confidence (high / medium / low).
4. **Fix** — the change that addresses the root cause, plus a regression test that would have caught it.

If the evidence is not enough to rank hypotheses, say which single additional piece of information would help most rather than guessing.

## Notes

- **Use when:** you have been stuck more than ~15 minutes, or the bug is intermittent.
- The `already_tried` field matters: it stops the model from suggesting what you ruled out.
- Paste the full stack trace, not a summary; the frame order is often the clue.

## Changelog

- 1.0.0 — initial version
