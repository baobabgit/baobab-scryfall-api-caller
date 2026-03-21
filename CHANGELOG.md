# Changelog

Toutes les evolutions notables du projet seront documentees dans ce fichier.

Le format suit les recommandations de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et le projet suit le versioning semantique.

## [Unreleased]

### Added

- **DX / diagnostic** : `CONTRIBUTING.md` (workflow local) ; Makefile etendu
  (`format`, `format-check`, `lint`, `typecheck`, `security`, `quality` / `check`) ;
  scripts `scripts/run_quality.ps1` et `scripts/run_quality.sh` ; pytest avec
  **`-ra`** (resume des skips / xfails) ; messages d'erreur par defaut du
  `ScryfallErrorTranslator` enrichis avec la route quand disponible ; `str()` sur
  `BaobabScryfallApiCallerException` tronque les gros `repr` de contexte ; message
  plus explicite si la reponse HTTP n'est pas un JSON dict exploitable ; tests bulk
  alignes sur la gate `bandit` (`tmp_path` / `# nosec B108` ou cas fictif).
- **Modeles** : `ImageUris` ; enrichissement de `Card` (type line, oracle text,
  rarete, cmc, couleurs, langue, artiste, images, jeux, legalites, drapeaux foil,
  etc.), de `CardFace` (loyalty, defense, flavor, artiste, `image_uris`), et
  `ruling_id` optionnel sur `Ruling` ; coercitions `as_optional_float`,
  `as_string_tuple`, `as_legalities_tuple` ; tests de mapping.
- **Rulings** : `list_for_card_multiverse_id`, `list_for_card_mtgo_id`,
  `list_for_card_arena_id` (routes Scryfall alignees sur les identifiants alternatifs).
- **Sets** : `list_cards_in_set`, `list_cards_in_set_by_id` (`GET /sets/.../cards`) ;
  `SetsService` accepte un `CardMapper` injectable ; predicat de cache par defaut :
  pas de mise en cache des listes `/sets/.../cards`.
- **Bulk Data : telechargement assiste** : `BulkDatasetDownloader` (delegation a
  `BulkFileDownloader` de `baobab-web-api-caller`), methodes
  `download_bulk_dataset` / `download_bulk_dataset_by_type` / `download_bulk_dataset_by_id`
  sur `BulkDataService`, injection via `ScryfallApiCaller(bulk_dataset_downloader=...)` ;
  modele `BulkDownloadResult` ; strategie `overwrite` explicite ; tests et README.
- **Cache optionnel** : protocole `JsonResponseCache`, implementation `InMemoryJsonCache`
  (memoire processus uniquement), integration dans `ScryfallHttpClient` et facade
  `ScryfallApiCaller` (`response_cache`, `cacheable_get_predicate`) ; predicat par defaut
  pour catalogs / sets / bulk-data / rulings / carte par UUID ; tests et README.
- **Recherche cartes** : `CardSearchQuery` (helpers `type_line`, `oracle`, `name_contains`,
  `set_code`, `cmc`, `raw`) ; `CardsService.search` accepte `query=` en alternative a
  `q=` (exactement l'un des deux). README et tests.
- **Pagination** : ergonomie Python sur `ListResponse` (`__iter__`, `__len__`, `__bool__`,
  `items`, `is_empty`, `count`, raccourcis `total_cards` / `warnings`, `__repr__`) ;
  `ScryfallPage` aligne ; helpers explicites `iter_list_pages` et `iter_list_items`
  dans `baobab_scryfall_api_caller.pagination` (aucun GET sans `fetch_next` fourni par
  l'appelant). README et tests unitaires associes.
- **Documentation tests live** : `docs/live_integration_tests.md` (chaine d'injection,
  marqueur `integration`, `--no-cov`, politique HTTP) ; scripts
  `scripts/run_live_integration_tests.ps1` / `.sh` ; liens depuis README et
  `docs/ci_integration_tests.md`.
- **Integration live** : fabrique `build_live_scryfall_client()` dans
  `tests/integration/live_transport_config.py` (point unique pour la fixture) ;
  scenarios supplementaires (`sets.get_by_id` en coherence avec `get_by_code`,
  `catalogs.get_catalog`, `bulk_data.get_by_type` / `get_by_id`, erreur de validation
  locale sur `cards.get_named()` sans parametres).
- **Documentation installation `baobab-web-api-caller`** : README (modes wheel PyPI,
  editable local, wheel fichier ; verification d'import ; ordre d'installation ;
  cibles `Makefile`), guide `docs/ci_integration_tests.md` (hypotheses CI sans
  workflow obligatoire).
- **Makefile** : cibles `install-dev`, `install-integration-deps`, `test`,
  `test-unit`, `test-integration` (equivalents documentes dans le README).
- **Tests d'integration reseau** : dossier `tests/integration` (marqueur pytest
  `integration`, fixture `live_scryfall_client` via `baobab-web-api-caller` et
  `ScryfallApiCaller`), jeux de donnees dans `scryfall_live_constants.py` ;
  execution : `python -m pytest tests/integration --no-cov -m integration` ou
  `make test-integration`.

### Removed

- **Workflow GitHub Actions** : suppression de `.github/workflows/ci.yml` (plus de CI
  dans le depot).

### Changed

- **pytest / couverture** : README, `docs/ci_integration_tests.md`, commentaire dans
  `pyproject.toml` — executer uniquement `tests/integration` avec `--no-cov` (ou
  `make test-integration`) pour eviter `cov-fail-under` sur une mesure partielle ;
  seuil 90 % inchange pour `pytest` / `pytest tests/`.
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
