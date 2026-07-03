#!/usr/bin/env bash
# Install festack from this shareable package.
# Delegates to festack/scripts/install.sh with the bundled plugin root.
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FESTACK_ROOT="$PACKAGE_ROOT/festack"

if [ ! -f "$FESTACK_ROOT/scripts/install.sh" ]; then
  echo "error: festack plugin not found at $FESTACK_ROOT" >&2
  echo "Make sure you run this from the festack repo root." >&2
  exit 1
fi

echo "festack"
echo "  package: $PACKAGE_ROOT"
echo "  plugin:  $FESTACK_ROOT"
echo

exec "$FESTACK_ROOT/scripts/install.sh" "$@"
