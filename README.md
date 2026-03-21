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

## Installation

- **Python** : 3.11 ou superieur (`requires-python` dans `pyproject.toml`).
- **Dependance runtime** : `baobab-web-api-caller` (installee automatiquement avec le package).

```bash
pip install baobab-scryfall-api-caller
```

Pour contribuer ou lancer la suite de tests localement :

```bash
pip install -e ".[dev]"
```

## Point d'entree : `ScryfallApiCaller`

Le point d'entree recommande est la classe **`ScryfallApiCaller`** : elle regroupe les
services domaine derriere une facade stable, sans logique metier additionnelle.

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

# Instancier `web_api_caller` selon la documentation de baobab-web-api-caller
# (base URL https://api.scryfall.com, configuration des en-tetes, etc.).
# web_api_caller = ...

client = ScryfallApiCaller(web_api_caller=web_api_caller)

# Acces aux services (voir section « Perimetre par domaine »)
card = client.cards.get_by_id("00000000-0000-0000-0000-000000000000")
sets_page = client.sets.list_sets()
ruling_page = client.rulings.list_for_card_id("00000000-0000-4000-8000-000000000001")
catalog = client.catalogs.get_card_names()
bulk = client.bulk_data.list_bulk_datasets()
```

### Services exposes

| Attribut       | Type               | Role |
|----------------|--------------------|------|
| `client.cards` | `CardsService`     | Cartes |
| `client.sets`  | `SetsService`      | Extensions |
| `client.rulings` | `RulingsService` | Oracle rulings |
| `client.catalogs` | `CatalogsService` | Catalogues de valeurs |
| `client.bulk_data` | `BulkDataService` | Metadonnees bulk |

La propriete en lecture seule `client.web_api_caller` retourne le transport injecte.

### Injection des services (tests ou extensions)

Chaque service peut etre remplace par une instance existante ; le transport
`web_api_caller` reste obligatoire pour documenter le contrat et initialiser les
services non remplaces.

```python
from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.services.cards import CardsService

custom_cards = CardsService(web_api_caller=web_api_caller)

client = ScryfallApiCaller(
    web_api_caller=web_api_caller,
    cards_service=custom_cards,
)
assert client.cards is custom_cards
```

Import direct des services (sans facade) reste possible : `CardsService`,
`SetsService`, etc., depuis les sous-packages `baobab_scryfall_api_caller.services.*`.

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

## Perimetre par domaine (implemente)

- **cards** : `get_by_id`, `get_by_mtgo_id`, `get_by_cardmarket_id`,
  `get_by_set_and_number`, `get_named` (exact ou fuzzy) ;
- **sets** : liste paginee, `get_by_code`, `get_by_id` ;
- **rulings** : `list_for_card_id` (pagination) ;
- **catalogs** : `get_catalog` et helpers (noms, types, artistes, etc.) ;
- **bulk data** : liste des jeux, `get_by_id`, `get_by_type` (metadonnees et URL) ;
- **pagination** : listes Scryfall via `ListResponse` / `ScryfallListResponseParser`.

Les endpoints Scryfall **search**, **collection**, **autocomplete** et **random** sont
prevus dans le cahier des charges V1 mais **ne sont pas** exposes par `CardsService`
dans l'etat actuel du code.

## Etat actuel du projet

- structure de packages source/tests en place ;
- configuration qualite centralisee dans `pyproject.toml` ;
- facade **`ScryfallApiCaller`** et domaines **Cards**, **Sets**, **Rulings**,
  **Catalogs** et **Bulk Data** conformement aux sections detaillees ci-dessus ;
- tests unitaires et couverture conformes aux exigences projet.

## Transport HTTP partage

La logique HTTP generique (GET/POST JSON, detection d'erreurs, extraction de payload)
est centralisee dans `ScryfallHttpClient`. Les clients de domaine (`CardsApiClient`,
`SetsApiClient`, `RulingsApiClient`, `CatalogsApiClient`, `BulkDataApiClient`)
s'appuient sur ce composant pour eviter la duplication tout en conservant une
facade par domaine.

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

## Cards (perimetre actuel)

Disponible via `client.cards` ou `CardsService` :

- `get_by_id(card_id)` ;
- `get_by_mtgo_id(mtgo_id)` ;
- `get_by_cardmarket_id(cardmarket_id)` ;
- `get_by_set_and_number(set_code, collector_number)` ;
- `get_named(exact=...)` ou `get_named(fuzzy=...)`.

Exemple (facade) :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

card_by_id = client.cards.get_by_id("00000000-0000-0000-0000-000000000000")
card_by_mtgo = client.cards.get_by_mtgo_id(12345)
card_by_cm = client.cards.get_by_cardmarket_id(67890)
card_by_set = client.cards.get_by_set_and_number("lea", "233")
card_named = client.cards.get_named(exact="Black Lotus")
```

Contraintes metier appliquees :

- `named` impose exactement un mode (`exact` ou `fuzzy`) ;
- aucune pagination reseau implicite n'est executee automatiquement.

## Sets (perimetre actuel)

Disponible via `client.sets` ou `SetsService` :

- `list_sets(page=...)` : liste paginee (`ListResponse[Set]`) via `GET /sets` ;
- `get_by_code(set_code)` : `GET /sets/{code}` avec validation locale du code ;
- `get_by_id(set_id)` : `GET /sets/{id}` avec validation UUID.

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

all_sets_page = client.sets.list_sets()
neo = client.sets.get_by_code("neo")
one = client.sets.get_by_id("2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f")
```

Contraintes metier appliquees :

- le code set est normalise en minuscules et valide sur un motif alphanumerique court ;
- l'identifiant Scryfall doit etre un UUID valide ;
- les reponses liste utilisent `ScryfallListResponseParser` (pagination `has_more` / `next_page`).

## Rulings (perimetre actuel)

Disponible via `client.rulings` ou `RulingsService` :

- `list_for_card_id(card_id, page=...)` : rulings Oracle pour une carte
  (`GET /cards/{id}/rulings`), reponse `ListResponse[Ruling]` paginee.

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

page = client.rulings.list_for_card_id("00000000-0000-4000-8000-000000000001")
```

Contraintes metier appliquees :

- l'identifiant carte doit etre un UUID Scryfall valide ;
- le parametre `page` est optionnel et valide comme entier strictement positif ;
- les reponses liste sont parsees via `ScryfallListResponseParser`.

## Catalogs (perimetre actuel)

Disponible via `client.catalogs` ou `CatalogsService` :

- `get_catalog(catalog_key)` : acces generique (`GET /catalog/{catalog_key}`) ;
- helpers : `get_card_names`, `get_creature_types`, `get_land_types`,
  `get_card_types`, `get_artist_names` (deleguent au generique).

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

names = client.catalogs.get_card_names()
custom = client.catalogs.get_catalog("keyword-abilities")
```

Contraintes metier appliquees :

- la cle catalogue est normalisee en minuscules et validee (motif kebab-case,
  longueur bornee) ;
- le mapper exige `object: catalog`, `uri`, `total_values` entier positif ou
  nul, et `data` comme liste de chaines (liste vide acceptee).

## Bulk Data (perimetre actuel)

Disponible via `client.bulk_data` ou `BulkDataService` :

- `list_bulk_datasets()` : liste des jeux (`GET /bulk-data`, `ListResponse[BulkData]`) ;
- `get_by_id(bulk_data_id)` : metadonnees par UUID (`GET /bulk-data/{id}`) ;
- `get_by_type(bulk_type)` : metadonnees par type d'URL kebab-case
  (`GET /bulk-data/{type}`, ex. ``oracle-cards``).

Aucun telechargement de fichier n'est effectue en V1 : seule l'URL
(`download_uri`) et les metadonnees sont exposees.

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

all_datasets = client.bulk_data.list_bulk_datasets()
one = client.bulk_data.get_by_type("oracle-cards")
by_uuid = client.bulk_data.get_by_id("922288cb-4bef-45e1-bb30-0c2bd3d3534f")
```

Contraintes metier appliquees :

- validation UUID pour `get_by_id`, motif kebab-case pour `get_by_type` ;
- coherence : `download_uri` en URL absolue HTTP(S), `size` strictement positif
  (sinon `ScryfallBulkDataException`) ;
- payloads `object: bulk_data` attendus pour chaque jeu.
