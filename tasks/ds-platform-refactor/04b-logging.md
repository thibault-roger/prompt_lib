---
title: "DSP refactor — Phase 4b: Logging and log access for DS users"
description: Request correlation, one structured log format across shell/worker/steps, per-team log access and deployment records.
tags: [task, ds-platform, logging, observability]
variables: [LOG_BACKEND, ARTIFACT_REPO, RETENTION]
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 4b: LOGGING & LOG ACCESS FOR DS USERS.

Goal: a DS user can see, for their own applications only, both their application logs and the logs of all the platform wrapping code that served them: the API shell, the runner/worker, and Argo steps. They can follow one request or one pipeline run across all components.

Implement
1. Correlation
   - The shell accepts an incoming X-Request-ID (validated: max 128 chars, [A-Za-z0-9._-]) or generates a UUID4, and returns it in the response headers, including on 4xx/5xx.
   - Extend the socket protocol: {"request_id": "...", "endpoint": "...", "kwargs": {...}}. Bump the contract MINOR version. The runner must accept requests without request_id (backward compatibility).
   - The runner stores request_id in a contextvars.ContextVar (Python >= 3.8 compatible, thread-safe with the threaded server and pre-fork). A logging.Filter injects it into every record emitted during that call, including DS logs.
   - Pipelines: request_id = Argo workflow name + node ID, passed as env vars ({{workflow.name}}, {{pod.name}}) in the generated templates.
2. Structured logs
   - One JSON-lines format for the shell, runner and step pods. Fields: ts (UTC ISO8601), level, component (shell|worker|runner|argo-step), app, app_version, shell_version, team, request_id, endpoint | pipeline/step/workflow, logger, message, exc (the full traceback as ONE field).
   - The runner installs the handler on the root logger at startup. This is stdlib only, inside dsp_runner.py. It must not break DS code that configures its own logging: document the precedence and test it.
   - DSP_LOG_LEVEL is configurable per app through the deployment, with no rebuild.
3. Wrapper log content
   - shell: one access-log line per request (method, path, status, duration_ms, request_id, worker_latency_ms).
   - 422: log the field paths and error types only, never the values.
   - 503/504: worker or socket state and timeout value. 500: "see worker logs" plus request_id.
   - worker: one line per call (endpoint, duration_ms, outcome). On a user exception: the full traceback in exc. Never log kwargs by default. Offer an opt-in DSP_LOG_PAYLOADS=1 for non-production use only, with redaction of the keys listed in the manifest.
4. Access control & retention
   - The assembler adds labels to pods and Argo workflows: dsp.platform/app, dsp.platform/team, dsp.platform/component.
   - Configure {{LOG_BACKEND}} so that users only query logs whose team label matches their group, covering both DS and wrapper components. Platform admins see everything.
   - Argo: archiveLogs=true to {{ARTIFACT_REPO}}. Argo server RBAC / SSO scoped per team namespace.
   - Retention: {{RETENTION}}. Logs must never contain secrets, tokens or env dumps.
5. Deployment record
   - The assembler emits one JSON event per deployment: app, team, DS image digest, overlay digest, shell image + digest, manifest sha, contract version, Python version, legacy derogation + expiry, timestamp, CI job URL.
   - Store it where users can query it next to their logs.
6. User documentation: a one-page guide "How to find my logs" with example queries: by request_id, by endpoint errors in the last hour, by pipeline run.

Tests (add to the suite with these IDs)
L1  The X-Request-ID is returned on 200/422/500/503/504. An incoming valid ID is preserved; an invalid one is replaced.
L2  One request produces shell + worker + DS log lines, all carrying the same request_id. 50 concurrent requests across 2 worker processes never mix IDs.
L3  An old runner without request_id support still works with a new shell, and the reverse (protocol compatibility).
L4  Every log line from every component parses as JSON and has all mandatory fields. A traceback is a single event.
L5  DS code calling logging.basicConfig or adding its own handlers: its logs are still emitted and still carry request_id, or the documented behaviour is asserted.
L6  No request values in logs on 422. No kwargs in logs by default. Redaction works when payload logging is enabled. Grep for injected test secrets finds nothing.
L7  Pipeline steps log the workflow name and node. Logs are retrievable from the archive after pod deletion.
L8  Tenancy: user from team A can query team A logs (DS + shell + runner) and gets zero results for team B. Verify on the staging log backend.
L9  The deployment record exists for each deploy and matches the running digests.
L10 Changing DSP_LOG_LEVEL changes verbosity after a rollout, with no image rebuild.
L11 Overhead: logging adds less than 0.5 ms p50 at 150 req/s (rerun H1 with logging enabled).

## Notes

**Why this phase exists.** The base architecture is already compatible with "DS users see their app logs plus all wrapper logs": everything goes to stdout and is collected, API pods hold worker + shell containers, and Argo step pods carry runner and DS logs together. What was missing:

- **Correlation** — nothing tied a shell-side 500 to the DS traceback in the worker. Fix: X-Request-ID generated/propagated by the shell, carried in the socket protocol, stored in a contextvar and injected into every DS log line by a logging filter. One ID search shows shell, runner and DS lines together.
- **One structured format** across components (app, versions, component, request_id, endpoint/pipeline, level, UTC ts). Tracebacks as a single event so the collector doesn't split them. Raw `print()` is still captured, just untagged.
- **Useful wrapper logs** — why a request was rejected or failed, without logging bodies (PII).
- **Per-team access** — team/owner labels set by the assembler, tenancy enforced by the log backend (Loki tenants, OpenSearch document-level security, or namespace RBAC on pods/log and the Argo UI).
- **Pipelines** — Argo `archiveLogs` so step logs survive pod garbage collection.
- **Deployment traceability** — a deployment record shows which wrapper version served a given log line.
- **Log level** — `DSP_LOG_LEVEL` per app, changeable without a rebuild.

Run after Phase 4 (it extends the shell and the runner protocol). `{{workflow.name}}` and `{{pod.name}}` are Argo template syntax and are left untouched by `render.py`. The L1–L11 tests must also be included when running Phase 9.

## Changelog

- 1.0.0 — initial version
