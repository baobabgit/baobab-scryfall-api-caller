# Changelog

Toutes les evolutions notables du projet seront documentees dans ce fichier.

Le format suit les recommandations de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et le projet suit le versioning semantique.

## [Unreleased]

### Added

- **Tests d'integration reseau** : dossier `tests/integration` (marqueur pytest
  `integration`, fixture `live_scryfall_client` via `baobab-web-api-caller` et
  `ScryfallApiCaller`), jeux de donnees dans `scryfall_live_constants.py` ;
  execution : `python -m pytest tests/integration --no-cov`.

### Removed

- **Workflow GitHub Actions** : suppression de `.github/workflows/ci.yml` (plus de CI
  dans le depot).

### Changed

- **Tests d'integration live** : configuration centralisee dans
  `tests/integration/live_transport_config.py` — throttling ~**6 req/s**
  (`RateLimitPolicy`, intervalle minimal **1/6 s**), en-tetes par defaut
  `User-Agent` (integration) et `Accept: application/json; charset=utf-8` injectes via
  `ServiceConfig` ; fixture `live_scryfall_client` mise a jour dans `conftest.py`.
- **pytest** : `tests/integration` exclu par defaut (`--ignore`) pour que `pytest` /
  `pytest tests/` n'executent que les tests unitaires avec couverture ; marker
  `integration` enregistre dans `pyproject.toml`.
- **Documentation** : README (section tests d'integration, suppression badge CI).
- **Stabilisation V1 (release candidate)** : tests supplementaires sur les branches
  d'erreur de `BulkDataMapper` ; validation `SetsService.get_by_code` lorsque le code
  n'est pas une chaine ; `ScryfallRequestValidators.require_uuid_string` lorsque la
  valeur n'est pas une chaine ; couverture globale ~97 %.
- **Packaging** : classifier PyPI `Development Status :: 5 - Production/Stable`
  (V1 pret pour publication).

## [0.1.0] - 2026-03-20

Premiere release publique : perimetre fonctionnel **V1** aligne sur
`docs/01_specifications.md` et synthese dans `docs/V1_compliance.md`.

### Added

- **Packaging** : `pyproject.toml` (PEP 621), `requires-python >= 3.11`, dependance
  `baobab-web-api-caller>=0.1.0,<2.0.0`, marqueur PEP 561 (`py.typed`).
- **Facade** : `ScryfallApiCaller` avec les services `cards`, `sets`, `rulings`,
  `catalogs`, `bulk_data` et le transport injecte (`web_api_caller`).
- **Exports racine** : `ScryfallApiCaller`, `WebApiTransportProtocol`, `__version__`
  (depuis `baobab_scryfall_api_caller`).
- **Exports `client`** : `ScryfallApiCaller`, `ScryfallHttpClient`,
  `WebApiTransportProtocol`.
- **Cards (V1)** : acces unitaires (`get_by_id`, `get_by_mtgo_id`,
  `get_by_cardmarket_id`, `get_by_set_and_number`), `get_named`, `search`,
  `autocomplete`, `random`, `get_collection` ; modeles et mappers associes.
- **Sets** : `list_sets`, `get_by_code`, `get_by_id`.
- **Rulings** : `list_for_card_id` (pagination).
- **Catalogs** : `get_catalog` et helpers (`get_card_names`, `get_creature_types`,
  `get_land_types`, `get_card_types`, `get_artist_names`).
- **Bulk data** : `list_bulk_datasets`, `get_by_id`, `get_by_type` (metadonnees et
  URL, sans telechargement de fichiers).
- **Transversal** : `ScryfallHttpClient`, validateurs partages, hierarchie
  d'exceptions metier, `ListResponse` / pagination Scryfall.
- **CI** : GitHub Actions (black, pylint, mypy, flake8, bandit, pytest, couverture
  minimale 90 %).
- **Documentation** : README, matrice `docs/V1_compliance.md`, journal
  `docs/dev_diary.md`.

### Changed

- Harmonisation Cards V1 : validations texte via `ScryfallRequestValidators` ;
  docstrings `CardsService` / `ScryfallApiCaller` ; tests de surface et
  `FakeBaobabStyleResponse` / `importlib.metadata` pour la CI (wheel PyPI +
  Python 3.11).

### Fixed

- Documentation (README, changelog) alignee sur les methodes effectivement
  exposees par les services.
