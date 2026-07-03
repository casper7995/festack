#!/usr/bin/env bash
# Run festack's automated contract tests.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m unittest tests.test_hook -v
