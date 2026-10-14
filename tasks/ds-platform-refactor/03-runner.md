---
title: "DSP refactor — Phase 3: Runner (worker + step executor)"
description: Single-file stdlib runner with run-step mode for Argo and a pre-forked Unix-socket serve mode.
tags: [task, ds-platform, runner]
variables: []
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 3: RUNNER (single file, stdlib only, Python >= 3.8).

This file is injected by the platform into DS images, including legacy ones. It must work with nothing installed.

Mode "run-step"
- Arguments: --manifest --pipeline --step --inputs-dir --output --param k=v (repeatable).
- Inputs from upstream steps are read from <inputs-dir>/<step_name>.json.
- Pipeline params arrive as strings. Coerce them using the manifest schema: integer, number, boolean, string; anything else is JSON-decoded.
- Write the JSON result to --output. A missing required parameter means a clear error and a non-zero exit code.

Mode "serve"
- Unix socket server. Protocol: one JSON object per line, in both directions.
  - Request: {"endpoint": "...", "kwargs": {...}}
  - Response: {"ok": true, "result": ...} or {"ok": false, "kind": "user"|"platform", "error": "..."}
- Allowlist: only endpoints declared in the manifest are callable. An unknown endpoint, bad JSON, or non-dict kwargs is a platform error.
- An exception in DS code is a "user" error. Log the traceback server-side and send only "<ExceptionType>: <message>". The worker must keep running.
- Persistent connections: loop over lines on one connection; do not close after each request.
- Threaded server (ThreadingMixIn, daemon threads).
- IMPORTANT, learned in benchmarks: set request_queue_size = 1024. The socketserver default of 5 causes connection resets under load.
- Pre-fork: --processes N (default from env DSP_WORKER_PROCESSES, default 1).
  - Bind the socket, import DS code, THEN fork N-1 children that all accept on the same socket. This shares the loaded model copy-on-write and gets around the GIL for CPU-bound code.
  - The parent forwards SIGTERM/SIGINT to the children.
- chmod 660 on the socket.

Tests
- run-step on a 3-step sample pipeline (data passing + param coercion).
- serve: a valid call, an unknown endpoint, a user exception (the worker survives), and concurrent calls with N=2 processes.
- Run all tests under the oldest supported Python version.

## Notes

- Paste the Phase 2 manifest schema and a sample manifest before this prompt.

## Changelog

- 1.0.0 — initial version
