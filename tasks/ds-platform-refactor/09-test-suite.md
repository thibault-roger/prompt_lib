---
title: "DSP refactor — Phase 9: Full test and validation suite"
description: Implemented test pyramid (A–I) covering SDK, runner, shell, pipelines, assembler, migration parity, security, performance and post-deploy health.
tags: [task, ds-platform, testing]
variables: [VERSIONS, ARTIFACT_REPO, SCANNER, P99_TARGET, X]
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 9: TEST & VALIDATION SUITE. Build the complete verification suite for the new architecture. Organise it as a test pyramid, with one command per level and one command that runs everything. Each test needs an ID, a purpose and the expected result. Implement the tests; do not just describe them.

A. SDK & MANIFEST (unit + contract)
A1  Decorators return the original function object unchanged (identity check). The decorated function stays callable in plain Python.
A2  A duplicate endpoint or step name raises an error that names the duplicate.
A3  Type mapping table test: int, float, str, bool, list[T], tuple, set, dict[str,T], Optional[T], Union[A,B], nested TypedDict, total=False TypedDict, unknown class → {} plus a warning, missing annotations, default values (including None and mutable defaults).
A4  Pipeline wiring: data dependency through a parameter name, "after" ordering, unknown dependency → error, cycle → error that shows the path, self-dependency → error.
A5  Golden-file manifest for each sample project. The diff must be empty. Updating a golden file requires an explicit flag.
A6  Determinism: building the manifest twice gives byte-identical output (stable ordering).
A7  Import side effects: a module that prints, reads env vars or fails on import produces a clear error, not a partial manifest.
A8  The SDK and the runner import nothing outside the stdlib. Enforce this with a static check over the import statements and with a run in an empty venv.
A9  Python compatibility matrix: run A1–A8 under every Python version in use ({{VERSIONS}}, minimum 3.8) and the newest available.
A10 Backward-compatibility shim: every decorator and option from the old package still works. Deprecated options emit DeprecationWarning. A sample of real legacy DS projects builds a manifest unchanged.
A11 Contract versioning: the shell rejects an unsupported MAJOR, accepts a newer MINOR, and logs the version mismatch.

B. RUNNER (unit + integration, under the oldest AND newest Python)
B1  run-step: param coercion (int/float/bool variants/str/JSON), a missing required param gives a non-zero exit and a message, default values are applied, upstream artifacts are read, the output is written, parent dirs are created.
B2  run-step on an unknown pipeline or step: non-zero exit and an explicit message.
B3  serve: a valid call, an unknown endpoint (platform error), bad JSON, non-dict kwargs, wrong kwargs for the function (user error).
B4  A user exception returns kind=user with no traceback in the response, the traceback is in the logs, and the worker serves the next request.
B5  Persistent connection: 1,000 sequential requests on one connection.
B6  Concurrency: 200 concurrent connections with no resets. This is a regression test for the request_queue_size bug.
B7  Pre-fork: N processes all serve traffic (check distinct PIDs in a debug field or the logs). SIGTERM stops parent and children with no orphans left.
B8  Socket permissions are 660. A stale socket file is replaced on start.
B9  Allowlist: a qualname or endpoint not in the manifest cannot be invoked, even when it exists in the module.
B10 Large payload: a ~5 MB request/response round-trips correctly within the limits. An oversized line is rejected cleanly.

C. API SHELL (integration)
C1  Routes, methods and paths match the manifest. OpenAPI is generated and contains the request schemas.
C2  Validation: an extra field → 422, a wrong type → 422, a missing required field → 422, nested object validation, nullable handling, default values are applied. None of these reach the worker (assert the worker received zero calls).
C3  Error mapping: user error → 500 with a generic body, platform error → 502, worker down → 503, timeout → 504. Assert that no stack trace, file path or exception message from DS code appears in any response body or header.
C4  Pool: connections are reused (count the accepts on the worker side). A connection closed by the worker is discarded and the call is retried on a fresh one or fails cleanly. A timed-out connection is never reused.
C5  Backpressure: with max_inflight=K, at most K concurrent calls reach the worker. The excess waits, then completes or times out.
C6  Health: /healthz stays 200 while the worker is down, /readyz returns 503 while the worker is down and 200 once it recovers, with no shell restart.
C7  Loop rebinding: several test clients and app instances in the same process work. This is a regression test for the event-loop-bound semaphore and pool.
C8  Isolation: the shell's environment cannot import the DS package. The DS environment cannot import fastapi/uvicorn/starlette.
C9  Legacy: a worker on the oldest Python, behind a shell on the newest Python, passes C1–C6.
C10 In-process mode passes C1–C3.
C11 Middleware from the current platform (auth, logging, metrics, tracing, request IDs): unauthenticated → 401/403, metrics are exposed, the request ID is propagated to worker logs.

D. PIPELINES / ARGO
D1  Golden YAML per sample pipeline. Validate it against the Argo CRD schema (offline, from the schema file shipped in our mirror).
D2  DAG correctness: the dependencies equal depends_on, artifact "from" references point to existing tasks, there are no empty lists, and names are k8s-safe.
D3  Workflow parameters: union + defaults. Conflicting defaults → error.
D4  Local simulation: execute every step in topological order with the runner, passing the artifacts as files. Compare the final output with calling the DS functions directly in Python. The results must be identical.
D5  Security context on every template: non-root, read-only root fs, /tmp emptyDir, capabilities dropped.
D6  Feature mapping from Phase 1 (retries, timeouts, schedules/CronWorkflow, resources, GPUs, node selectors): one test per feature.
D7  On a test cluster (if available): submit, the workflow succeeds, the artifacts exist in {{ARTIFACT_REPO}}. A failure injected in step 2 means steps 3+ do not run, and retries behave as configured.

E. ASSEMBLER & KUBERNETES
E1  Dry-run rendering for KIND=api and KIND=pipeline. Every document parses and validates with kubeconform/kubectl --dry-run=server (if a cluster is available).
E2  Python policy: below MIN_PYTHON → exit 2; ALLOW_LEGACY=1 → succeeds, logs DEROGATION, forces sidecar, adds an expiry label.
E3  Manifest extraction runs with no network, a read-only fs and non-root. A DS module that tries network access at import fails extraction with a clear error.
E4  The overlay image adds exactly 2 files plus USER and CMD. The DS layers are untouched: compare layer digests before and after.
E5  The manifest sha annotation changes when the manifest changes and is stable otherwise.
E6  The rendered pod spec has: no ports on the worker, no SA token, hardened securityContext on both containers, NetworkPolicy present (DNS-only egress), HPA present.
E7  Template injection: names or descriptions containing quotes, newlines, "{{", "${" or YAML special characters either render safely or are rejected.
E8  On a test cluster: deploy, pods become Ready, a smoke call succeeds through the Service, NetworkPolicy blocks outbound traffic from the worker container (attempt a connection and expect failure).

F. MIGRATION & PARITY (old platform vs new)
F1  For each representative DS project: deploy with the OLD mechanism and the NEW one side by side. Replay the same recorded or generated requests against both. Responses must match (status + body, with documented tolerance for floats).
F2  OpenAPI diff old vs new. Any breaking change for API consumers is listed and either fixed or explicitly accepted.
F3  Pipeline parity: the same inputs give the same outputs on the old and new runs.
F4  The per-project switch flag works in both directions (rollback test).

G. SECURITY
G1  Dependency scan with {{SCANNER}}: the shell image has zero critical/high findings. DS images contain none of: fastapi, uvicorn, starlette, gunicorn, h11, argo/hera packages.
G2  CVE rollout drill: publish shell v+1 → the rollout job redeploys all APIs. No DS image is rebuilt (registry digests unchanged). The canary stops on an injected readiness failure.
G3  Fuzzing the shell: random and malformed JSON, deep nesting, huge strings, unicode, numeric edge cases (NaN, Infinity, huge ints). The shell never returns 5xx for invalid input (must be 4xx) and never crashes.
G4  Malicious-manifest tests: path traversal in module or qualname, dunder attribute access, names with shell or YAML metacharacters. All rejected.
G5  Slow-client / slowloris and many idle connections: the shell stays responsive within its configured timeouts.
G6  Secrets: none in manifests, ConfigMaps, logs or error bodies (grep the test outputs for the test secrets injected).

H. PERFORMANCE & RESILIENCE
H1  Open-loop load at 150 req/s for 10 min, light and heavy endpoints, in-process vs sidecar: p50, p95, p99, error rate. Pass criteria: p99 < {{P99_TARGET}}, errors = 0, sidecar overhead p50 < 1 ms.
H2  Saturation test: find max throughput per pod and per worker-process count. Record the curve.
H3  Soak: 2–4 h at nominal load. No memory growth beyond {{X}}%, no file descriptor or thread leak in the shell or the worker.
H4  Spike: 0 → 3× nominal in 10 s. The HPA scales out, the error rate stays within budget, and backpressure queues rather than failing.
H5  Chaos:
    - kill the worker process mid-traffic → the shell returns 503 and recovers when the worker restarts;
    - kill a pod → traffic shifts;
    - fill /tmp;
    - delay the socket → 504 at the timeout, no hung requests.
H6  Graceful shutdown: in-flight requests complete during rollout (zero 5xx during a rolling update under load).

I. POST-DEPLOY SMOKE & CONTINUOUS HEALTH (runs in CD and on a schedule)
I1  After every deploy: /readyz, one valid call per endpoint using an example payload from the manifest, one invalid call expecting 422, and OpenAPI reachable.
I2  Synthetic probes every N minutes per API, plus one canary pipeline run per day, with alerts on failure.
I3  Dashboards and alerts:
    - request rate, p99 and 5xx by API;
    - worker restarts;
    - pool saturation (in-flight vs max);
    - 503/504 counts;
    - pipeline success rate;
    - number and age of legacy derogations.
I4  A weekly report of shell versions deployed vs latest. Any API more than one version behind is flagged.

DELIVERABLES
- Test code organised by level, a fixtures directory, and sample DS projects: modern, legacy-Python, failing-on-purpose, malicious.
- Make/CI targets: test-unit, test-contract, test-integration, test-compat-matrix, test-e2e, test-security, test-perf, test-cluster, test-all.
- CI wiring: unit, contract and integration on every MR; compat matrix and security nightly; perf, soak and chaos weekly and before each shell release; cluster tests on the staging namespace.
- A traceability matrix: each requirement from Prompt 0 and each Phase 1 feature → the test IDs covering it. Every requirement must have at least one test.
- A final TEST REPORT in the format from the test addendum.

## Notes

- `X` is the maximum acceptable memory growth (in %) during the H3 soak test.
- If Phase 4b was run, paste its L1–L11 tests too and ask for them to be included in the suite and the traceability matrix.
- The "TEST REPORT format from the test addendum" means pasting `99-test-addendum.md` too if this is a fresh session: render with `--append 99-test-addendum.md`.

## Changelog

- 1.0.0 — initial version
