#!/usr/bin/env bash
# festack installer. Links festack's skills + agents into a host so its
# commands load. One source of truth (this repo); each host gets the right wiring.
#
# Usage:
#   scripts/install.sh cursor          install skills + agents globally (recommended)
#   scripts/install.sh cursor --plugin-only   local plugin symlink only (needs userLocal plugins on)
#   scripts/install.sh claude          link skills + agents into Claude Code (~/.claude)
#   scripts/install.sh codex           link skills + agents into Codex (~/.codex)
#
#   --copy   copy instead of symlink (Windows, or locked-down environments)
#   --force  replace existing non-festack targets
#
# Claude Code and Codex use the same SKILL.md format, so the skills are portable
# as-is. The per-host tool and model tweaks are documented in README "Portability".
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${1:-}"; shift || true
COPY=0; PLUGIN_ONLY=0; FORCE=0
for a in "$@"; do
  [ "$a" = "--copy" ] && COPY=1
  [ "$a" = "--plugin-only" ] && PLUGIN_ONLY=1
  [ "$a" = "--force" ] && FORCE=1
  [ "$a" = "--dev" ] && echo "  note: --dev is deprecated; default cursor install now links skills directly" >&2
done

is_managed_target() { # src dst
  [ ! -e "$2" ] && return 0
  [ "$FORCE" = 1 ] && return 0
  if [ -L "$2" ]; then
    local target
    target="$(readlink "$2")"
    [[ "$target" == "$ROOT"* ]] && return 0
  fi
  [ -d "$2" ] && [ -f "$2/.festack-managed" ] && return 0
  [ -f "$1" ] && [ -f "$2" ] && cmp -s "$1" "$2" && return 0
  return 1
}

put() { # src dst  -- symlink (default) or copy
  mkdir -p "$(dirname "$2")"
  if ! is_managed_target "$1" "$2"; then
    echo "Refusing to overwrite unmanaged target: $2" >&2
    echo "Re-run with --force if you intentionally want to replace it." >&2
    exit 1
  fi
  rm -rf "$2"
  if [ "$COPY" = 1 ]; then
    cp -R "$1" "$2"
    [ -d "$2" ] && touch "$2/.festack-managed"
  else
    ln -s "$1" "$2"
  fi
  return 0
}

remove_stale_skill_links() { # SKILLS_DIR
  local skills_dir="$1"
  for name in festack-mode solution review; do
    local target="$skills_dir/$name"
    [ -e "$target" ] || [ -L "$target" ] || continue
    if [ -L "$target" ]; then
      local link_target
      link_target="$(readlink "$target")"
      if [[ "$link_target" == "$ROOT"* ]]; then
        rm -rf "$target"
      fi
    elif [ -d "$target" ] && [ -f "$target/.festack-managed" ]; then
      rm -rf "$target"
    fi
  done
}

link_all() { # SKILLS_DIR AGENTS_DIR  -- link every skill folder + agent
  mkdir -p "$1" "$2"
  remove_stale_skill_links "$1"
  for d in "$ROOT"/skills/*/; do
    put "${d%/}" "$1/$(basename "${d%/}")"
  done
  for a in "$ROOT"/agents/*.md; do
    put "$a" "$2/$(basename "$a")"
  done
  echo "  linked $(ls -d "$ROOT"/skills/*/ | wc -l | tr -d ' ') skills + $(ls "$ROOT"/agents/*.md | wc -l | tr -d ' ') agents"
}

case "$HOST" in
  cursor)
    if [ "$PLUGIN_ONLY" = 0 ]; then
      echo "festack: installing into ~/.cursor/skills + ~/.cursor/agents"
      link_all "$HOME/.cursor/skills" "$HOME/.cursor/agents"
      put "$ROOT" "$HOME/.cursor/plugins/local/festack"
      echo "  also linked plugin manifest at ~/.cursor/plugins/local/festack"
      put "$ROOT/hooks" "$HOME/.cursor/festack/hooks"
      echo "  also linked last-look hooks at ~/.cursor/festack/hooks (merge hooks/cursor-hooks.json into ~/.cursor/hooks.json)"
    else
      echo "festack: installing local Cursor plugin manifest only"
      put "$ROOT" "$HOME/.cursor/plugins/local/festack"
      echo "  linked plugin manifest at ~/.cursor/plugins/local/festack"
    fi
    echo "  Reload Cursor (Developer: Reload Window), then type /festack, /autopilot, etc."
    ;;
  claude)
    echo "festack: installing into Claude Code (~/.claude)"
    link_all "$HOME/.claude/skills" "$HOME/.claude/agents"
    put "$ROOT/hooks" "$HOME/.claude/festack/hooks"
    echo "  also linked last-look hooks at ~/.claude/festack/hooks"
    echo "  Tool/model tweaks: see README 'Portability'. Run /setup-models once to map models."
    ;;
  codex)
    echo "festack: installing into Codex (~/.codex)"
    link_all "$HOME/.codex/skills" "$HOME/.codex/agents"
    put "$ROOT/hooks" "$HOME/.codex/festack/hooks"
    echo "  also linked last-look hooks at ~/.codex/festack/hooks"
    echo "  Tool/model tweaks: see README 'Portability'. Run /setup-models once to map models."
    ;;
  *)
    echo "usage: scripts/install.sh [cursor|claude|codex] [--plugin-only] [--copy]"
    exit 1
    ;;
esac
