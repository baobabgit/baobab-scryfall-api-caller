# Conformite V1 — baobab-scryfall-api-caller

Document de synthese par rapport au cahier des charges (`docs/01_specifications.md`)
et a l'etat du code a la release **0.1.0** (perimetre fonctionnel V1).

## Exigences structurelles

| Exigence | Statut | Commentaire |
|----------|--------|-------------|
| Transport via `baobab-web-api-caller` uniquement | OK | Dependance PyPI bornee ; `ScryfallHttpClient` + `BaobabQueryParamsNormalizer` ; injection `WebApiTransportProtocol` |
| GET et POST exposes au niveau transport | OK | `ScryfallHttpClient`, `CardsApiClient` (POST collection) |
| Classes, une classe par fichier | OK | Respecte la convention projet |
| Tests miroir, classes `Test...` | OK | `tests/` aligne sur `src/` |
| Couverture >= 90 % | OK | `pytest-cov` + `fail_under` ; verifie en CI |
| Typage public, `py.typed` | OK | `pyproject.toml` + marqueur PEP 561 |
| Exceptions racine projet | OK | `BaobabScryfallApiCallerException` et derivees |
| Qualite (black, pylint, mypy, flake8, bandit) | OK | Configuration `pyproject.toml` ; CI GitHub Actions sur `main` |

## Perimetre fonctionnel (services)

| Domaine | Cahier des charges V1 | Implementation (0.1.0) |
|---------|------------------------|-------------------------|
| **Cards** | id, MTGO, Cardmarket, set+numero, named, search, collection, autocomplete, random | `get_by_id`, `get_by_mtgo_id`, `get_by_cardmarket_id`, `get_by_set_and_number`, `get_named` (exact/fuzzy), `search`, `get_collection`, `autocomplete`, `random` |
| **Sets** | liste, par code, par id | `list_sets`, `get_by_code`, `get_by_id` |
| **Rulings** | par id carte | `list_for_card_id` (pagination) |
| **Catalogs** | generique + helpers | `get_catalog`, `get_card_names`, `get_creature_types`, `get_land_types`, `get_card_types`, `get_artist_names` |
| **Bulk data** | liste, metadonnees, URL telechargement | `list_bulk_datasets`, `get_by_id`, `get_by_type` (`download_uri` expose ; pas de telechargement fichier) |

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
exhaustive de tous les endpoints secondaires, telechargement automatique des fichiers
bulk, cache applicatif, retry avance, persistance locale, CLI, integration asynchrone,
etc.

## Ecarts et limitations connues

- **Tests d'integration reseau** : non inclus dans ce depot (suite unitaire avec mocks).
- **Telechargement bulk** : non implemente (seules metadonnees + URL).
- **Wheel `baobab-web-api-caller`** : les tests du depot evitent l'import top-level du
  paquet dependance en CI pour rester robustes ; l'integrateur doit valider la
  combinaison de versions en environnement reel.

## Recommandations post-V1

1. Ajouter des tests d'integration optionnels (marqueurs pytest) contre l'API Scryfall
   ou un mock HTTP de reference.
2. Pinner ou documenter les combinaisons `baobab-scryfall-api-caller` /
   `baobab-web-api-caller` validees en production.
3. Etendre le perimetre endpoints (symbologie, backs, etc.) selon les besoins produit,
   sans casser l'API publique stable (`ScryfallApiCaller` + services).
