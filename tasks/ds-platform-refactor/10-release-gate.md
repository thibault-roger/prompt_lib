---
title: "DSP refactor — Prompt 10: Release gate"
description: Evidence-based GO / NO-GO for switching one project to the new mechanism. Run once per project.
tags: [task, ds-platform, release]
variables: [PROJECT, N]
version: 1.0.0
tested_with: []
---

## Prompt

RELEASE GATE. Using the outputs of the test suite I paste (reports, logs, metrics), decide GO / NO-GO for migrating project {{PROJECT}} to the new architecture.

Check each item and quote the evidence (test ID + result). Missing evidence counts as a fail.
1. A1–A11, B1–B10 and C1–C11 pass under the project's Python version.
2. Parity F1–F3 pass for this project, or the differences are documented and accepted.
3. G1 is clean for the shell version being deployed. G3 and G4 pass.
4. H1 passes at this project's expected load, plus 50% headroom. H6 passes.
5. E1, E6 and E8 pass in staging. I1 smoke passes in staging.
6. A rollback (F4) was tested within the last {{N}} days.
7. If the project uses ALLOW_LEGACY: the expiry date is set, an owner is named, and the migration ticket exists.

Output: GO / NO-GO, the blocking items, the non-blocking risks, and the exact rollback command.

## Notes

- `N` is the maximum age, in days, of the last successful rollback test. `PROJECT` is usually passed on the command line, since it changes per run: `--var PROJECT=my-api`.
- Run this in a fresh session (Prompt 0 first) so the decision rests only on the pasted evidence.

## Changelog

- 1.0.0 — initial version
