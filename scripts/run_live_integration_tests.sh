#!/usr/bin/env bash
# Tests d'integration live Scryfall (reseau requis). Sans couverture (--no-cov).
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pytest tests/integration --no-cov -m integration "$@"
