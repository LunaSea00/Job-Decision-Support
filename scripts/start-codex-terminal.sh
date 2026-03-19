#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v codex >/dev/null 2>&1; then
  echo "codex command not found in PATH"
  echo "Install Codex CLI first, then reopen this workspace."
  exec bash -i
fi

exec codex
