# baobab-scryfall-api-caller

## But de la librairie

`baobab-scryfall-api-caller` est une librairie Python qui fournit une API orientee metier
pour consommer l'API Web Scryfall.

La librairie encapsule la logique specifique a Scryfall :

- construction des routes metier ;
- validation des entrees ;
- serialisation des parametres ;
- mapping des reponses ;
- gestion des erreurs metier ;
- gestion des reponses paginees.

## Dependance a baobab-web-api-caller

La couche de transport HTTP repose exclusivement sur `baobab-web-api-caller`.

Regles structurantes :

- aucun appel HTTP direct hors de `baobab-web-api-caller` ;
- aucune duplication de logique HTTP generique ;
- separation stricte entre transport et logique metier Scryfall.

## Principes d'architecture

- architecture orientee classes ;
- une classe par fichier ;
- separation claire entre `src/`, `tests/` et `docs/` ;
- arborescence miroir entre code source et tests ;
- API publique typee et documentee ;
- exceptions projet dediees avec racine commune.

## Perimetre V1 (cible)

- cards : get by id, named, search, collection, autocomplete, random ;
- sets : listage et recuperation ;
- rulings : recuperation par identifiant ;
- catalogs : acces generique et helpers principaux ;
- bulk data : liste et metadonnees ;
- pagination Scryfall.

## Etat actuel du projet

- structure de packages source/tests en place ;
- configuration qualite centralisee dans `pyproject.toml` ;
- domaines **Cards**, **Sets** et **Rulings** implementes sur le perimetre V1 decrit ci-dessous ;
- tests unitaires et couverture conformes aux exigences projet.

## Transport HTTP partage

La logique HTTP generique (GET/POST JSON, detection d'erreurs, extraction de payload)
est centralisee dans `ScryfallHttpClient`. Les clients de domaine (`CardsApiClient`,
`SetsApiClient`, `RulingsApiClient`) s'appuient sur ce composant pour eviter la
duplication tout en conservant une facade par domaine.

## Couche d'exceptions et traduction d'erreurs

Le projet fournit une hierarchie d'exceptions metier prete pour les futurs services :

- `BaobabScryfallApiCallerException` (racine projet) ;
- `ScryfallRequestException` ;
- `ScryfallNotFoundException` ;
- `ScryfallValidationException` ;
- `ScryfallRateLimitException` ;
- `ScryfallResponseFormatException` ;
- `ScryfallPaginationException` ;
- `ScryfallBulkDataException`.

Le composant `ScryfallErrorTranslator` traduit les erreurs transport/HTTP/validation/format
en exceptions metier, sans couplage fort a une implementation interne du transport HTTP.

## Modeles partages et pagination

Le projet inclut un socle commun pour les reponses de type liste :

- `ListResponse[T]` pour porter les elements typables ;
- `PaginationMetadata` pour `has_more`, `next_page`, `total_cards` et `warnings` ;
- `ScryfallWarning` pour normaliser les avertissements ;
- `ScryfallListResponseValidator` et `ScryfallListResponseParser` pour valider/parser
  les payloads de liste ;
- `ScryfallPage[T]` pour manipuler une page locale sans iteration reseau automatique.

## Cards core (perimetre actuel)

La premiere tranche du domaine Cards est disponible via `CardsService` :

- `get_by_id(card_id)` ;
- `get_by_mtgo_id(mtgo_id)` ;
- `get_by_cardmarket_id(cardmarket_id)` ;
- `get_by_set_and_number(set_code, collector_number)` ;
- `get_named(exact=...)` ou `get_named(fuzzy=...)`.

Exemple d'usage :

```python
from baobab_scryfall_api_caller.services.cards import CardsService

cards = CardsService(web_api_caller=web_api_caller)

card_by_id = cards.get_by_id("00000000-0000-0000-0000-000000000000")
card_by_mtgo = cards.get_by_mtgo_id(12345)
card_by_cm = cards.get_by_cardmarket_id(67890)
card_by_set = cards.get_by_set_and_number("lea", "233")
card_named = cards.get_named(exact="Black Lotus")
```

Contraintes metier appliquees :

- `named` impose exactement un mode (`exact` ou `fuzzy`) ;
- aucune pagination reseau implicite n'est executee automatiquement.

## Sets (perimetre actuel)

Le domaine Sets est disponible via `SetsService` :

- `list_sets(page=...)` : liste paginee (`ListResponse[Set]`) via `GET /sets` ;
- `get_by_code(set_code)` : `GET /sets/{code}` avec validation locale du code ;
- `get_by_id(set_id)` : `GET /sets/{id}` avec validation UUID.

Exemple d'usage :

```python
from baobab_scryfall_api_caller.services.sets import SetsService

sets = SetsService(web_api_caller=web_api_caller)

all_sets_page = sets.list_sets()
neo = sets.get_by_code("neo")
one = sets.get_by_id("2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f")
```

Contraintes metier appliquees :

- le code set est normalise en minuscules et valide sur un motif alphanumerique court ;
- l'identifiant Scryfall doit etre un UUID valide ;
- les reponses liste utilisent `ScryfallListResponseParser` (pagination `has_more` / `next_page`).

## Rulings (perimetre actuel)

Le domaine Rulings est disponible via `RulingsService` :

- `list_for_card_id(card_id, page=...)` : rulings Oracle pour une carte
  (`GET /cards/{id}/rulings`), reponse `ListResponse[Ruling]` paginee.

Exemple d'usage :

```python
from baobab_scryfall_api_caller.services.rulings import RulingsService

rulings = RulingsService(web_api_caller=web_api_caller)

page = rulings.list_for_card_id("00000000-0000-4000-8000-000000000001")
```

Contraintes metier appliquees :

- l'identifiant carte doit etre un UUID Scryfall valide ;
- le parametre `page` est optionnel et valide comme entier strictement positif ;
- les reponses liste sont parsees via `ScryfallListResponseParser`.
