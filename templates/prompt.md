---
title: Short task name
description: One line describing what this prompt produces.
tags: [domain, task]
variables: [input]
version: 0.1.0
tested_with: []
---

## Prompt

You are helping with <task>. The output will be read by <audience>, who needs it to <purpose>.

<instructions: what to do, in order, and why each constraint matters>

Format the output as:
<structure, length, what to omit>

If the input is insufficient to do this well, say what is missing instead of guessing.

<input>
{{input}}
</input>

## Notes

- **Use when:** …
- **Avoid when:** …
- **Failure modes:** …

## Changelog

- 0.1.0 — initial version
