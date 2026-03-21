# Gate qualite locale (format, lint, types, securite, tests unitaires + couverture).
# Depuis la racine du depot : .\scripts\run_quality.ps1
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m black --check src tests
python -m flake8 src tests
python -m pylint src/baobab_scryfall_api_caller --fail-under=10
python -m mypy src/baobab_scryfall_api_caller
python -m bandit -c pyproject.toml -r src tests
python -m pytest @args
