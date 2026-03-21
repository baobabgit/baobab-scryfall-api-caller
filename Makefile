# Confort d'execution (Unix / Git Bash). Equivalents explicites dans le README.
.PHONY: install-dev install-integration-deps test test-unit test-integration

install-dev:
	python -m pip install -e ".[dev]"

# Memes dependances que les tests unitaires : outils dev + baobab-web-api-caller (PyPI ou deja installe).
install-integration-deps: install-dev

# Suite par defaut : tests unitaires + couverture + seuil 90 % (pytest addopts).
test test-unit:
	python -m pytest

# Integration live seule : sans coverage (evite cov-fail-under sur un sous-ensemble).
test-integration:
	python -m pytest tests/integration --no-cov -m integration
