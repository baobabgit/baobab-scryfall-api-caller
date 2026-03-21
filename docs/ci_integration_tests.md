# CI et dependance `baobab-web-api-caller` pour les tests d'integration

Ce depot **ne definit pas** de workflow GitHub Actions obligatoire ; les hypotheses
ci-dessous servent a reproduire un job propre en CI ou en machine ephemere.

## Principes

- **Couverture** : les jobs qui ne lancent que `tests/integration` doivent utiliser
  `--no-cov` (ou `make test-integration`). Sinon les `addopts` pytest appliquent le
  seuil global 90 % a une mesure partielle et le job echoue sans interet.
- **Aucun** `sys.path` ni `PYTHONPATH` artificiel : `baobab-web-api-caller` doit etre
  installe comme distribution Python (wheel ou editable).
- Les tests **unitaires** (`pytest` / `pytest tests/`) exigent la presence du wheel
  `baobab-web-api-caller` (voir `tests/.../test_baobab_web_api_caller_import.py`).
- Les tests **d'integration** (`tests/integration`) importent en outre le package
  `baobab_web_api_caller` (chaine reelle HTTP).

## Scenario A : dependances depuis PyPI (wheel)

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest tests/
python -m pytest tests/integration --no-cov -m integration
```

`pip` installe `baobab-web-api-caller` conformement a `pyproject.toml`.

## Scenario B : wheel `baobab-web-api-caller` produit en amont

Si un artefact `.whl` est disponible (build d'une autre pipeline) :

```bash
python -m pip install --upgrade pip
python -m pip install chemin/vers/baobab_web_api_caller-*.whl
python -m pip install -e ".[dev]"
python -m pytest tests/
python -m pytest tests/integration --no-cov -m integration
```

La deuxieme ligne installe le transport ; la troisieme installe ce projet et ses
dependances **dev** ; pip ne reinstalle pas `baobab-web-api-caller` si la version
satisfait la contrainte semver du `pyproject.toml`.

## Scenario C : clone editable local (developpement conjoint)

Ordre recommande :

1. `pip install -e /repo/baobab-web-api-caller`
2. `pip install -e /repo/baobab-scryfall-api-caller[dev]`

## Verification rapide dans un job

```bash
python -c "import importlib.metadata as m; print(m.version('baobab-web-api-caller'))"
python -c "import baobab_web_api_caller; print('import ok')"
```

## Reseau

Les tests d'integration appellent `https://api.scryfall.com` ; activer le job
uniquement si l'environnement CI autorise le trafic sortant.
