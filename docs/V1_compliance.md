# Conformite V1 — baobab-scryfall-api-caller

Document de synthese par rapport au cahier des charges (`docs/01_specifications.md`)
et a l'etat du code a la release **0.2.0** (perimetre fonctionnel V1 conserve ;
extensions post-0.1.0 integrees dans le tableau ci-dessous).

## Exigences structurelles

| Exigence | Statut | Commentaire |
|----------|--------|-------------|
| Transport via `baobab-web-api-caller` uniquement | OK | Dependance PyPI bornee ; `ScryfallHttpClient` + `BaobabQueryParamsNormalizer` ; injection `WebApiTransportProtocol` |
| GET et POST exposes au niveau transport | OK | `ScryfallHttpClient`, `CardsApiClient` (POST collection) |
| Classes, une classe par fichier | OK | Respecte la convention projet |
| Tests miroir, classes `Test...` | OK | `tests/` aligne sur `src/` |
| Couverture >= 90 % | OK | `pytest-cov` + `fail_under` ; gate locale (`make quality`, `CONTRIBUTING.md`) |
| Typage public, `py.typed` | OK | `pyproject.toml` + marqueur PEP 561 |
| Exceptions racine projet | OK | `BaobabScryfallApiCallerException` et derivees |
| Qualite (black, pylint, mypy, flake8, bandit) | OK | Configuration `pyproject.toml` ; execution locale ou pipeline externe |
| Tests d'integration reseau (optionnels) | OK | `tests/integration`, marqueur `integration`, chaine `baobab-web-api-caller` + `ScryfallApiCaller` |

## Perimetre fonctionnel (services)

| Domaine | Cahier des charges V1 | Implementation (0.2.0) |
|---------|------------------------|-------------------------|
| **Cards** | id, MTGO, Cardmarket, set+numero, named, search, collection, autocomplete, random | `get_by_id`, `get_by_mtgo_id`, `get_by_cardmarket_id`, `get_by_set_and_number`, `get_named` (exact/fuzzy), `search`, `get_collection`, `autocomplete`, `random` |
| **Sets** | liste, par code, par id, cartes par set | `list_sets`, `get_by_code`, `get_by_id`, `list_cards_in_set`, `list_cards_in_set_by_id` |
| **Rulings** | par id carte et cles alternatives | `list_for_card_id`, `list_for_card_multiverse_id`, `list_for_card_mtgo_id`, `list_for_card_arena_id` (pagination) |
| **Catalogs** | generique + helpers | `get_catalog`, `get_card_names`, `get_creature_types`, `get_land_types`, `get_card_types`, `get_artist_names` |
| **Bulk data** | liste, metadonnees, telechargement optionnel | `list_bulk_datasets`, `get_by_id`, `get_by_type`, `download_bulk_dataset` (avec `BulkDatasetDownloader` injecte) |

### Domaine Cards (synthese V1)

Le perimetre V1 Cards du cahier des charges est couvert par `CardsService` et expose via
`ScryfallApiCaller.cards`, avec validations et mappers alignes sur le domaine.

## Facade publique

| Exigence | Statut |
|----------|--------|
| Point d'entree `ScryfallApiCaller` | OK |
| Services `cards`, `sets`, `rulings`, `catalogs`, `bulk_data` | OK |
| Transport injecte accessible en lecture (`web_api_caller`) | OK |

## Hors perimetre V1 (specifications)

Conformement a `docs/01_specifications.md`, ne sont pas requis en V1 : couverture
exhaustive de tous les endpoints secondaires, **telechargement bulk sans injection
explicite** (le telechargement assiste en 0.2.0 est opt-in via `BulkDatasetDownloader`),
retry avance, persistance locale, CLI, integration asynchrone, etc. Le **cache GET**
optionnel (0.2.0) est en memoire processus et desactive par defaut.

## Ecarts et limitations connues

- **Tests d'integration** : disponibles sous `tests/integration` (a la demande, reseau
  requis) ; la suite par defaut reste **unitaire** pour la couverture et la rapidite.
- **Telechargement bulk** : optionnel via `BulkDatasetDownloader` (voir README).
- **Wheel `baobab-web-api-caller`** : les tests du depot evitent l'import top-level du
  paquet dependance en CI pour rester robustes ; l'integrateur doit valider la
  combinaison de versions en environnement reel.

## Recommandations post-V1

1. Etendre ou ajuster les tests d'integration (`tests/integration`) selon l'evolution
   de l'API Scryfall ou des besoins de non-regression reseau.
2. Pinner ou documenter les combinaisons `baobab-scryfall-api-caller` /
   `baobab-web-api-caller` validees en production.
3. Etendre le perimetre endpoints (symbologie, backs, etc.) selon les besoins produit,
   sans casser l'API publique stable (`ScryfallApiCaller` + services).

## Bilan release 0.2.0 (publication)

| Critere | Statut |
|---------|--------|
| Domaines V1 (Cards, Sets, Rulings, Catalogs, Bulk Data) | OK — alignes sur le code et les tests |
| Extensions post-0.1.0 (CHANGELOG `[0.2.0]`) | OK — documentees (README, CHANGELOG, journal) |
| Pagination / exceptions / transport injecte | OK |
| Documentation (README, CHANGELOG, cette matrice, `CONTRIBUTING.md`) | OK |
| Qualite (black, pylint, mypy, flake8, bandit, pytest) | OK — execution locale / pipeline externe |
| Couverture | OK — > 90 % |

Notes de release synthetiques : `docs/release_notes_0.2.0.md`.

**Risques residuels** : voir section *Ecarts et limitations connues* ; combinaison de
versions avec le wheel `baobab-web-api-caller` a valider chez l'integrateur.

## Bilan historique — release 0.1.0 (RC)

Avant tag **0.1.0** / publication initiale : memes criteres structurels ; matrice et
README synchronises sur la branche RC ; couverture cible ~97 % sur le code mesure.
