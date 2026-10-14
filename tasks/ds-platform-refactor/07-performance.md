---
title: "DSP refactor — Phase 7: Performance validation"
description: Open-loop load testing of in-process vs sidecar modes, sizing guide, and a cost-ordered list of fixes.
tags: [task, ds-platform, performance]
variables: [P99_TARGET]
append: 99-test-addendum.md
version: 1.0.0
tested_with: []
---

## Prompt

PHASE 7: PERFORMANCE. Target: APIs at 100–150 req/s sustained, p99 below {{P99_TARGET}}.

1. Write an OPEN-LOOP load generator: requests fire on a fixed schedule at RATE req/s for DUR seconds, whatever the responses. Report p50, p95, p99 and the error count. Closed-loop saturation tests hide real latency at the target rate, so do not rely on them alone.
2. Write a benchmark module with two endpoints:
   - "light": ~0 ms of work, to measure plumbing overhead;
   - "heavy": ~5 ms of pure-Python CPU that holds the GIL, to simulate a small model.
3. Compare in-process mode against sidecar mode with 1, 2 and N worker processes, at 150 req/s and at saturation.
   Reference result from a prototype on 2 shared vCPU, at 150 req/s:
   - light: p50 2.3 ms both modes;
   - heavy: p50 ~8 ms, p99 13 ms in-process vs 19 ms sidecar;
   - zero errors.
   Treat a sidecar overhead above ~1 ms p50 as a bug to investigate.
4. Produce a sizing guide: cores ≈ TPS × CPU-seconds per request ÷ 0.6. Set worker processes ≈ cores per pod, then scale replicas with the HPA.
5. If profiling shows a bottleneck, propose fixes in order of cost:
   - more worker processes or replicas;
   - msgpack or Arrow instead of JSON for large payloads;
   - dynamic batching for vectorised or GPU models;
   - adopting an existing model server that uses the same process separation and consumes our manifest (only from what is in our internal mirror).

Deliver: scripts, a results table, and the sizing guide.

## Notes

- Run the load generator on a different host or pod than the system under test where possible, so client CPU does not distort latency.

## Changelog

- 1.0.0 — initial version
