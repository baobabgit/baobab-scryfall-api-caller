# Contribuer a baobab-scryfall-api-caller

## Prerequis

- Python **3.11+**
- Depots clones avec `pip install -e ".[dev]"` a la racine de ce projet (voir `README.md`).

## Installation developpeur

```bash
python -m pip install -e ".[dev]"
```

Les tests d'integration live (`tests/integration`) necessitent en plus que
`baobab-web-api-caller` soit importable (PyPI ou editable) : voir `README.md`
section **baobab-web-api-caller**.

## Validation locale (gate avant PR)

Ordre recommande (rapide a diagnostiquer en cas d'echec) :

1. `python -m black --check src tests` (ou `make format-check`)
2. `python -m flake8 src tests`
3. `python -m pylint src/baobab_scryfall_api_caller --fail-under=10`
4. `python -m mypy src/baobab_scryfall_api_caller`
5. `python -m bandit -c pyproject.toml -r src tests`
6. `python -m pytest` (tests unitaires + couverture ; `tests/integration` exclu par defaut)

**Raccourci** (Unix / Git Bash / WSL avec `make`) :

```bash
make quality
```

**Sans Make** (PowerShell ou CMD depuis la racine du depot) :

```powershell
.\scripts\run_quality.ps1
```

Ou sous Bash :

```bash
./scripts/run_quality.sh
```

## Tests

| Objectif | Commande |
|----------|----------|
| Unitaires + couverture (defaut CI locale) | `python -m pytest` ou `make test` |
| Integration reseau Scryfall | `python -m pytest tests/integration --no-cov -m integration` ou `make test-integration` |

Ne pas lancer uniquement `tests/integration` **sans** `--no-cov` : les `addopts`
globaux appliquent le seuil de couverture a tout le package et le run peut echouer
sans lien avec une regression unitaire (voir `README.md`).

## Style et structure

- Arborescence miroir `src/` / `tests/`
- Pas d'appel HTTP direct hors `baobab-web-api-caller` (transport injecte)
- Exceptions projet : `BaobabScryfallApiCallerException` et sous-classes ; messages
  et contexte (`http_status`, `url`, etc.) pour le diagnostic

## Documentation

Pour une evolution notable : mettre a jour `CHANGELOG.md` et, si utile,
`docs/dev_diary.md` et `README.md`.

Pour une **release semver** : aligner `pyproject.toml` (`project.version`),
`baobab_scryfall_api_caller.__version__`, le test `test_package_bootstrap`, puis
`CHANGELOG` (section versionnee), `docs/V1_compliance.md` si la matrice change, et
eventuellement `docs/release_notes_X.Y.Z.md`.
