---
title: "DSP refactor — Phase 2: SDK and manifest"
description: Declarative stdlib-only SDK, manifest builder with JSON Schema mapping and pipeline wiring, and a backward-compatible shim.
tags: [task, ds-platform, sdk]
variables: [CURRENT_PACKAGE_NAME]
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 2: SDK + MANIFEST.

Implement the new declarative SDK and a backward-compatible shim for {{CURRENT_PACKAGE_NAME}}.

Requirements
- Decorators (keep the existing public names/options from Phase 1; at minimum):
  - endpoint(path=None, method="POST", name=None)
  - step(pipeline, name=None, after=(), resources=None)
  They store a spec in a module-level registry and return the original function unchanged. A duplicate name raises a clear error.
- Manifest builder, runnable as: python -m <sdk>.manifest <module> [<module>...] > manifest.json
  It imports the modules, introspects signatures with typing.get_type_hints and inspect, and emits:
  {
    contract_version, modules,
    endpoints: [{ name, path, method, description, callable: {module, qualname},
                  params: [{ name, schema, required, default? }], returns }],
    pipelines: [{ name,
                  steps: [{ name, description, callable, params, returns,
                            after, resources, depends_on }] }]
  }
- Type → JSON Schema mapping:
  - int / float / str / bool;
  - list / tuple / set[T];
  - dict[str, T];
  - Optional / Union (use "nullable" and "anyOf");
  - TypedDict (properties + required).
  Unknown types map to {} (any) with a warning, never a crash.
- Pipeline wiring convention: a parameter named after another step of the same pipeline receives that step's output. Mark it source="step" and add it to depends_on. Other parameters are source="pipeline_param". "after" adds ordering without data.
  Validate that dependencies exist and detect cycles, reporting the cycle path.
- Python >= 3.8 compatible. Standard library only.
- Shim: the old package re-exports the new decorators, maps old option names to new ones, and emits DeprecationWarning for options that are no longer supported.

Tests
- Unit tests for the type mapping, wiring, cycle detection and duplicate detection.
- Run the manifest builder on the representative projects from Phase 1, under the oldest and the newest Python version.
- A golden-file test for the manifest of one sample project.

Deliver: file tree, full code, tests, and a short CHANGELOG entry for DS users.

## Notes

- Paste the Phase 1 inventory (decorators and options) before this prompt.
- The test addendum is appended automatically by `scripts/render.py`.

## Changelog

- 1.0.0 — initial version
