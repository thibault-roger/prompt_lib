---
title: "DSP refactor — Phase 4: API shell"
description: Platform-owned FastAPI image that builds routes and Pydantic validation from the manifest and relays to the worker.
tags: [task, ds-platform, api]
variables: []
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 4: API SHELL (platform-owned image: FastAPI + uvicorn, latest patched versions).

Build the app from the manifest at startup. Factory: create_app(). Configuration through env vars:
DSP_MANIFEST, DSP_MODE=sidecar|inprocess, DSP_SOCKET, DSP_TIMEOUT_S, DSP_MAX_INFLIGHT, DSP_APP_NAME, DSP_APP_VERSION.

Requirements
- Refuse to start if the manifest contract MAJOR differs from the one the shell supports.
- For each endpoint, build a Pydantic request model from the param schemas, recursively for nested objects, using ConfigDict(extra="forbid"). Unexpected or mistyped fields must get a 422 BEFORE reaching DS code.
- Build the response_model from "returns" when the schema is specific. Generate the OpenAPI docs from the manifest.
- Register routes dynamically. Set the handler's __signature__ so FastAPI sees the body model.
- Sidecar invoker:
  - Pool of persistent Unix-socket connections. Reuse idle ones; discard closed ones.
  - asyncio.Semaphore(max_inflight) for backpressure.
  - Timeout → 504, and do NOT return that connection to the pool.
  - Worker unreachable or connection lost → 503.
  - Worker "user" error → 500 with a generic message. Worker "platform" error → 502. Never leak stack traces.
  - IMPORTANT: the semaphore and the pool are bound to an event loop. Re-create them when the running loop changes (test clients, reloads).
- In-process invoker (optional mode): import the callables and run them in a threadpool. Same error mapping.
- /healthz (liveness) and /readyz (the worker is reachable). Exclude both from the schema.
- Integration points to keep from the current platform (from Phase 1): auth, request logging, metrics, tracing. Implement them as shell middleware, never in DS code.
- Pinned requirements with hashes. A multi-stage Dockerfile with non-root user 10001, no server header, and proxy headers enabled.

Tests
- Sidecar mode with the worker in a SEPARATE interpreter/venv that does not have FastAPI. Also assert that the shell cannot import the DS package.
- 422 on an extra field and on a wrong type; 503 when the worker is stopped; 500 without a stack trace on a user exception.
- A legacy-Python worker (e.g. 3.8) behind a shell running the newest Python.

## Notes

- Paste the runner (Phase 3) protocol section and the Phase 1 middleware inventory before this prompt.

## Changelog

- 1.0.0 — initial version
