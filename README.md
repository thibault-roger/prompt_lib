# prompt_lib

A personal, version-controlled library of **working prompts** for recurring tasks and **agent definitions** that streamline day-to-day work.

Everything here is plain Markdown with YAML frontmatter: readable on GitHub, easy to copy-paste, and machine-checkable.

## Layout

```
prompt_lib/
  prompts/                 # Single-shot task prompts, grouped by domain
    coding/                #   review, debugging, tests, refactoring
    data/                  #   SQL, data-quality audits, Polars optimization
    writing/               #   summaries, technical explainers
    analysis/              #   decision memos, comparisons
  agents/
    claude-code/           # Claude Code subagents (drop-in for ~/.claude/agents)
    system-prompts/        # Model-agnostic system prompts for any chat/API agent
  workflows/               # Generic recipes that chain library prompts + agents
  tasks/                   # Project-specific, ordered multi-session prompt sequences
    ds-platform-refactor/  #   00-…10 phase prompts, test addendum, vars.example
  templates/               # Starting points for new prompts and agents
  scripts/
    promptlib.py           # Shared frontmatter / section parsing
    validate.py            # Lints frontmatter, sections and declared variables
    render.py              # Fills {{variables}} (inline, @file or --vars-file), appends addenda
    install_agents.sh      # Symlinks Claude Code agents into a .claude/agents dir
```

## Prompts vs. agents vs. workflows vs. tasks

| Kind | What it is | When to use it |
|------|-----------|----------------|
| **Prompt** | One message with `{{variables}}` that solves one task | You know the task and want a reliable, repeatable result in a single turn |
| **Agent** | A persistent role: system prompt + tools + operating rules | The task needs multiple steps, tool use, or judgement across a session |
| **Workflow** | An ordered recipe combining prompts and agents | A recurring process (e.g. "ship a feature", "onboard a dataset") |
| **Task** | A numbered sequence of purpose-written prompts sharing one context and one vars file | A large one-off project run phase by phase across sessions (e.g. a platform refactor) |

## Quick start

```bash
# List and validate everything
python3 scripts/validate.py

# Render a prompt with variables (values can be literal or @path/to/file)
python3 scripts/render.py prompts/coding/code-review.md \
  --var language=python --var diff=@my_change.diff

# Copy straight to the clipboard (macOS)
python3 scripts/render.py prompts/writing/summarize-document.md \
  --var audience="engineering managers" --var document=@notes.md | pbcopy

# Install Claude Code agents globally (symlinks, so edits here stay live)
./scripts/install_agents.sh            # -> ~/.claude/agents
./scripts/install_agents.sh ./.claude/agents   # -> a project-local dir
```

Requires Python 3.9+ and no third-party packages.

## File format

Every prompt starts from [`templates/prompt.md`](templates/prompt.md):

```markdown
---
title: Code review
description: One line, shown in listings.
tags: [coding, review]
variables: [language, diff]
version: 1.0.0
tested_with: [claude-opus-5-5]
---

## Prompt
...the text sent to the model, with {{language}} and {{diff}} placeholders...

## Notes
Why it works, known failure modes, tuning tips.
```

Optional frontmatter: `append: other-file.md` makes `render.py` append that file's prompt (used for mandatory addenda). Only identifier-style placeholders (`{{name}}`, `{{UPPER_NAME}}`) are variables; dotted ones like Argo's `{{workflow.name}}` are kept literally.

Agents for Claude Code follow the native subagent format (`name`, `description`, `tools`, `model`) — see [`templates/claude-code-agent.md`](templates/claude-code-agent.md). Model-agnostic system prompts use [`templates/system-prompt.md`](templates/system-prompt.md).

## Contributing a prompt

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: a prompt earns a place here only after it has produced good output on real work at least twice. Bump `version` when you change behavior, and note why in `## Changelog`.

## Catalog

### Prompts

| Prompt | Purpose |
|--------|---------|
| [coding/code-review](prompts/coding/code-review.md) | Severity-ranked review of a diff, bugs before style |
| [coding/debug-root-cause](prompts/coding/debug-root-cause.md) | Hypothesis-driven root-cause analysis from an error and context |
| [coding/write-tests](prompts/coding/write-tests.md) | Behavior-focused tests with edge cases, matching project style |
| [coding/refactor-plan](prompts/coding/refactor-plan.md) | Safe, incremental refactor plan with checkpoints |
| [data/sql-from-question](prompts/data/sql-from-question.md) | Business question → validated SQL with stated assumptions |
| [data/data-quality-audit](prompts/data/data-quality-audit.md) | Profile a dataset sample and list concrete quality issues |
| [data/polars-optimize](prompts/data/polars-optimize.md) | Rewrite pandas/eager code as idiomatic lazy Polars |
| [writing/summarize-document](prompts/writing/summarize-document.md) | Audience-aware summary with decisions and open questions |
| [writing/technical-explainer](prompts/writing/technical-explainer.md) | Explain a technical concept at a chosen depth |
| [analysis/decision-memo](prompts/analysis/decision-memo.md) | Options, trade-offs and a recommendation in one page |

### Agents

| Agent | Kind | Purpose |
|-------|------|---------|
| [code-reviewer](agents/claude-code/code-reviewer.md) | Claude Code | Reviews the current diff; read-only |
| [test-writer](agents/claude-code/test-writer.md) | Claude Code | Writes and runs tests for changed code |
| [data-engineer](agents/claude-code/data-engineer.md) | Claude Code | Builds and optimizes Polars/SQL pipelines |
| [docs-writer](agents/claude-code/docs-writer.md) | Claude Code | Keeps README and docstrings in sync with code |
| [research-analyst](agents/system-prompts/research-analyst.md) | System prompt | Source-backed research with explicit confidence |
| [project-planner](agents/system-prompts/project-planner.md) | System prompt | Turns a vague goal into a scoped, sequenced plan |

### Workflows

| Workflow | Steps |
|----------|-------|
| [feature-delivery](workflows/feature-delivery.md) | plan → implement → test-writer → code-reviewer → docs-writer |
| [dataset-onboarding](workflows/dataset-onboarding.md) | data-quality-audit → data-engineer → sql-from-question |

### Tasks

| Task | Phases |
|------|--------|
| [ds-platform-refactor](tasks/ds-platform-refactor/README.md) | Decouple DS code from its exposure stack: shared context → discovery → SDK/manifest → runner → API shell → logging → Argo generator → assembler/K8s → performance → security review → test suite → per-project release gate |
