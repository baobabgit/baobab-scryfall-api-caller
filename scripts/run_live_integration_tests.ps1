# Tests d'integration live Scryfall (reseau requis). Sans couverture (--no-cov).
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pytest tests/integration --no-cov -m integration @args
