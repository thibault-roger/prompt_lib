---
title: Technical explainer
description: Explain a technical concept at a chosen depth, building a correct mental model.
tags: [writing, teaching, explanation]
variables: [topic, reader, depth]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt

Explain {{topic}} to {{reader}}. Target depth: {{depth}} (one of: intuition, working knowledge, expert).

The aim is a correct mental model the reader can reason with, not a list of facts. So:
- Open with the problem the concept solves — why it exists — before what it is.
- Introduce at most one new term per paragraph, and define it in plain words the first time.
- Use one concrete running example throughout rather than several disconnected ones. Include a short runnable code snippet if the topic is code-related.
- Name the most common misconception and show why it is wrong.
- End with "When it matters / when it doesn't": the practical boundary of the concept.

Length: about 300 words for intuition, 600 for working knowledge, 1,000 for expert. Use headings only if the explanation exceeds ~500 words. Do not hedge with phrases like "in simple terms"; just write simply.

## Notes

- **Use when:** writing docs, onboarding material, or learning something yourself.
- Ask for a follow-up quiz ("give me 3 questions that test this mental model") to check understanding.

## Changelog

- 1.0.0 — initial version
