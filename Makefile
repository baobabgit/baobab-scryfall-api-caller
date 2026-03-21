# Confort d'execution (Unix / Git Bash). Equivalents : README, CONTRIBUTING.md, scripts/run_quality.*.
.PHONY: install-dev install-integration-deps test test-unit test-integration
.PHONY: format format-check lint typecheck security quality check

install-dev:
	python -m pip install -e ".[dev]"

# Memes dependances que les tests unitaires : outils dev + baobab-web-api-caller (PyPI ou deja installe).
install-integration-deps: install-dev

# Suite par defaut : tests unitaires + couverture + seuil 90 % (pytest addopts).
test test-unit:
	python -m pytest

# Integration live seule : sans coverage (evite cov-fail-under sur un sous-ensemble).
# Equivalent : scripts/run_live_integration_tests.ps1 ou .sh
test-integration:
	python -m pytest tests/integration --no-cov -m integration

format:
	python -m black src tests

format-check:
	python -m black --check src tests

lint:
	python -m flake8 src tests
	python -m pylint src/baobab_scryfall_api_caller --fail-under=10

typecheck:
	python -m mypy src/baobab_scryfall_api_caller

security:
	python -m bandit -c pyproject.toml -r src tests

# Gate locale complete (meme ordre que CONTRIBUTING.md).
quality check: format-check lint typecheck security test
