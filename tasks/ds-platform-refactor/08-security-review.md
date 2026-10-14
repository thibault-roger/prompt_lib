---
title: "DSP refactor — Phase 8: Security review"
description: Independent security review of SDK, runner, shell, generators, assembler and rendered YAML, with a prioritised remediation list.
tags: [task, ds-platform, security, review]
variables: []
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 8: SECURITY REVIEW. Act as an independent reviewer who did not write this code. I will paste the SDK, runner, shell, generators, assembler and rendered YAML.

Check and report findings by severity, each with a file/line reference and a concrete fix.
- Can any network input reach DS code without validation? Can the worker call anything outside the manifest allowlist (attribute traversal through qualname, import side effects)?
- Is the manifest trusted? It is produced by running DS code. What can a malicious DS project inject into it, and how does the shell or the assembler defend against that (paths, names, schema size, YAML injection in rendered templates)?
- Extraction sandbox: network, filesystem, user, resource limits, timeouts.
- Error handling: any stack traces or internal details leaking to clients? Timeouts everywhere? Behaviour under slow or malicious clients?
- Container and pod hardening: run as root anywhere? Writable filesystems? Service account tokens? Egress? Capabilities?
- Supply chain: pinned and hashed shell dependencies, base image provenance, scanning gate, SBOM.
- Legacy Python: what risk remains in the worker, and is it confined and time-boxed?
- Residual risks that the architecture does NOT remove, stated plainly.

End with a prioritised remediation list.

## Notes

- Run last among the build phases, **in a fresh session** (Prompt 0 first), so the reviewer has not seen the reasoning that produced the code.
- Include the Phase 4b logging code: log injection and secret leakage are in scope.

## Changelog

- 1.0.0 — initial version
