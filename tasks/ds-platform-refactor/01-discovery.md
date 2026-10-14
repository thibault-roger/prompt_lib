---
title: "DSP refactor — Phase 1: Discovery and gap analysis"
description: Inventory current decorators and couplings, map each feature to the target architecture, and plan the migration. No code.
tags: [task, ds-platform, discovery]
variables: [CURRENT_PACKAGE_NAME]
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 1: DISCOVERY. Do not write implementation code in this phase.

I will paste:
(a) the source of {{CURRENT_PACKAGE_NAME}} (decorators + any wrapping logic);
(b) the CI/CD templates that package DS code;
(c) 2–3 representative DS projects, including the oldest Python version one.

Produce:
1. An inventory of every decorator and option, and what each one currently generates (routes, request/response models, auth, middleware, pipeline steps, parameters, resources, schedules, retries).
2. For each feature, where it must live in the target architecture: SDK metadata, manifest field, shell, runner, Argo generator, or assembler. Flag any feature that requires DS code to import the exposure stack: those are migration blockers. Propose how to remove each one.
3. Hidden couplings: DS code that imports fastapi/starlette/argo/hera directly, uses Request objects, or relies on app startup hooks or global state initialised by the wrapper.
4. The data passed between pipeline steps today: size, format, and whether it goes by value or by reference (S3 paths).
5. A migration plan in ordered, independently shippable steps, each with a rollback strategy. Old and new mechanisms must coexist during migration, selectable per project with a flag.
6. Open questions for me, as a numbered list.

Output as structured markdown. Be explicit about assumptions.

## Notes

- Save the output (e.g. `phase1-discovery.md` in the platform repo). Later phases refer to "from Phase 1": paste the relevant parts back in.

## Changelog

- 1.0.0 — initial version
