# Cahier des charges — baobab-scryfall-api-caller

## 1. Objet
La librairie `baobab-scryfall-api-caller` fournit un client Python structuré, typé et testable pour consommer l’API Scryfall, en s’appuyant sur `baobab-web-api-caller`.

## 2. Objectifs
- Encapsuler les appels à l’API Scryfall
- Fournir une API Python claire et typée
- Garantir robustesse et testabilité

## 3. Dépendances
- `baobab-web-api-caller` obligatoire
- Aucun appel HTTP direct

## 4. Périmètre fonctionnel

### Cartes
- Par id, MTGO, Cardmarket, set+numéro
- Recherche (`named`, `search`)
- Collection (max 75)
- Autocomplete
- Random

### Sets
- Liste
- Par code / id

### Rulings
- Par id

### Catalogues
- Accès générique

### Bulk
- Liste + métadonnées + URL

## 5. Architecture
src/baobab_scryfall_api_caller/
- client/
- services/
- models/
- exceptions/
- pagination/

## 6. Design API
```python
client = ScryfallApiCaller(web_api_caller=web_api_caller)
client.cards.get_by_id("id")
```

## 7. Modèles
- Card, Set, Ruling, Catalog, BulkData
- ListResponse[T]

## 8. Pagination
- has_more
- next_page

## 9. Exceptions
- BaobabScryfallApiCallerException
- ScryfallRequestException
- ScryfallNotFoundException
- ScryfallValidationException
- ScryfallRateLimitException

## 10. Règles Scryfall
- Collection ≤ 75
- Autocomplete ≤ 20

## 11. Tests
- 1 fichier par classe
- Couverture ≥ 90%

## 12. Qualité
- black, pylint, mypy, flake8, bandit

## 13. Documentation
- README.md
- CHANGELOG.md
- docs/dev_diary.md

## 14. Version V1
- cartes, sets, rulings, catalogues, bulk
- pagination
- exceptions
- tests

## 15. Critères
- Utilise baobab-web-api-caller
- API typée
- Tests OK
