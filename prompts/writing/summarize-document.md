---
title: Summarize a document
description: Audience-aware summary that leads with decisions, actions and open questions.
tags: [writing, summary]
variables: [audience, purpose, document]
version: 1.0.0
tested_with: [claude-opus-5-5, claude-haiku-5-5]
---

## Prompt

Summarize the document below for {{audience}}, who will use the summary to {{purpose}}. They will read the first few lines carefully and skim the rest, so put what they need to act on first.

<document>
{{document}}
</document>

Structure:
1. **Bottom line** — 2–3 sentences: what this document means for the reader.
2. **Key points** — at most 6 bullets, each a complete claim (not a topic label), most important first.
3. **Decisions and actions** — who decided or must do what, by when, if stated.
4. **Open questions / risks** — what is unresolved or contested.

Stay faithful to the source: do not add facts, and when the document is ambiguous, say so rather than resolving it. Keep numbers, names and dates exactly as written. Omit any section that has no content rather than filling it.

## Notes

- **Use when:** meeting notes, long email threads, specs, reports.
- Changing `audience` changes the output a lot ("the CFO" vs "the on-call engineer") — be specific.
- Fast models (Haiku) handle this well for short inputs; use a larger model for documents with subtle disagreements.

## Changelog

- 1.0.0 — initial version
