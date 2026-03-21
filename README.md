# baobab-scryfall-api-caller

## But de la librairie

`baobab-scryfall-api-caller` est une librairie Python qui fournit une API orientee metier
pour consommer l'API Web Scryfall (**perimetre V1** documente dans `docs/01_specifications.md`
et suivi dans `docs/V1_compliance.md`).

La librairie encapsule la logique specifique a Scryfall :

- construction des routes metier ;
- validation des entrees ;
- serialisation des parametres ;
- mapping des reponses ;
- gestion des erreurs metier ;
- gestion des reponses paginees.

## Installation

- **Python** : 3.11 ou superieur (`requires-python` dans `pyproject.toml`).
- **Dependance runtime** : `baobab-web-api-caller` (contrainte de version bornee dans
  `pyproject.toml`, installee automatiquement avec le package).

```bash
pip install baobab-scryfall-api-caller
```

Pour contribuer ou lancer la suite de tests localement :

```bash
pip install -e ".[dev]"
```

### `baobab-web-api-caller` : installation pour les tests d'integration live

Les tests du dossier **`tests/integration`** chargent le package Python
**`baobab_web_api_caller`** (meme chaine que la production : `ServiceConfig` →
transport → `ScryfallApiCaller`). La dependance doit donc etre **importable** via
l'installation normale (**pip**), sans bricolage de `PYTHONPATH` ni de `sys.path`.

- **Wheel PyPI** : depuis la racine de ce depot, `python -m pip install -e ".[dev]"` ;
  pip installe `baobab-web-api-caller` selon `pyproject.toml` (`>=0.1.0,<2.0.0`).
- **Editable local** : developpement conjoint — **1)** `python -m pip install -e`
  `/chemin/vers/baobab-web-api-caller` **2)** puis `python -m pip install -e ".[dev]"`
  ici ; pip reutilise l'installation locale si la version est compatible.
- **Wheel fichier** : `python -m pip install chemin/vers/baobab_web_api_caller-*.whl`
  puis `python -m pip install -e ".[dev]"` ; details dans `docs/ci_integration_tests.md`.

**Verifier l'installation** (aucun hack de chemin) :

```bash
python -c "import importlib.metadata as m; print(m.version('baobab-web-api-caller'))"
python -c "import baobab_web_api_caller; print('import baobab_web_api_caller: ok')"
```

**Lancer les tests live** (Internet requis) :

```bash
python -m pytest tests/integration --no-cov -m integration
```

**Cibles Makefile** (optionnel ; sous Unix ou Git Bash : `make`) :

- `make install-dev` — installe ce projet en editable avec `[dev]` (meme prerequis
  que les tests d'integration) ;
- `make install-integration-deps` — alias de `install-dev` (nom explicite pour CI
  ou scripts) ;
- `make test-integration` — execute `pytest tests/integration --no-cov -m integration`.

Recettes CI detaillees (PyPI, wheel artefact, editable) : **`docs/ci_integration_tests.md`**.

## Point d'entree : `ScryfallApiCaller`

Le point d'entree recommande est la classe **`ScryfallApiCaller`** : elle regroupe les
services domaine derriere une facade stable, sans logique metier additionnelle.

```python
from baobab_web_api_caller import (
    BaobabServiceCaller,
    HttpTransportCaller,
    RequestsSessionFactory,
    ServiceConfig,
)
from baobab_scryfall_api_caller import ScryfallApiCaller

service_config = ServiceConfig(base_url="https://api.scryfall.com")
transport = HttpTransportCaller.from_service_config(
    service_config=service_config,
    session_factory=RequestsSessionFactory(),
)
web_api_caller = BaobabServiceCaller(
    service_config=service_config,
    web_api_caller=transport,
)

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

### Version et exports publics (racine)

- **Version** : `0.1.0` (premiere release ; perimetre fonctionnel V1). Acces programme :
  `from baobab_scryfall_api_caller import __version__`.
- **`__all__`** : `ScryfallApiCaller`, `WebApiTransportProtocol`, `__version__`.
- Pour les composants clients avances (ex. tests ou extension) :
  `from baobab_scryfall_api_caller.client import ScryfallHttpClient` (non reexportes
  a la racine du package).

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

La couche de transport HTTP repose **exclusivement** sur `baobab-web-api-caller`
(PyPI). Aucune requete ne doit utiliser `requests`, `urllib` ou un client HTTP
direct dans ce depot : tout passe par l'instance injectee (`BaobabServiceCaller`
+ `HttpTransportCaller`, ou double de test respectant `WebApiTransportProtocol`).

`ScryfallHttpClient` adapte les appels metier (routes Scryfall, query dict) vers
les signatures `get(path=..., query_params=..., headers=...)` et
`post(..., json_body=...)` de `BaobabServiceCaller`, et extrait les JSON depuis
`BaobabResponse.json_data`.

Regles structurantes :

- aucun appel HTTP direct hors de `baobab-web-api-caller` ;
- aucune duplication de logique HTTP generique ;
- separation stricte entre transport et logique metier Scryfall ;
- injection unique : pas de singleton global pour le transport.

## Principes d'architecture

- architecture orientee classes ;
- une classe par fichier ;
- separation claire entre `src/`, `tests/` et `docs/` ;
- arborescence miroir entre code source et tests ;
- API publique typee et documentee ;
- exceptions projet dediees avec racine commune.

## Perimetre par domaine (implemente)

- **cards** : `get_by_id`, `get_by_mtgo_id`, `get_by_cardmarket_id`,
  `get_by_set_and_number`, `get_named` (exact ou fuzzy), `search`, `autocomplete`,
  `random`, `get_collection` ;
- **sets** : liste paginee, `get_by_code`, `get_by_id` ;
- **rulings** : `list_for_card_id` (pagination) ;
- **catalogs** : `get_catalog` et helpers (noms, types, artistes, etc.) ;
- **bulk data** : liste des jeux, `get_by_id`, `get_by_type` (metadonnees et URL) ;
- **pagination** : listes Scryfall via `ListResponse` / `ScryfallListResponseParser`.

Les endpoints Scryfall **search**, **collection**, **autocomplete** et **random** sont
exposes par `CardsService` (voir section Cards ci-dessous).

## Etat actuel du projet

- **Release V1** : version **0.1.0** ; fonctionnalites prevues au cahier des charges V1
  sont implementees (synthese : `docs/V1_compliance.md`). La branche de stabilisation
  a verifie l'alignement doc / code, la qualite complete et une couverture elevee
  (~97 %) avant tag / publication PyPI.
- Structure `src/` / `tests/` / `docs/` ; tests en arborescence miroir.
- Facade **`ScryfallApiCaller`** et domaines **Cards**, **Sets**, **Rulings**,
  **Catalogs**, **Bulk Data** comme decrit ci-dessous.
- Qualite : outils configures dans `pyproject.toml` (executes localement ou dans votre
  pipeline ; voir section qualite ci-dessous).
- Couverture de tests : seuil minimal **90 %** ; objectif atteint au-dela sur la branche
  RC (rapport sous `docs/tests/coverage/`).

## Limitations connues et release readiness

- **Transport** : la librairie n'instancie pas `baobab-web-api-caller` a votre place ;
  vous devez composer `ServiceConfig`, `HttpTransportCaller`, `BaobabServiceCaller`
  (ou equivalent conforme a `WebApiTransportProtocol`) comme dans l'exemple du
  README.
- **Bulk data** : pas de telechargement automatique des fichiers export ; seules les
  metadonnees et l'URL (`download_uri`) sont exposees (hors scope V1, voir specifications).
- **Tests d'integration** : une suite **optionnelle** (`tests/integration`, marqueur
  `integration`) appelle l'API reelle Scryfall via `baobab-web-api-caller` ; a lancer
  a la demande (reseau requis). Les tests **unitaires** restent par defaut sans reseau
  (`pytest` exclut ce dossier ; voir section qualite).
- **Dependance `baobab-web-api-caller`** : version semver bornee dans `pyproject.toml` ;
  modes d'installation (wheel PyPI, editable, wheel fichier) : section **Installation**
  ci-dessus et `docs/ci_integration_tests.md`. Les tests unitaires verifient la
  presence du **distribution name** sans importer le package top-level ; les tests
  d'integration exigent un import reel de `baobab_web_api_caller`.

## Packaging et typage (PEP 621 / PEP 561)

- **Distribution** : `pyproject.toml` (metadonnees, dependances, outils qualite).
- **Version** : `0.1.0` (champ `project.version`, dupliquee par `__version__` dans le
  package racine ; doit rester alignee).
- **Classifiers / keywords** : declares dans `pyproject.toml` pour indexation PyPI
  (Python supporte : 3.11+).
- **Marqueur de typage** : `py.typed` inclus dans le wheel via
  `[tool.setuptools.package-data]` pour les consommateurs `mypy` / IDE.
- **Installation editable** : `pip install -e ".[dev]"` installe les dependances
  de developpement (tests, formatage, analyse statique).

## Qualite et couverture de tests

Les commandes suivantes sont attendues vertes avant fusion :

- `python -m black src tests`
- `python -m black --check src tests` (verification sans modification)
- `python -m pylint src/baobab_scryfall_api_caller --fail-under=10`
- `python -m mypy src/baobab_scryfall_api_caller`
- `python -m flake8 src tests`
- `python -m bandit -c pyproject.toml -r src tests`
- `python -m pytest tests/` ou `python -m pytest` : **tests unitaires uniquement**
  (dossier `tests/integration` ignore dans la configuration pytest par defaut) avec
  `pytest-cov` et seuil 90 %.

Les rapports de couverture (HTML, XML, JSON) sont generes sous `docs/tests/coverage/`
(configure dans `pyproject.toml` ; fichiers generes listes dans `.gitignore`).

### Tests d'integration reseau (Scryfall)

Le dossier **`tests/integration`** contient des tests marques **`@pytest.mark.integration`**
qui utilisent la **meme chaine** que le README : `ServiceConfig` → `HttpTransportCaller` →
`BaobabServiceCaller` → **`ScryfallApiCaller`**, ciblant **`https://api.scryfall.com`**.

- **Objectif** : valider transport, mapping et exceptions sur reponses reelles (hors mocks).
- **Debit et HTTP** : la configuration est centralisee dans
  `tests/integration/live_transport_config.py` et injectee via ``ServiceConfig`` de
  `baobab-web-api-caller` :
  - **Throttling** : environ **6 requetes/seconde** en moyenne (intervalle minimal **1/6 s**
    entre deux appels, via `RateLimitPolicy`), volontairement dans la zone conservative
    5–8 req/s par rapport aux limites Scryfall.
  - **En-tetes par defaut** : `User-Agent` explicite dedie aux tests d'integration
    (nom du projet + URL du depot) et `Accept: application/json; charset=utf-8`.
  Tous les tests live passent par la fixture ``live_scryfall_client`` qui applique cette
  configuration au transport (pas de reconstruction par test).
- **Contraintes** : acces Internet ; respect des [lignes directrices Scryfall](https://scryfall.com/docs/api)
  (pas de secrets ni credentials).
- **Execution** :
  - uniquement integration : `python -m pytest tests/integration --no-cov`
    (le `--no-cov` evite d'appliquer le seuil de couverture 90 % aux seuls tests
    reseau, qui feraient sinon chuter le rapport global).
  - filtre sur le marqueur : `python -m pytest tests/integration -m integration --no-cov`
- **Couverture** : les runs **unitaires** (`pytest` / `pytest tests/`) calculent la
  couverture avec `pytest-cov`. Les tests d'integration peuvent etre mesures avec
  `python -m pytest tests/integration --cov=baobab_scryfall_api_caller` si besoin.
- **Donnees de test** : identifiants et requetes stables dans
  `tests/integration/scryfall_live_constants.py` ; politique HTTP (debit + headers) dans
  `tests/integration/live_transport_config.py`.

## Conformite cahier des charges (V1)

Une **matrice de conformite** detaillee (exigences structurelles, synthese domaine
Cards V1, recommandations post-V1) est maintenue dans `docs/V1_compliance.md`.

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

## Cards (V1)

Disponible via `client.cards` ou `CardsService`. Toutes les operations V1 Scryfall
prevues pour les cartes (acces unitaires, named, search, autocomplete, random,
collection) sont exposees.

| Methode | Retour | Endpoint HTTP |
|---------|--------|----------------|
| `get_by_id(card_id)` | `Card` | `GET /cards/{id}` |
| `get_by_mtgo_id(mtgo_id)` | `Card` | `GET /cards/mtgo/{id}` |
| `get_by_cardmarket_id(cardmarket_id)` | `Card` | `GET /cards/cardmarket/{id}` |
| `get_by_set_and_number(set_code, collector_number)` | `Card` | `GET /cards/{set}/{collector_number}` |
| `get_named(exact=...)` ou `get_named(fuzzy=...)` | `Card` | `GET /cards/named` |
| `search(q=..., page=...)` | `ListResponse[Card]` | `GET /cards/search` |
| `autocomplete(q=...)` | `AutocompleteResult` | `GET /cards/autocomplete` |
| `random(q=...)` | `Card` | `GET /cards/random` |
| `get_collection(identifiers=...)` | `CardCollectionResult` | `POST /cards/collection` |

**Erreurs** : les erreurs de validation locale levent `ScryfallValidationException` ;
les erreurs HTTP / transport, les erreurs de format de payload JSON et les erreurs
Scryfall (`object: error`) sont traduites via `ScryfallHttpClient` en exceptions
metier (`ScryfallRequestException`, `ScryfallNotFoundException`, etc.) et la
`BaobabScryfallApiCallerException` racine.

Exemple (facade) :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.models.cards import CardCollectionIdentifier

client = ScryfallApiCaller(web_api_caller=web_api_caller)

card_by_id = client.cards.get_by_id("00000000-0000-0000-0000-000000000000")
card_by_mtgo = client.cards.get_by_mtgo_id(12345)
card_by_cm = client.cards.get_by_cardmarket_id(67890)
card_by_set = client.cards.get_by_set_and_number("lea", "233")
card_named = client.cards.get_named(exact="Black Lotus")

search_page = client.cards.search(q="type:creature cmc=3")
suggestions = client.cards.autocomplete(q="light")
lucky = client.cards.random()
lucky_filtered = client.cards.random(q="type:creature")

batch = client.cards.get_collection(
    identifiers=[
        CardCollectionIdentifier(id="00000000-0000-4000-8000-000000000001"),
        CardCollectionIdentifier(set_code="neo", collector_number="1"),
    ]
)
```

Contraintes et comportements :

- **Champs texte** (`card_id`, codes set, `exact` / `fuzzy`, etc.) : non vides apres
  `strip` ; le code d'extension est en outre passe en minuscules dans l'URL.
- **named** : exactement un seul parmi `exact` ou `fuzzy`.
- **search / autocomplete / random** : `q` doit etre une chaine non vide (test de vide
  apres `strip`) ; le DSL transmis a Scryfall n'est pas reecrit.
- **search** : `page` optionnel (entier >= 1) ; reponse avec `metadata` (`has_more`,
  `next_page`, `total_cards`, `warnings`) via `ScryfallListResponseParser` ; aucune
  pagination reseau supplementaire n'est declenchee automatiquement.
- **get_collection** : sequence non vide, au plus `MAX_CARD_COLLECTION_IDENTIFIERS` (75)
  `CardCollectionIdentifier` ; un schema par identifiant (voir modele) ; `not_found`
  liste les identifiants non resolus tels que renvoyes par Scryfall.

## Sets (perimetre actuel)

Disponible via `client.sets` ou `SetsService` :

- `list_sets(*, page=...)` : liste paginee (`ListResponse[Set]`) via `GET /sets` ;
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
