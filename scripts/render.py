#!/usr/bin/env python3
"""Render a prompt file: fill {{variables}} and print the `## Prompt` section.

Examples:
  render.py prompts/coding/code-review.md --var language=python --var diff=@change.diff
  render.py tasks/ds-platform-refactor/03-runner.md --vars-file tasks/ds-platform-refactor/vars.local
  render.py prompts/data/sql-from-question.md --list
"""

import argparse
import sys
from pathlib import Path

from promptlib import PLACEHOLDER, load, section


def read_value(raw):
    """`@path` reads a file; anything else is a literal."""
    if raw.startswith("@"):
        return Path(raw[1:]).expanduser().read_text(encoding="utf-8")
    return raw


def parse_vars_file(path):
    values = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            sys.exit("render: bad line in {}: {!r} (expected KEY=value)".format(path, line))
        value = value.strip()
        if value:  # empty means "not set", so the missing-variable check still fires
            values[key.strip()] = read_value(value)
    return values


def prompt_text(path):
    meta, body = load(path)
    text = section(body, "Prompt")
    if text is None:
        sys.exit("render: {} has no '## Prompt' section".format(path))
    return meta, text


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", type=Path)
    parser.add_argument("--var", action="append", default=[], metavar="KEY=VALUE",
                        help="set a variable; VALUE may be @path to read a file (repeatable)")
    parser.add_argument("--vars-file", type=Path, help="KEY=VALUE file; --var overrides it")
    parser.add_argument("--append", type=Path, action="append", default=[],
                        help="extra prompt file whose Prompt section is appended (repeatable)")
    parser.add_argument("--no-append", action="store_true", help="ignore the file's `append:` frontmatter")
    parser.add_argument("--allow-missing", action="store_true", help="leave unset placeholders as-is")
    parser.add_argument("--list", action="store_true", help="list the variables and exit")
    args = parser.parse_args()

    meta, text = prompt_text(args.file)

    appended = [] if args.no_append else [args.file.parent / a for a in _as_list(meta.get("append"))]
    for extra in appended + args.append:
        _, extra_text = prompt_text(extra)
        text = text + "\n\n" + extra_text

    used = list(dict.fromkeys(PLACEHOLDER.findall(text)))  # first-appearance order
    if args.list:
        for name in used:
            print(name)
        return

    values = parse_vars_file(args.vars_file) if args.vars_file else {}
    for item in args.var:
        key, sep, value = item.partition("=")
        if not sep:
            sys.exit("render: --var expects KEY=VALUE, got {!r}".format(item))
        values[key] = read_value(value)

    missing = [name for name in used if name not in values]
    if missing and not args.allow_missing:
        sys.exit("render: missing variables: {}".format(", ".join(missing)))

    def substitute(match):
        name = match.group(1)
        return values.get(name, match.group(0))

    sys.stdout.write(PLACEHOLDER.sub(substitute, text) + "\n")


def _as_list(value):
    if not value:
        return []
    return value if isinstance(value, list) else [value]


if __name__ == "__main__":
    main()
