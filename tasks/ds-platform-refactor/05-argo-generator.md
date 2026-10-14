---
title: "DSP refactor — Phase 5: Argo pipeline generator"
description: Deploy-time generation of a hardened Argo WorkflowTemplate from the manifest.
tags: [task, ds-platform, argo, pipelines]
variables: [ARGO_VERSION, ARTIFACT_REPO]
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 5: ARGO GENERATOR (platform side, runs at deploy time).

Input: the manifest, a pipeline name, and the assembled image reference. Output: an Argo WorkflowTemplate YAML that works with Argo {{ARGO_VERSION}}.

Requirements
- Workflow parameters are the union of all source="pipeline_param" params across steps. Fail if the same name has conflicting defaults.
- One DAG task per step, with "dependencies" taken from depends_on. Convert names to k8s-safe form (lowercase, "_" → "-").
- One container template per step:
  - command: python /opt/dsp/dsp_runner.py run-step ...
  - pass params as --param name={{inputs.parameters.name}}
  - data inputs as artifacts at /tmp/inputs/<step>.json
  - output artifact "result" at /tmp/outputs/result.json
  Emit no empty lists.
- Hardened securityContext:
  - runAsNonRoot, uid 10001, no privilege escalation, drop ALL capabilities, seccomp RuntimeDefault;
  - readOnlyRootFilesystem, plus an emptyDir mounted at /tmp.
- Map resources from the manifest to requests/limits. Use a dedicated serviceAccountName.
- Large data: document and support passing references (object-store URIs) instead of values, using the existing artifact repository {{ARTIFACT_REPO}}.
- Map existing platform features from Phase 1 (retries, schedules → CronWorkflow, timeouts, node selectors, GPUs) to manifest fields, then to Argo fields.

Tests
- A golden-file YAML for the sample pipeline. Check DAG dependencies and artifact wiring.
- A local simulation: execute the steps in topological order with the runner, passing the artifacts as files.
- Optional, if a cluster is available: argo lint, then a submit to a test namespace.

## Notes

- `{{inputs.parameters.name}}` is Argo template syntax and is left untouched by `render.py`.
- If Phase 4b is done, also wire the workflow/pod env vars for request_id and the dsp.platform/* labels.

## Changelog

- 1.0.0 — initial version
