## 2026-03-24 10:00:00

### Modifications
- **Modeles** : `ImageUris`, champs supplementaires sur `Card` / `CardFace`, `ruling_id` ;
  coercitions partagees ; tests ; README (section modeles) ; CHANGELOG.

### Buts
- Refleter davantage les payloads Scryfall sans casser les usages (champs optionnels en fin de dataclass).

### Impact
- Les services existants retournent des objets plus riches lorsque l'API fournit les champs.

## 2026-03-23 20:30:00

### Modifications
- **Rulings** : multiverse / MTGO / Arena ; **Sets** : cartes par code ou UUID de set ;
  cache : exclusion `/sets/.../cards` ; README, CHANGELOG, `V1_compliance.md`.

### Buts
- Couvrir des acces Scryfall utiles sans dupliquer le domaine Cards.

### Impact
- API existante preservee ; `default_cacheable_get` affiné pour les listes de cartes d'un set.

## 2026-03-23 18:00:00

### Modifications
- **Bulk download** : `BulkDatasetDownloader`, `bulk_download_uri`, `BulkDownloadResult` ;
  `BulkDataService` + `ScryfallApiCaller` ; tests ; README / CHANGELOG.

### Buts
- Telechargement fichier bulk via la meme dependance `baobab-web-api-caller`, sans HTTP direct
  dans ce depot ; API explicite et `overwrite` clair.

### Impact
- Sans `bulk_dataset_downloader`, comportement identique pour les seuls appels metadonnees.

## 2026-03-23 12:00:00

### Modifications
- **Cache GET optionnel** : package `cache` (`JsonResponseCache`, `InMemoryJsonCache`,
  `default_cacheable_get`, `make_get_cache_key`) ; `ScryfallHttpClient` + services +
  `ScryfallApiCaller` ; tests ; README / CHANGELOG.

### Buts
- Socle simple, injectable, sans persistance ni reseau implicite ; desactive par defaut.

### Impact
- Meme API si `response_cache` absent ; consommateurs avances peuvent reduire les allers-retours.

## 2026-03-22 23:45:00

### Modifications
- **CardSearchQuery** : assembleur optionnel pour `GET /cards/search` ; `search(q=...)`
  ou `search(query=...)` exclusif ; validations legeres ; README + CHANGELOG + tests.

### Buts
- Ergonomie sans remplacer le DSL brut ; pas de reecriture semantique cote client.

### Impact
- API publique etendue de maniere compatible ; imports depuis `models.cards`.

## 2026-03-22 22:30:00

### Modifications
- **Ergonomie pagination** : `ListResponse` et `ScryfallPage` (iteration, `items`,
  `is_empty`, `count`, `repr`, raccourcis metadata) ; `iter_list_pages` /
  `iter_list_items` avec `fetch_next` explicite ; README, CHANGELOG, tests.

### Buts
- Usage naturel des pages sans requetes reseau implicites ; API publique des champs
  `data` / `metadata` preservee.

### Impact
- Consommateurs peuvent parcourir une page avec `for x in response` ou enchainer
  les pages via un callable documente.

## 2026-03-22 20:00:00

### Modifications
- **Durcissement integration live** : `build_live_scryfall_client()` dans
  `live_transport_config.py` ; `conftest` simplifie ; scenarios supplementaires
  (sets round-trip id/code, `get_catalog`, bulk `get_by_type` / `get_by_id`,
  validation locale `get_named`) ; `docs/live_integration_tests.md` ;
  scripts `scripts/run_live_integration_tests.*` ; README, `ci_integration_tests.md`,
  `pyproject.toml` (marqueur), CHANGELOG.

### Buts
- Un seul point de construction du client reel ; suite live documentee et separee des
  unites ; couverture inchangee pour les runs standards.

### Impact
- Memes commandes `pytest` / `make test-integration` ; referentiel live centralise.

## 2026-03-22 18:00:00

### Modifications
- **Integration sans cov-fail-under** : README (tableau remplace par listes), commentaire
  `pyproject.toml`, `make test` / `test-unit`, CHANGELOG, `docs/ci_integration_tests.md`.

### Buts
- Documenter pourquoi `pytest tests/integration` seul exige `--no-cov` ; garder le seuil
  90 % sur les runs standards.

### Impact
- `make test-integration` reste la commande de reference pour le reseau.

## 2026-03-22 12:00:00

### Modifications
- **Installabilite tests live** : README (wheel / editable / wheel fichier, verification,
  `make`), `docs/ci_integration_tests.md`, `Makefile` ; CHANGELOG.

### Buts
- Rendre explicite l'usage de `baobab-web-api-caller` sans `sys.path` ; faciliter CI
  et developpement conjoint.

### Impact
- Memes commandes `pytest` ; confort `make install-dev` / `make test-integration`.

## 2026-03-21 23:30:00

### Modifications
- **Integration live — debit Scryfall** : `tests/integration/live_transport_config.py`
  (`build_live_service_config`, ~6 req/s, `User-Agent` + `Accept` via `ServiceConfig`) ;
  `conftest.py` aligne ; tests unitaires de structure `test_live_transport_config.py` ;
  README / CHANGELOG.

### Buts
- Respecter les attentes Scryfall (debit conservateur, en-tetes explicites) sans HTTP
  hors `baobab-web-api-caller`.

### Impact
- Meme commande `pytest tests/integration --no-cov` ; delais implicites via throttling
  du transport.

## 2026-03-21 22:00:00

### Modifications
- **Tests d'integration Scryfall** : `tests/integration` (fixture `live_scryfall_client`,
  marqueur `integration`, constantes `scryfall_live_constants.py`) ; pytest ignore ce
  dossier par defaut ; suppression du workflow GitHub Actions ; README / CHANGELOG /
  `V1_compliance.md`.

### Buts
- Valider la chaine reelle `baobab-web-api-caller` + `ScryfallApiCaller` sans HTTP direct.

### Impact
- `python -m pytest` = unites ; `python -m pytest tests/integration --no-cov` = reseau.

## 2026-03-21 18:00:00

### Modifications
- **Stabilisation V1 RC** : tests supplementaires (`BulkDataMapper` branches invalide,
  `SetsService.get_by_code` non-string, `require_uuid_string` non-string) ; couverture
  ~97 % ; classifier PyPI Production/Stable ; README / CHANGELOG / `V1_compliance.md`
  (bilan RC).

### Buts
- Fermer la release candidate avant tag 0.1.0 sans nouvelle fonctionnalite metier.

### Impact
- Depôt pret pour merge `main` puis etiquetage.

## 2026-03-20 21:00:00

### Modifications
- Documentation **release V1 / 0.1.0** : README (objectif, exports `__version__` /
  `__all__`, limitations, etat projet, `list_sets` signature) ; `CHANGELOG.md`
  restructure avec section `[0.1.0]` ; `docs/V1_compliance.md` (CI, hors perimetre,
  ecarts, post-V1) ; metadonnees `pyproject.toml` (keywords, classifiers) ;
  test `test_packaging_public_api` (version vs metadata, exports racine).

### Buts
- Aligner la documentation et le packaging sur l'implementation reelle pour une
  publication coherente.

### Impact
- Les consommateurs peuvent s'appuyer sur README + matrice V1 pour le perimetre 0.1.0.

## 2026-03-21 20:30:00

### Modifications
- Ajustement tests pour la CI : `FakeBaobabStyleResponse` (remplace `BaobabResponse`
  importe) ; test metadata `baobab-web-api-caller` via `importlib.metadata` pour ne
  pas executer `baobab_web_api_caller.__init__` (wheel PyPI + Python 3.11).

### Buts
- Faire passer le job pytest sur GitHub Actions sans modifier le code metier.

### Impact
- La CI reste alignee sur l'installation standard `pip install -e ".[dev]"`.

## 2026-03-21 20:00:00

### Modifications
- Ajout du workflow **GitHub Actions** `ci.yml` : qualite statique + pytest avec
  seuil de couverture 90 % ; documentation README (badge, commandes alignees sur
  bandit `src` + `tests`) ; `CHANGELOG.md`.

### Buts
- Materialiser la preuve de qualite par une CI automatique sur `main`.

### Impact
- Chaque PR declenche les memes controles qu'en local.

## 2026-03-21 19:30:00

### Modifications
- Passage de finition domaine **Cards V1** : factorisation validations texte
  (`require_non_empty_text`), docstrings, README (tableau + erreurs), conformite V1,
  test de surface publique `CardsService`.

### Buts
- Uniformiser l'API et la documentation apres ajout search / random / autocomplete / collection.

### Impact
- `CardsService` et README decrivent de maniere alignee le perimetre V1 Cards.

## 2026-03-21 18:00:00

### Modifications
- Domaine Cards : `CardsService.get_collection` (`POST /cards/collection`) avec
  `CardCollectionIdentifier`, `CardCollectionResult`, `CardCollectionMapper` ;
  limite 75 identifiants ; validation des schemas Scryfall ; `not_found` mappe en
  tuple de dicts ; validateurs `require_non_empty_text` / `require_strict_positive_int`.
- README, `CHANGELOG.md`, `docs/V1_compliance.md` ; tests unitaires (modeles, mapper,
  service, validateurs).

### Buts
- Finaliser le perimetre Cards V1 incluant `collection`.

### Impact
- `client.cards.get_collection(...)` disponible pour les lots d'identifiants.

## 2026-03-21 12:00:00

### Modifications
- Domaine Cards : `CardsService.search` (`GET /cards/search`, `ListResponse[Card]`
  via `ScryfallListResponseParser`), `CardsService.autocomplete` (`GET /cards/autocomplete`,
  `AutocompleteResult` + `AutocompleteMapper`), `CardsService.random` (`GET /cards/random`).
- Validateur partage `ScryfallRequestValidators.require_scryfall_query_string` pour
  `q` (type, non vide) sans reecrire le DSL transmis a Scryfall.
- Tests unitaires (service, mapper, validateurs) ; README, `CHANGELOG.md`.

### Buts
- Couvrir les endpoints Cards search / autocomplete / random sans `collection` dans cette branche.

### Impact
- `client.cards.search|autocomplete|random` disponibles avec le transport existant.

## 2026-03-21 06:00:00

### Modifications
- Integration officielle de `baobab-web-api-caller` : protocole `WebApiTransportProtocol`,
  adaptation `ScryfallHttpClient` vers `path` / `query_params` / `json_body`,
  extraction `json_data` depuis `BaobabResponse`, `BaobabQueryParamsNormalizer`.
- Dependance PyPI bornee `<2.0.0` ; tests packaging (tomllib) et import du package
  transport ; README avec enchainement `BaobabServiceCaller` + `ScryfallApiCaller`.

### Buts
- Aligner le code sur l'API reelle de la librairie de transport et securiser l'injection.

### Impact
- Les consommateurs peuvent brancher le transport PyPI sans couche HTTP parallele.

## 2026-03-21 05:00:00

### Modifications
- Durcissement qualite V1 : tests supplementaires (`ScryfallHttpClient` POST /
  erreurs, `CardsService` validations, `BaobabScryfallApiCallerException.__str__`,
  `CardsApiClient.post`), couverture globale renforcee.
- Documentation : `docs/V1_compliance.md`, sections README (packaging, qualite,
  lien conformite), `CHANGELOG.md`.
- Note historique : precision sous l'entree du 2026-03-20 19:40:00 (plan non
  reflete dans le code).

### Buts
- Finaliser une V1 stable, homogene et verifiable avant integration continue elargie.

### Impact
- Moins d'angles morts sur le transport HTTP et les validations Cards ; trace
  ecrite des ecarts au cahier des charges.

## 2026-03-21 04:00:00

### Modifications
- Alignement README / CHANGELOG : le perimetre **Cards** documente reflete
  uniquement les methodes presentes dans `CardsService` ; les endpoints
  `search`, `collection`, `autocomplete` et `random` sont indiques comme non
  exposes pour l'instant (ecart explicite avec le cahier des charges V1 cible).

### Buts
- Eviter toute ambiguite pour les utilisateurs de la librairie.

### Impact
- La documentation ne suggere plus que les methodes manquantes sont livrees.

## 2026-03-21 03:00:00

### Modifications
- Introduction de `ScryfallApiCaller` : facade legere exposant les services V1
  (`cards`, `sets`, `rulings`, `catalogs`, `bulk_data`) avec validation du
  transport et injection optionnelle par service pour les tests.
- Reexports : package racine `baobab_scryfall_api_caller` et
  `baobab_scryfall_api_caller.client`.
- README restructure (installation, tableau des services, exemples unifies) ;
  `CHANGELOG.md` mis a jour.
- Tests : `tests/.../client/test_scryfall_api_caller.py` (types, transport partage,
  injection, imports publics).

### Buts
- Rendre la librairie consommable via un point d'entree clair sans god object.

### Impact
- Les integrateurs peuvent demarrer avec un seul import et des exemples alignes
  sur l'API reelle.

## 2026-03-21 02:00:00

### Modifications
- Ajout du domaine Bulk Data : `BulkData`, `BulkDataMapper`, `BulkDataApiClient`,
  `BulkDataService` avec liste (`/bulk-data`), acces par UUID ou par type
  kebab-case, et regles de coherence sur `download_uri` / `size`
  (`ScryfallBulkDataException`).
- Tests unitaires miroir et documentation (`README.md`, `CHANGELOG.md`).
- Test supplementaire : `get_by_type` avec espaces uniquement (slug vide apres
  `strip`).

### Buts
- Exposer les metadonnees des exports bulk Scryfall sans telechargement ni cache.

### Impact
- Les integrations peuvent resoudre l'URL courante des fichiers bulk de maniere
  typee et validee.

## 2026-03-21 01:00:00

### Modifications
- Ajout du domaine Catalogs : `Catalog`, `CatalogMapper`, `CatalogsApiClient`,
  `CatalogsService` avec methode generique `get_catalog` et helpers V1
  (noms de cartes, types de creature / terrain / carte, artistes).
- Validation locale des cles catalogue (kebab-case) et mapping strict du
  payload `object: catalog` (distinct des listes paginees).
- Tests unitaires miroir et documentation (`README.md`, `CHANGELOG.md`).

### Buts
- Offrir un acces simple aux catalogues Scryfall sans dupliquer le transport HTTP.

### Impact
- Les applications peuvent consommer les jeux de valeurs de reference Scryfall
  de maniere typee et testee.

## 2026-03-21 00:15:00

### Modifications
- Ajout du domaine Rulings : `Ruling`, `RulingMapper`, `RulingsApiClient`,
  `RulingsService` avec `list_for_card_id` (liste paginee via
  `ScryfallListResponseParser`).
- Introduction de `ScryfallRequestValidators` pour factoriser validation UUID et
  parametre `page` ; refactor de `SetsService` pour reutiliser ce composant.
- Tests unitaires miroir (modele, mapper, client, service, validateurs) et mise
  a jour de `README.md`, `CHANGELOG.md`.

### Buts
- Couvrir le perimetre V1 rulings par identifiant carte sans API speculative.
- Garder le service extensible (nouvelles methodes de recouvrement possibles plus tard).

### Impact
- Les consommateurs peuvent recuperer les textes de rulings Oracle pour une carte donnee.

## 2026-03-20 23:30:00

### Modifications
- Ajout du domaine Sets : `Set`, `SetMapper`, `SetsApiClient`, `SetsService`
  avec liste paginee et recuperation par code ou UUID.
- Introduction de `ScryfallHttpClient` et refactor de `CardsApiClient` pour
  centraliser GET/POST JSON sans dupliquer la logique transport.
- Ajout de `scryfall_payload_coercions` pour factoriser les coercitions communes
  aux mappers Carte et Set.
- Tests unitaires miroir (client HTTP, mapper, service, modele) et documentation
  (`README.md`, `CHANGELOG.md`).

### Buts
- Livrer le perimetre Sets V1 (liste, get par code, get par id) aligne sur Cards.
- Respecter la contrainte « un seul endroit » pour le transport HTTP generique.

### Impact
- Les integrations peuvent consommer les sets Scryfall de maniere typee et testee.
- Les futurs domaines pourront reutiliser `ScryfallHttpClient` de la meme facon.

## 2026-03-20 19:40:00

**Note (2026-03-21)** : le corps ci-dessous decrivait un plan d'extension **non
present dans l'arbre source** au moment de la V1 ; il est conserve pour l'historique
du journal uniquement.

### Modifications
- Ajout des modeles de requete Cards : `CardSearchQuery`, `NamedCardQuery`,
  `CardCollectionIdentifier`.
- Extension de `CardsApiClient` avec support `POST` JSON pour endpoint collection.
- Extension de `CardsService` avec les methodes `search`, `get_collection`,
  `autocomplete` et `get_random`.
- Reutilisation du socle de pagination (`ScryfallListResponseParser`) pour `search`
  et `collection`.
- Ajout des tests unitaires complementaires sur modeles, client et service.
- Mise a jour de `README.md` et `CHANGELOG.md`.

### Buts
- Finaliser la couverture du perimetre Cards V1 sans casser l'API deja exposee.
- Garantir les validations metier (dont limite 75 identifiants en collection)
  et une gestion d'erreurs metier coherente.

### Impact
- Le domaine Cards couvre desormais tout le perimetre V1 attendu.
- Les reponses listes sont mappees en `ListResponse[Card]` avec metadonnees de pagination.
- Les futures integrations `client.cards` disposent d'une API stable et complete.

## 2026-03-20 19:20:00

### Modifications
- Ajout des modeles Cards `Card` et `CardFace`.
- Ajout du `CardMapper` pour mapper les payloads de carte.
- Ajout de `CardsApiClient` pour encapsuler les appels HTTP Cards via
  `baobab-web-api-caller`.
- Ajout de `CardsService` avec les methodes :
  `get_by_id`, `get_by_mtgo_id`, `get_by_cardmarket_id`,
  `get_by_set_and_number`, `get_named` (`exact`/`fuzzy`).
- Ajout des tests unitaires sur modeles, mapper, client et service.
- Mise a jour des exports publics et de la documentation (`README.md`, `CHANGELOG.md`).

### Buts
- Livrer une premiere API Cards exploitable sur le perimetre V1 prioritaire.
- Garantir la robustesse du mapping et de la gestion d'erreurs avant ajout des autres endpoints.

### Impact
- Le domaine Cards est desormais utilisable sur les cas d'acces unitaires principaux.
- Les validations locales et les erreurs API sont traduites en exceptions metier dediees.
- La base est prete pour l'extension vers `search`, `collection`, `autocomplete` et `random`.

## 2026-03-20 19:05:00

### Modifications
- Ajout des modeles communs `ListResponse`, `PaginationMetadata`, `ScryfallWarning`.
- Ajout du modele `ScryfallErrorPayload` pour la structure d'erreur distante.
- Ajout des composants de pagination `ScryfallListResponseValidator`,
  `ScryfallListResponseParser` et `ScryfallPage`.
- Mise a jour des exports publics des packages `models/common` et `pagination`.
- Ajout des tests unitaires exhaustifs sur modeles et pagination.
- Mise a jour de `README.md` pour documenter ce socle partage.

### Buts
- Fournir un contrat commun reutilisable pour les futures features `cards`, `sets`,
  `rulings`, `catalogs` et `bulk_data`.
- Garantir une validation robuste des reponses liste avant l'integration des services metier.

### Impact
- Le projet dispose d'une base de pagination stable et typee.
- Les cas invalides de format/liste/pagination remontent des exceptions metier dediees.
- L'integration future des services pourra se concentrer sur la logique metier specifique.

## 2026-03-20 18:55:00

### Modifications
- Ajout de la hierarchie complete des exceptions metier dans `src/.../exceptions/`.
- Ajout du composant `ScryfallErrorTranslator` dans `src/.../mappers/`.
- Mise a jour des exports publics des packages `exceptions` et `mappers`.
- Ajout des tests unitaires complets de la couche exceptions/traduction.
- Mise a jour de `README.md` pour documenter la couche d'erreurs.

### Buts
- Poser un contrat d'erreur unique et reutilisable pour tous les futurs services Scryfall.
- Centraliser la traduction des erreurs techniques vers des exceptions metier explicites.

### Impact
- Les futures features peuvent lever des erreurs homogenes et diagnostiquables.
- Le socle est decouple d'une implementation fragile de la couche transport.
- La couche erreurs est testee de facon unitaire et prete a l'integration.

## 2026-03-20 18:40:00

### Modifications
- Creation du socle initial du projet `baobab-scryfall-api-caller`.
- Mise en place de l'arborescence source sous `src/baobab_scryfall_api_caller/`.
- Mise en place de la structure miroir sous `tests/baobab_scryfall_api_caller/`.
- Initialisation du packaging et de l'export public.
- Centralisation des configurations qualite et tests dans `pyproject.toml`.
- Initialisation de la documentation `README.md` et `CHANGELOG.md`.
- Ajout de tests de bootstrap pour l'import du package et la disponibilite des dossiers de base.

### Buts
- Etablir une base saine, testable et maintenable avant l'implementation des services metier.
- Verifier le respect des contraintes projet (qualite, structure, typage, couverture).

### Impact
- Le projet devient installable et pret a accueillir les fonctionnalites V1.
- La chaine de validation (qualite, tests, coverage) peut etre executee des maintenant.
- Le cadre architectural est explicitement pose sans introduire de logique metier prematuree.
