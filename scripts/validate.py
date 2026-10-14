#!/usr/bin/env python3
"""Lint the library: frontmatter fields, required sections, and that declared
`variables` match the {{placeholders}} used in `## Prompt` (both ways).

Exit code 1 if any error is found.
"""

import sys

from promptlib import PLACEHOLDER, ROOT, load, section

PROMPT_FIELDS = ("title", "description", "tags", "variables", "version")
AGENT_FIELDS = ("name", "description", "tools")
WORKFLOW_FIELDS = ("title", "description")


def check_prompt(path, meta, body, errors):
    for field in PROMPT_FIELDS:
        if field not in meta:
            errors.append("{}: missing frontmatter field '{}'".format(path, field))
    text = section(body, "Prompt")
    if text is None:
        errors.append("{}: missing '## Prompt' section".format(path))
        return
    declared = set(meta.get("variables") or [])
    used = set(PLACEHOLDER.findall(text))
    for name in sorted(used - declared):
        errors.append("{}: placeholder {{{{{}}}}} not declared in variables".format(path, name))
    for name in sorted(declared - used):
        errors.append("{}: variable '{}' declared but not used in ## Prompt".format(path, name))
    appends = meta.get("append")
    for name in ([appends] if isinstance(appends, str) else appends or []):
        if not (path.parent / name).is_file():
            errors.append("{}: append target '{}' not found".format(path, name))


def check_agent(path, meta, errors):
    for field in AGENT_FIELDS:
        if field not in meta:
            errors.append("{}: missing frontmatter field '{}'".format(path, field))
    if meta.get("name") and meta["name"] != path.stem:
        errors.append("{}: name '{}' should match filename '{}'".format(path, meta["name"], path.stem))


def main():
    errors = []
    counts = {"prompts": 0, "tasks": 0, "agents": 0, "system-prompts": 0, "workflows": 0}

    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        top = rel.parts[0]
        if len(rel.parts) == 1 or top == "templates" or path.name == "README.md":
            continue
        try:
            meta, body = load(path)
        except ValueError as exc:
            errors.append("{}: {}".format(rel, exc))
            continue
        rel_path = ROOT / rel
        if top in ("prompts", "tasks"):
            check_prompt(rel_path, meta, body, errors)
            counts[top] += 1
        elif rel.parts[:2] == ("agents", "claude-code"):
            check_agent(rel_path, meta, errors)
            counts["agents"] += 1
        elif rel.parts[:2] == ("agents", "system-prompts"):
            check_prompt(rel_path, meta, body, errors)
            counts["system-prompts"] += 1
        elif top == "workflows":
            for field in WORKFLOW_FIELDS:
                if field not in meta:
                    errors.append("{}: missing frontmatter field '{}'".format(rel, field))
            counts["workflows"] += 1

    summary = ", ".join("{} {}".format(n, k) for k, n in counts.items())
    if errors:
        print("\n".join(str(e).replace(str(ROOT) + "/", "") for e in errors))
        print("\nFAILED ({} errors) — checked {}".format(len(errors), summary))
        sys.exit(1)
    print("OK — checked {}".format(summary))


if __name__ == "__main__":
    main()
