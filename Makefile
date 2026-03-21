# Confort d'execution (Unix / Git Bash). Equivalents pip explicites dans le README.
.PHONY: install-dev install-integration-deps test-integration

install-dev:
	python -m pip install -e ".[dev]"

# Memes dependances que les tests unitaires : outils dev + baobab-web-api-caller (PyPI ou deja installe).
install-integration-deps: install-dev

test-integration:
	python -m pytest tests/integration --no-cov -m integration
