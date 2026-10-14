# Task: DS platform refactor — "declare in DS code, expose at deploy time"

An ordered, multi-session prompt sequence for decoupling data-science code from its exposure stack (FastAPI/uvicorn, Argo). DS code only declares endpoints and steps. The platform injects a stdlib runner and a separately patched API shell at deploy time, so a CVE fix means rebuilding one shell image instead of every DS project.

## Run order

| # | File | Session | Test addendum | Output to keep |
|---|------|---------|---------------|----------------|
| 0 | [00-shared-context](00-shared-context.md) | First message of **every** session | — | — |
| 1 | [01-discovery](01-discovery.md) | 1 | — | Inventory, feature mapping, migration plan |
| 2 | [02-sdk-manifest](02-sdk-manifest.md) | 2 | auto | SDK, shim, manifest builder, golden manifest |
| 3 | [03-runner](03-runner.md) | 3 | auto | `dsp_runner.py` |
| 4 | [04-api-shell](04-api-shell.md) | 4 | auto | Shell app, Dockerfile, pinned requirements |
| 4b | [04b-logging](04b-logging.md) | 4 or 5 | auto | Correlation, JSON logs, tenancy, deployment record |
| 5 | [05-argo-generator](05-argo-generator.md) | 6 | auto | WorkflowTemplate generator, golden YAML |
| 6 | [06-assembler-k8s](06-assembler-k8s.md) | 7 | auto | Assembler, rendered K8s, CVE rollout job |
| 7 | [07-performance](07-performance.md) | 8 | auto | Load generator, results table, sizing guide |
| 8 | [08-security-review](08-security-review.md) | **fresh** | auto | Findings + remediation list |
| 9 | [09-test-suite](09-test-suite.md) | 9 | — (has its own) | Full suite A–I (+ L from 4b), CI targets, traceability matrix |
| 10 | [10-release-gate](10-release-gate.md) | **fresh**, once per project | — | GO / NO-GO |
| — | [99-test-addendum](99-test-addendum.md) | Appended to phases 2–8 | — | — |

Session boundaries are suggestions: one phase per session keeps context focused. Paste the previous phase's key outputs (interfaces, manifest sample, protocol) after Prompt 0 when a phase depends on them.

## Setup

Fill the platform variables once:

```bash
cp tasks/ds-platform-refactor/vars.example tasks/ds-platform-refactor/vars.local
$EDITOR tasks/ds-platform-refactor/vars.local      # git-ignored
```

## Rendering each step

```bash
T=tasks/ds-platform-refactor
V=$T/vars.local

# Session start
python3 scripts/render.py $T/00-shared-context.md --vars-file $V | pbcopy

# A phase (the test addendum is appended automatically for 02–08)
python3 scripts/render.py $T/03-runner.md --vars-file $V | pbcopy

# Release gate for one project
python3 scripts/render.py $T/10-release-gate.md --vars-file $V --var PROJECT=churn-api | pbcopy
```

`render.py` only substitutes declared `{{UPPER_CASE}}` variables. Argo expressions such as `{{inputs.parameters.name}}` and `{{workflow.name}}` are left as written.

## Using it with Claude Code

Each phase is a code-producing session. In Claude Code, run it inside the platform repo: send Prompt 0, then the phase prompt, and let it write files and run tests directly instead of pasting code. The `code-reviewer` and `test-writer` agents from `agents/claude-code/` fit naturally after each phase. Keep Phase 8 in a separate session, or give it to a different reviewer, so the review stays independent.
