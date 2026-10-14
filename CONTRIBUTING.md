# Contributing

## Admission rule

A prompt or agent goes in only after it has produced output you would actually use, on real work, at least twice. Untested ideas belong in a branch or an issue, not on `main`.

## Adding a prompt

1. Copy `templates/prompt.md` into the right `prompts/<domain>/` folder. Use a kebab-case filename that names the task (`write-tests.md`, not `tests-prompt-v2.md`).
2. Fill in the frontmatter. `variables` must list every `{{placeholder}}` used in `## Prompt` — `validate.py` checks this both ways.
3. Write the prompt. Guidelines that consistently pay off:
   - **State the goal and the reader** before the instructions. The model calibrates depth and tone from who the output is for.
   - **Say what good output looks like**: structure, length, what to leave out.
   - **Explain the why behind constraints.** "Rank bugs above style because reviewers skim" generalizes better than "ALWAYS rank bugs first".
   - **Wrap inputs in XML-style tags** (`<diff>…</diff>`) so instructions and data never blur.
   - **Give the model an exit.** Tell it what to do when the input is insufficient (ask, or state assumptions) instead of guessing silently.
4. Add `## Notes` covering when to use it, when not to, and known failure modes.
5. Run `python3 scripts/validate.py` and add a row to the catalog in `README.md`.

## Adding an agent

- **Claude Code subagent** → `agents/claude-code/`, from `templates/claude-code-agent.md`. The `description` field is what Claude reads to decide when to delegate, so write it as a trigger ("Use after code changes to…"), not a job title. Grant the narrowest `tools` list that works; a reviewer does not need `Edit`.
- **Model-agnostic system prompt** → `agents/system-prompts/`, from `templates/system-prompt.md`.

## Adding a task

For a large project run phase by phase, create `tasks/<name>/` containing:

- numbered `NN-<phase>.md` files in the prompt format (a letter suffix such as `04b` inserts a phase without renumbering);
- a `README.md` with the run order and session boundaries;
- a `vars.example` for shared variables (the filled `vars.local` copy is git-ignored);
- optional addenda referenced from phases via `append: <file>.md`.

## Versioning

Use semver in the `version` field:

- **patch** — wording fixes, no behavior change
- **minor** — new optional variable, added section in the output
- **major** — output format changes in a way that breaks anything parsing it

Record the reason in `## Changelog` at the bottom of the file.
