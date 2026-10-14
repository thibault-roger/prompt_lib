---
title: "DSP refactor — Phase 6: Assembler and Kubernetes deployment"
description: Deploy-time composition of DS image + runner overlay, hardened K8s/Argo rendering, and the automated CVE rollout flow.
tags: [task, ds-platform, kubernetes, ci]
variables: [CI, BUILD_TOOL, SCANNER]
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 6: ASSEMBLER + K8S (deploy-time composition).

Write an assembler script for our CI ({{CI}}) using {{BUILD_TOOL}}. Inputs: KIND=api|pipeline, APP, DS_IMAGE, MODULES, SHELL_IMAGE (api), PIPELINE (pipeline). Options: PUSH, MANIFEST (skips extraction, for tests), MIN_PYTHON (default 3.10), ALLOW_LEGACY.

Steps
1. Extract the manifest by running the DS image with no network, a read-only root filesystem and a non-root user:
   python -m <sdk>.manifest $MODULES
2. Read the DS image's Python version.
   - Below MIN_PYTHON: fail with exit code 2.
   - If ALLOW_LEGACY=1: continue, log a visible DEROGATION, force sidecar mode, and record an expiry date label.
3. Build the overlay: FROM DS_IMAGE, COPY the runner and manifest to /opt/dsp/, USER 10001. The default CMD is the worker serve command. The DS image itself is never rebuilt.
4. Render:
   - API: a ConfigMap (the manifest) and a Deployment with two containers sharing an in-memory emptyDir at /run/dsp.
     - "worker": the overlay image, NO ports. Readiness = a Python one-liner connecting to the socket; DS images may not have "test". Env DSP_WORKER_PROCESSES.
     - "shell": SHELL_IMAGE on port 8080, readiness /readyz, liveness /healthz.
     - Both containers hardened: non-root, readOnlyRootFilesystem, drop ALL, automountServiceAccountToken false.
     - Pod annotation with the manifest sha256, so that manifest changes trigger a rollout. A label with the shell version.
     - Service; a NetworkPolicy allowing DNS egress only; an HPA on CPU at 60%.
   - Pipeline: call the Argo generator.
5. Validate every rendered YAML (parse it, plus kubeconform or kubectl --dry-run if available).

CVE flow (design and implement)
- The shell image is versioned independently and scanned with {{SCANNER}}.
- When a new shell version is published, a job lists all deployed APIs by label, re-renders them with the new SHELL_IMAGE, and rolls them out progressively (canary → all). It stops automatically on readiness or error-rate regressions. No DS involvement.
- Report legacy (ALLOW_LEGACY) deployments and their expiry dates.

Tests
- Dry-run rendering for both kinds; the legacy refusal and the derogation; YAML validity.
- List anything you could not run (builds, cluster apply).

## Notes

- If Phase 4b is done, the assembler also sets the dsp.platform/* labels and emits the deployment record.

## Changelog

- 1.0.0 — initial version
