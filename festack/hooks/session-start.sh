#!/usr/bin/env bash
# festack sessionStart — inject FESTACK_HOME for Cursor agent sessions (IDE + CLI).
set -euo pipefail

resolve_festack_home() {
  if [ -n "${FESTACK_HOME:-}" ]; then
    printf '%s' "$FESTACK_HOME"
    return
  fi

  local pointer="$HOME/.cursor/festack/home"
  if [ -f "$pointer" ]; then
    tr -d '[:space:]' < "$pointer"
    return
  fi

  if [ -f "$HOME/.zshenv" ]; then
    local from_zshenv
    from_zshenv="$(
      grep -E '^export FESTACK_HOME=' "$HOME/.zshenv" 2>/dev/null | head -1 \
        | sed -E 's/^export FESTACK_HOME=//; s/^"//; s/"$//; s/'"'"'//g'
    )"
    if [ -n "$from_zshenv" ]; then
      printf '%s' "$from_zshenv"
      return
    fi
  fi

  if [ -f "$HOME/.claude/festack/profile.md" ]; then
    printf '%s' "$HOME/.claude/festack"
    return
  fi

  printf '%s' "$HOME/.cursor/festack"
}

HOME_DIR="$(resolve_festack_home)"
export FESTACK_HOME="$HOME_DIR"

python3 - <<'PY'
import json, os
home = os.environ.get("FESTACK_HOME", "")
parts = [f"festack: FESTACK_HOME={home}"]
if os.path.isfile(os.path.join(home, "profile.md")):
    parts.append("(profile present)")
if os.path.isfile(os.path.join(home, "engagements", "ENGAGEMENTS.md")):
    parts.append("(engagements ledger present)")
print(json.dumps({
    "env": {"FESTACK_HOME": home},
    "additional_context": " ".join(parts),
}))
PY
