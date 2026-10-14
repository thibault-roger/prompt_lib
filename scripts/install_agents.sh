#!/usr/bin/env bash
# Symlink Claude Code agents from this repo into an agents directory.
# Usage: install_agents.sh [target_dir]   (default: ~/.claude/agents)
# Symlinks mean edits in this repo take effect immediately. Existing regular
# files with the same name are left alone and reported.
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
src_dir="$repo_dir/agents/claude-code"
target_dir="${1:-$HOME/.claude/agents}"

mkdir -p "$target_dir"

for src in "$src_dir"/*.md; do
  name="$(basename "$src")"
  dest="$target_dir/$name"
  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "skip    $name (a non-symlink file already exists at $dest)"
    continue
  fi
  ln -sfn "$src" "$dest"
  echo "linked  $name -> $dest"
done
