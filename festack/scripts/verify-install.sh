#!/usr/bin/env bash
# Verify festack skills and agents are linked for a host.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0
HOST="${1:-cursor}"
BASE_HOME="$HOME"
if [ "${2:-}" = "--home" ]; then
  BASE_HOME="${3:-}"
fi

case "$HOST" in
  cursor) HOST_DIR="$BASE_HOME/.cursor" ;;
  claude) HOST_DIR="$BASE_HOME/.claude" ;;
  codex) HOST_DIR="$BASE_HOME/.codex" ;;
  *)
    echo "usage: scripts/verify-install.sh [cursor|claude|codex] [--home PATH]"
    exit 1
    ;;
esac

check() {
  if [ -e "$2" ]; then
    echo "  OK  $1"
  else
    echo "  MISS $1 -> $2"
    FAIL=1
  fi
}

echo "festack $HOST skills and agents verification"
echo
for d in "$ROOT"/skills/*/; do
  name="$(basename "${d%/}")"
  check "/$name" "$HOST_DIR/skills/$name/SKILL.md"
done
for a in "$ROOT"/agents/*.md; do
  name="$(basename "$a")"
  check "$name" "$HOST_DIR/agents/$name"
done

echo
if [ "$FAIL" -eq 0 ]; then
  echo "All skills and agents present. Reload Cursor if slash menu is stale."
else
  echo "Install incomplete. Run: scripts/install.sh $HOST"
  exit 1
fi
