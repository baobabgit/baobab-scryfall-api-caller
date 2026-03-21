# Notes de release — baobab-scryfall-api-caller 1.0.0

**Date** : 2026-03-23

## Resume

Premiere release **stable** au sens [semver](https://semver.org/lang/fr/) : engagement
sur une API publique stable (`ScryfallApiCaller`, exports racine, services domaine)
pour les versions **1.x.y** compatibles. Le comportement runtime est aligne sur la
branche **0.2.0** ; le passage en **1.0.0** formalise la stabilite annoncee.

## Synthese fonctionnelle (perimetre V1)

La librairie couvre le **perimetre V1** du cahier des charges (`docs/01_specifications.md`)
et la matrice `docs/V1_compliance.md` :

- **Cards** : acces unitaires (id, MTGO, Cardmarket, set+numero), `get_named`, `search`
  (y compris `CardSearchQuery`), `autocomplete`, `random`, `get_collection`.
- **Sets** : liste, par code / id, cartes du set (`list_cards_in_set` / `..._by_id`).
- **Rulings** : par id carte, multiverse, MTGO, Arena (pagination).
- **Catalogs** : `get_catalog` et helpers.
- **Bulk data** : metadonnees, `download_bulk_dataset` optionnel avec
  `BulkDatasetDownloader` injecte.
- **Transversal** : pagination Scryfall (`ListResponse`, helpers), exceptions metier,
  cache GET optionnel (`InMemoryJsonCache`).

Le detail des ajouts cumules depuis **0.1.0** figure dans [`CHANGELOG.md`](../CHANGELOG.md).

## Architecture (points cles)

- **Transport** : tout passe par `baobab-web-api-caller` (injection de
  `WebApiTransportProtocol` / `BaobabServiceCaller`, etc.) ; pas de `requests` direct
  dans ce depot.
- **Facade** : `ScryfallApiCaller` regroupe `cards`, `sets`, `rulings`, `catalogs`,
  `bulk_data` ; transport expose en lecture seule.
- **Couche HTTP** : `ScryfallHttpClient` ; normalisation des erreurs via
  `ScryfallErrorTranslator`.
- **Typage** : PEP 561 (`py.typed`), modeles et services types.

## Dependance : `baobab-web-api-caller`

- Contrainte declaree : **`>=0.1.0,<2.0.0`** (voir `pyproject.toml`).
- Elle fournit le transport HTTP generique ; la combinaison de versions en production
  doit etre validee par l'integrateur (voir limitations ci-dessous).

## Limitations connues (honnetes)

- **Transport** : non instancie par la librairie — vous composez `ServiceConfig`,
  `HttpTransportCaller`, etc. (voir README).
- **Bulk** : pas de telechargement automatique sans `BulkDatasetDownloader` injecte.
- **Tests d'integration** : suite optionnelle sous `tests/integration` (reseau,
  marqueur `integration`).
- **CI** : pas de workflow GitHub Actions dans ce depot ; qualite attendue via
  execution locale ou pipeline externe (`CONTRIBUTING.md`, `make quality`).

## Installation minimale

```bash
pip install baobab-scryfall-api-caller==1.0.0
```

Dependance runtime installee automatiquement : `baobab-web-api-caller` dans la plage
semver ci-dessus.

```python
from baobab_scryfall_api_caller import ScryfallApiCaller, __version__

assert __version__ == "1.0.0"
# Injecter web_api_caller (voir README pour la composition complete).
```

## Publication PyPI (mainteneurs)

Checklist : [`publishing_checklist.md`](publishing_checklist.md) (build, `twine check`,
upload, tag — **sans** execution automatique dans ce depot).

## Historique changelog

Sections `[0.2.0]` et `[0.1.0]` dans [`CHANGELOG.md`](../CHANGELOG.md).
