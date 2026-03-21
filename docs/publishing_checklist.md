# Checklist publication PyPI — baobab-scryfall-api-caller

Document **mainteneur** : preparer et publier une release (apres merge sur `main` et
validation locale). **Aucune publication automatique** depuis ce depot : pas de
workflow CI GitHub dans le referentiel (gate qualite : `CONTRIBUTING.md`, `make quality`).

## Avant publication

1. `main` a jour ; version dans `pyproject.toml` / `__version__` alignee avec
   `CHANGELOG.md` et le tag Git prevu (ex. **1.0.0** → tag **`v1.0.0`**).
2. Executer la gate qualite : `make quality` ou `scripts/run_quality.ps1` / `.sh`.
3. Tests d'integration live optionnels : `make test-integration` (reseau).

## Construire les artefacts

Depuis la racine du depot (environnement avec `build` installe : `pip install build`) :

```bash
python -m build
```

Sortie attendue sous `dist/` :

- `baobab_scryfall_api_caller-<version>.tar.gz` (sdist)
- `baobab_scryfall_api_caller-<version>-py3-none-any.whl` (wheel)

Verifier les noms de fichiers et la **version** dans les metadonnees.

## Verification des paquets (twine)

```bash
pip install twine
python -m twine check dist/*
```

Les dossiers `dist/` et `build/` sont listes dans `.gitignore` : ne pas les versionner.

## Installabilite (smoke test)

Creer un **venv propre**, installer uniquement le **wheel** PyPI ou le wheel local :

```bash
python -m venv .venv-test
.venv-test\Scripts\pip install dist\baobab_scryfall_api_caller-1.0.0-py3-none-any.whl
.venv-test\Scripts\python -c "from baobab_scryfall_api_caller import ScryfallApiCaller, __version__; print(__version__)"
```

Verifier que `baobab-web-api-caller` est bien installe en dependance.

## Publication PyPI (manuelle)

```bash
python -m twine upload dist/*
```

(Configurer les credentials PyPI / API token selon votre organisation.)

## Tag Git

Apres publication reussie (ou en meme temps selon la politique equipe) :

```bash
git tag -a v1.0.0 -m "baobab-scryfall-api-caller 1.0.0"
git push origin v1.0.0
```

## Notes

- **Limitations** consommateur : voir `README.md` et `docs/V1_compliance.md`.
- **Dependance** : `baobab-web-api-caller` doit etre resolvable sur PyPI dans la plage
  declaree dans `pyproject.toml`.
