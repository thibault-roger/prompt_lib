"""Shared helpers: frontmatter parsing and prompt-section extraction (stdlib only)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Only identifier-style placeholders are variables. Dotted ones such as Argo's
# {{inputs.parameters.name}} or {{workflow.name}} are literal text.
PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


def parse_frontmatter(text):
    """Return (metadata, body). Supports `key: value` and `key: [a, b]` lines."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError("bad frontmatter line: {!r}".format(line))
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key.strip()] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = value.strip("\"'")
    return meta, text[end + len("\n---\n"):]


def section(body, heading):
    """Text under `## <heading>` up to the next level-2 heading, or None."""
    match = re.search(r"^## {}\s*$(.*?)(?=^## |\Z)".format(re.escape(heading)), body, re.M | re.S)
    return match.group(1).strip() if match else None


def load(path):
    path = Path(path)
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    return meta, body
