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
