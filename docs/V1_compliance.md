# Conformite V1 — baobab-scryfall-api-caller

Document de synthese par rapport au cahier des charges (`docs/01_specifications.md`)
et a l'etat du code a la finalisation V1.

## Exigences structurelles

| Exigence | Statut | Commentaire |
|----------|--------|-------------|
| Transport via `baobab-web-api-caller` uniquement | OK | Dependance PyPI bornee ; `ScryfallHttpClient` + `BaobabQueryParamsNormalizer` ; injection `WebApiTransportProtocol` |
| GET et POST exposes au niveau transport | OK | `ScryfallHttpClient`, `CardsApiClient` |
| Classes, une classe par fichier | OK | Respecte la convention projet |
| Tests miroir, classes `Test...` | OK | `tests/` aligne sur `src/` |
| Couverture >= 90 % | OK | Verifiee en CI locale (`pytest-cov`) |
| Typage public, `py.typed` | OK | `pyproject.toml` + marqueur PEP 561 |
| Exceptions racine projet | OK | `BaobabScryfallApiCallerException` et derivees |
| Qualite (black, pylint, mypy, flake8, bandit) | OK | Configuration `pyproject.toml` |

## Perimetre fonctionnel (services)

| Domaine | Cahier des charges V1 | Implementation actuelle |
|---------|------------------------|-------------------------|
| **Cards** | id, MTGO, Cardmarket, set+numero, named, search, collection, autocomplete, random | id, MTGO, Cardmarket, set+numero, named (exact/fuzzy) |
| **Sets** | liste, par code, par id | `list_sets`, `get_by_code`, `get_by_id` |
| **Rulings** | par id carte | `list_for_card_id` |
| **Catalogs** | generique + helpers | `get_catalog` + helpers |
| **Bulk data** | liste, metadonnees, URL telechargement | `list_bulk_datasets`, `get_by_id`, `get_by_type` |

### Ecarts residuels (Cards)

Les endpoints Scryfall **search**, **collection**, **autocomplete** et **random** sont
listes au cahier des charges mais **non** exposes par `CardsService` dans cette V1.
Le transport (`POST` JSON) est pret cote `CardsApiClient` pour de futures extensions.

## Facade publique

| Exigence | Statut |
|----------|--------|
| Point d'entree `ScryfallApiCaller` | OK |
| Services `cards`, `sets`, `rulings`, `catalogs`, `bulk_data` | OK |

## Recommandations post-V1

1. Implementer les endpoints Cards manquants en conservant les validateurs et mappers.
2. Envisager des tests d'integration contre l'API Scryfall (hors scope des tests unitaires actuels).
3. Documenter les versions de `baobab-web-api-caller` validees en integration continue.
