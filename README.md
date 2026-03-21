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
- `make test` / `make test-unit` — `pytest` avec couverture et seuil 90 % (defaut) ;
- `make test-integration` — `pytest tests/integration --no-cov -m integration`.

Recettes CI detaillees (PyPI, wheel artefact, editable) : **`docs/ci_integration_tests.md`**.

Guide d'integration live (marqueur, `--no-cov`, politique HTTP) :
**`docs/live_integration_tests.md`**. Scripts : `scripts/run_live_integration_tests.ps1` /
`scripts/run_live_integration_tests.sh` (equivalent `make test-integration`).

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

## Cache optionnel (reponses GET)

**Desactive par defaut.** La librairie peut memoriser en **memoire processus** les
payloads JSON de certains **GET** reussis, pour reduire les appels reseau repetitifs
(catalogues, sets, bulk data, rulings par carte, carte par UUID). Aucune persistance
disque ni cache distribue : uniquement un socle injectable et explicite.

- **Types** : `JsonResponseCache` (protocole), `InMemoryJsonCache`, predicat
  `default_cacheable_get`, cle stable `make_get_cache_key` — module
  `baobab_scryfall_api_caller.cache`.
- **Facade** : `ScryfallApiCaller(web_api_caller=..., response_cache=InMemoryJsonCache())`.
  Le meme objet cache est partage par les services par defaut. Sans instance de cache,
  le comportement reste identique aux versions precedentes.
- **Filtre** : `cacheable_get_predicate` optionnel ; si absent et qu'un cache est fourni,
  le predicat par defaut s'applique (exclut notamment `search`, `random`, `autocomplete`).
- Les **erreurs HTTP** et les reponses `object: error` ne sont **pas** mises en cache.
- Les **POST** (`collection`, etc.) ne passent pas par ce mecanisme.

```python
from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.cache import InMemoryJsonCache

client = ScryfallApiCaller(
    web_api_caller=web_api_caller,
    response_cache=InMemoryJsonCache(),
)
```

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
- **sets** : liste paginee, `get_by_code`, `get_by_id`, `list_cards_in_set` /
  `list_cards_in_set_by_id` ;
- **rulings** : `list_for_card_id`, multiverse / MTGO / Arena (pagination) ;
- **catalogs** : `get_catalog` et helpers (noms, types, artistes, etc.) ;
- **bulk data** : liste des jeux, `get_by_id`, `get_by_type`, telechargement optionnel
  via `BulkDatasetDownloader` ;
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
- **Tests d'integration** : suite **optionnelle** (`tests/integration`, marqueur
  `integration`) contre l'API reelle ; a lancer a la demande (reseau requis).
  Reference : `docs/live_integration_tests.md`. Les tests **unitaires** restent par
  defaut sans reseau (`pytest` ignore ce dossier ; voir section qualite).
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

### Pytest : unites vs integration (couverture)

- **Validation standard** (CI locale, pre-merge) : `python -m pytest` ou
  `python -m pytest tests/` — **couverture active** (`pytest-cov`, seuil 90 % dans
  `pyproject.toml`) ; `tests/integration` est **ignore** par defaut.
- **Uniquement tests d'integration live** :
  `python -m pytest tests/integration --no-cov -m integration` — **sans** couverture :
  sans `--no-cov`, les `addopts` mesurent tout `src/` et appliquent le seuil global au
  seul code execute par ces tests (souvent ~70 %), donc **echec** de `cov-fail-under`
  sans lien avec la regression sur les unites.
- **Confort** : `make test` / `make test-unit` (idem `pytest`) ; `make test-integration`
  (meme ligne que l'integration ci-dessus).

Le seuil **90 %** reste exige pour les **runs habituels** ; couper la couverture pour la
sous-suite reseau **ne reduit pas** cette exigence sur le package dans le flux standard.

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
- **Execution** (obligatoire : `--no-cov` si vous ne lancez que ce dossier) :
  - `python -m pytest tests/integration --no-cov -m integration`
    (sans `--no-cov`, les options par defaut mesurent tout `src/` et appliquent le
    seuil 90 % a un **sous-ensemble** de branches, ce qui fait echouer inutilement le
    run ; voir tableau **Pytest : unites vs integration** ci-dessus).
  - `make test-integration` : meme commande.
- **Couverture** : le seuil **90 %** s'applique aux runs **unitaires** standards
  (tableau ci-dessus). Une mesure ad hoc sur `tests/integration` avec coverage
  doit eviter d'heriter betement des `addopts` globaux (sinon meme piege que sans
  `--no-cov`).
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

### Ergonomie : `ListResponse` et pages suivantes

Sur une page deja obtenue (ex. `CardsService.search`, `SetsService.list_sets`) :

- **Iteration** : `for card in page:` parcourt les elements de la **page courante** ;
  `len(page)`, `bool(page)`, `page.is_empty`, `page.count` ;
- **Alias** : `page.items` est un alias de `page.data` ;
- **Metadonnees** : `page.has_more`, `page.next_page`, `page.total_cards`, `page.warnings` ;
- **Representation** : `repr(page)` resume taille et pagination sans lister tous les objets.

Pour enchainer **plusieurs pages** via les URL `next_page` de Scryfall, le module
`baobab_scryfall_api_caller.pagination` expose des helpers **explicites** qui ne
declenchent aucun GET tant que vous ne fournissez pas `fetch_next` :

- `iter_list_pages(first, fetch_next=..., max_pages=...)` : yield chaque `ListResponse` ;
- `iter_list_items(first, fetch_next=..., max_pages=...)` : yield tous les elements
  en suivant les pages.

`fetch_next(url_absolue)` doit executer le GET via votre transport
(`ScryfallHttpClient` / `baobab-web-api-caller`), parser la reponse avec le meme
`ScryfallListResponseParser` et le mapper du domaine. Aucun parcours reseau implicite
n'est effectue sans cet appel.

Exemple minimal (pseudo-code) :

```python
from baobab_scryfall_api_caller.pagination import iter_list_items

def fetch_next(url: str):
    payload = http.get(route=url, params=None)  # URL absolue Scryfall
    return parser.parse(raw_response=payload, item_mapper=card_mapper.map_card)

first = client.cards.search(q="type:creature")
for card in iter_list_items(first, fetch_next=fetch_next, max_pages=5):
    ...
```

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
| `search(q=..., page=...)` ou `search(query=..., page=...)` | `ListResponse[Card]` | `GET /cards/search` |
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
from baobab_scryfall_api_caller.models.cards import CardCollectionIdentifier, CardSearchQuery

client = ScryfallApiCaller(web_api_caller=web_api_caller)

card_by_id = client.cards.get_by_id("00000000-0000-0000-0000-000000000000")
card_by_mtgo = client.cards.get_by_mtgo_id(12345)
card_by_cm = client.cards.get_by_cardmarket_id(67890)
card_by_set = client.cards.get_by_set_and_number("lea", "233")
card_named = client.cards.get_named(exact="Black Lotus")

search_page = client.cards.search(q="t:creature cmc=3")
same_as_builder = client.cards.search(
    query=CardSearchQuery().type_line("creature").cmc(3),
)
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
- **search** : fournir **exactement un** parmi `q` (DSL brut Scryfall) ou `query`
  (`CardSearchQuery` assemble en chaine puis envoyee comme `q`) ; ne pas combiner les deux.
- **autocomplete / random** : `q` doit etre une chaine non vide (test de vide apres
  `strip`) ; le DSL transmis a Scryfall n'est pas reecrit pour ces methodes.
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
- `get_by_id(set_id)` : `GET /sets/{id}` avec validation UUID ;
- `list_cards_in_set(set_code, *, page=...)` : cartes d'un set par code
  (`GET /sets/{code}/cards`, `ListResponse[Card]`) ;
- `list_cards_in_set_by_id(set_id, *, page=...)` : memes cartes adressees par UUID de set
  (`GET /sets/{id}/cards`).

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

all_sets_page = client.sets.list_sets()
neo = client.sets.get_by_code("neo")
one = client.sets.get_by_id("2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f")
cards_page = client.sets.list_cards_in_set("neo")
```

Contraintes metier appliquees :

- le code set est normalise en minuscules et valide sur un motif alphanumerique court ;
- l'identifiant Scryfall doit etre un UUID valide ;
- les reponses liste utilisent `ScryfallListResponseParser` (pagination `has_more` / `next_page`) ;
- les listes de cartes sont mappees via `CardMapper` (injection optionnelle au constructeur).

## Rulings (perimetre actuel)

Disponible via `client.rulings` ou `RulingsService` :

- `list_for_card_id(card_id, page=...)` : rulings Oracle pour une carte
  (`GET /cards/{id}/rulings`), reponse `ListResponse[Ruling]` paginee ;
- `list_for_card_multiverse_id(multiverse_id, page=...)` :
  `GET /cards/multiverse/{id}/rulings` ;
- `list_for_card_mtgo_id(mtgo_id, page=...)` : `GET /cards/mtgo/{id}/rulings` ;
- `list_for_card_arena_id(arena_id, page=...)` : `GET /cards/arena/{id}/rulings`.

Exemple :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

page = client.rulings.list_for_card_id("00000000-0000-4000-8000-000000000001")
by_mv = client.rulings.list_for_card_multiverse_id(123456)
```

Contraintes metier appliquees :

- l'identifiant carte (`list_for_card_id`) doit etre un UUID Scryfall valide ;
- multiverse id et mtgo id : entiers strictement positifs ; arena id : texte non vide ;
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

**Telechargement de fichier (optionnel)** : la librairie ne declenche aucun GET binaire
tant que vous n'injectez pas un `BulkDatasetDownloader`
(`baobab_scryfall_api_caller.services.bulk_data`).
Le telechargement repose sur `BulkFileDownloader` de `baobab-web-api-caller`
(meme dependance que le transport JSON) : streaming vers disque,
fichier temporaire ``.part`` puis renommage, pas d'HTTP direct dans ce depot.

- Construire un downloader : `BulkDatasetDownloader(session_factory=RequestsSessionFactory())`
  (optionnellement `default_headers=` alignes sur votre `ServiceConfig` pour
  `User-Agent` / politique Scryfall).
- Passer ``bulk_dataset_downloader=...`` a ``ScryfallApiCaller`` ou ``BulkDataService``.
- Appeler ``download_bulk_dataset(bulk_data=..., destination_path=Path("/chemin/fichier.json"))``,
  ``download_bulk_dataset_by_type("oracle-cards", destination_path=...)`` ou
  ``download_bulk_dataset_by_id(...)``.
- ``overwrite=False`` (defaut) : refuser d'ecraser un fichier deja present ; passer
  ``overwrite=True`` pour remplacer explicitement.

Exemple (metadonnees seules) :

```python
from baobab_scryfall_api_caller import ScryfallApiCaller

client = ScryfallApiCaller(web_api_caller=web_api_caller)

all_datasets = client.bulk_data.list_bulk_datasets()
one = client.bulk_data.get_by_type("oracle-cards")
by_uuid = client.bulk_data.get_by_id("922288cb-4bef-45e1-bb30-0c2bd3d3534f")
```

Exemple (telechargement, avec injection) :

```python
from pathlib import Path

from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.services.bulk_data import BulkDatasetDownloader

downloader = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
client = ScryfallApiCaller(web_api_caller=web_api_caller, bulk_dataset_downloader=downloader)

meta = client.bulk_data.get_by_type("oracle-cards")
result = client.bulk_data.download_bulk_dataset(
    bulk_data=meta,
    destination_path=Path("./oracle-cards.json"),
    overwrite=False,
)
# result.path : fichier ecrit ; result.bulk_data : metadonnees
```

Contraintes metier appliquees :

- validation UUID pour `get_by_id`, motif kebab-case pour `get_by_type` ;
- coherence : `download_uri` en URL absolue HTTP(S), `size` strictement positif
  (sinon `ScryfallBulkDataException`) ;
- payloads `object: bulk_data` attendus pour chaque jeu ;
- destination de telechargement : chemin **fichier** (pas un repertoire seul) ;
  erreurs HTTP / transport reseau : `ScryfallRequestException` ou `ScryfallBulkDataException`
  selon le cas (voir docstrings).
