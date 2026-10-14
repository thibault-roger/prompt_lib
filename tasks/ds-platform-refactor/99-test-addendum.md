---
title: "DSP refactor — Test addendum"
description: Mandatory testing requirements appended to the end of every Phase 2–8 prompt.
tags: [task, ds-platform, testing]
variables: []
version: 1.0.0
tested_with: []
---

## Prompt

TESTING REQUIREMENTS FOR THIS PHASE (mandatory)
- Before writing code, list the tests you will write. For each test give an ID (<PHASE>-<AREA>-<NN>), the level (unit / contract / integration / e2e / perf / security), what it proves, and how it fails.
- Tests must run offline, using only packages from our internal mirror, with no external services. Use fixtures, local Unix sockets, temp dirs and local registries.
- Each test must be deterministic: fixed seeds, no sleeps used as synchronisation (poll with a timeout instead), and isolated temp dirs. Clean up processes on teardown, including on failure.
- Every bug found during this phase gets a regression test named after it.
- Assert behaviour, not implementation: status codes, payloads, exit codes, files produced, log lines that matter.
- End the phase with a TEST REPORT:
  - tests run / passed / failed / skipped, with the reason for each skip;
  - what was NOT tested and why;
  - the exact commands to re-run everything.
- A phase is not done while any test is failing or any required test is missing.

## Notes

- Phases 02–08 (including 04b) declare `append: 99-test-addendum.md` in their frontmatter, so `scripts/render.py` appends this automatically. Use `--no-append` to skip it.

## Changelog

- 1.0.0 — initial version
