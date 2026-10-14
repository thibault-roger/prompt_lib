---
title: Feature delivery
description: From idea to merged PR using the planner, the coding prompts and the Claude Code agents.
tags: [workflow, coding]
version: 1.0.0
---

# Feature delivery

A repeatable path for shipping a code change with Claude Code. Each step has a clear output that feeds the next one.

| # | Step | Tool | Output |
|---|------|------|--------|
| 1 | Scope the change | `agents/system-prompts/project-planner.md` (or `prompts/coding/refactor-plan.md` for restructuring) | Goal, in/out of scope, first task |
| 2 | Implement | Claude Code main session, plan mode first | Working change on a branch |
| 3 | Test | `test-writer` agent | New tests, passing suite |
| 4 | Review | `code-reviewer` agent | Ranked findings; fix blockers and majors |
| 5 | Document | `docs-writer` agent | README/docstrings in sync |
| 6 | Ship | `git commit`, open PR | PR ready for human review |

## Running it in Claude Code

Install the agents once:

```bash
./scripts/install_agents.sh
```

Then, in a session on the target repo:

```text
1. Plan:      "Enter plan mode. Goal: <goal>. Constraints: <constraints>."
2. Implement: approve the plan and let the session implement it.
3. Test:      "Use the test-writer agent on the current changes."
4. Review:    "Use the code-reviewer agent, then fix every blocker and major it reports."
5. Document:  "Use the docs-writer agent to update docs for this change."
```

Steps 3–5 are independent of each other once the implementation is stable, so they can be requested together; run review again if test-writer surfaced bugs that required code changes.

## When to skip steps

- One-line fixes: skip 1 and 5.
- Spikes and throwaway notebooks: stop after 2.
- Anything touching data correctness or auth: never skip 4.
