# Changelog

Toutes les evolutions notables du projet seront documentees dans ce fichier.

Le format suit les recommandations de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et le projet suit le versioning semantique.

## [Unreleased]

### Added
- Domaine Cards : `CardsService.get_collection` (`POST /cards/collection`, `CardCollectionResult`) ;
  modeles `CardCollectionIdentifier`, `CardCollectionResult` ; constante
  `MAX_CARD_COLLECTION_IDENTIFIERS` ; mapper `CardCollectionMapper` ;
  validateurs `ScryfallRequestValidators.require_non_empty_text`,
  `require_strict_positive_int`.
- Domaine Cards : `CardsService.search` (`GET /cards/search`, `ListResponse[Card]`),
  `CardsService.autocomplete` (`GET /cards/autocomplete`, modele `AutocompleteResult`),
  `CardsService.random` (`GET /cards/random`) ; mapper `AutocompleteMapper` ;
  validateur partage `ScryfallRequestValidators.require_scryfall_query_string`.
- Document `docs/V1_compliance.md` : matrice de conformite au cahier des charges,
  ecarts residuels (Cards) et pistes post-V1.
- Sections README : packaging / `py.typed`, commandes qualite, emplacement des
  rapports de couverture, lien vers la conformite V1.
- Facade publique `ScryfallApiCaller` (`client/scryfall_api_caller.py`) : point
  d'entree unique exposant `cards`, `sets`, `rulings`, `catalogs`, `bulk_data`
  avec le meme transport ; reexport depuis le package racine et `client`.
- Documentation utilisateur enrichie (installation, tableau des services, exemples
  par domaine via la facade).
- Domaine Bulk Data : modele `BulkData`, `BulkDataMapper`, `BulkDataApiClient`,
  `BulkDataService` (liste, `get_by_id`, `get_by_type`, exposition `download_uri`
  sans telechargement).
- Domaine Catalogs : modele `Catalog`, `CatalogMapper`, `CatalogsApiClient`,
  `CatalogsService` (`get_catalog` + helpers frequents).
- Domaine Rulings : modele `Ruling`, `RulingMapper`, `RulingsApiClient`,
  `RulingsService` (`list_for_card_id` sur `GET /cards/{id}/rulings`).
- `ScryfallRequestValidators` (pagination optionnelle, UUID) partage entre
  services Sets et Rulings.
- Domaine Sets : modele `Set`, `SetMapper`, `SetsApiClient`, `SetsService`
  (`list_sets`, `get_by_code`, `get_by_id`) avec pagination pour la liste.
- `ScryfallHttpClient` pour mutualiser la couche HTTP ; `CardsApiClient` delegue
  a ce composant.
- `scryfall_payload_coercions` pour les coercitions de champs partagees entre mappers.
- Bootstrap initial du projet (`src`, `tests`, configuration qualite, documentation).
- Couche d'exceptions metier et traducteur d'erreurs.
- Socle de modeles partages et pagination.
- Premiere tranche du domaine Cards (`get_by_id`, `get_by_mtgo_id`,
  `get_by_cardmarket_id`, `get_by_set_and_number`, `get_named` exact/fuzzy).

### Changed
- `CardsService` : validation des entiers positifs (`mtgo_id`, `cardmarket_id`) via
  `ScryfallRequestValidators.require_strict_positive_int` (factorisation avec collection).
- Integration `baobab-web-api-caller` : contrainte de version `>=0.1.0,<2.0.0` ;
  `ScryfallHttpClient` tente les signatures `BaobabServiceCaller` (`path`,
  `query_params`, `json_body`) et lit `BaobabResponse.json_data` ; typage
  `WebApiTransportProtocol` sur la facade et les services ; normaliseur
  `BaobabQueryParamsNormalizer` ; README avec exemple `BaobabServiceCaller` +
  `HttpTransportCaller`.
- Durcissement tests : scenarios HTTP POST supplementaires, validations
  `CardsService`, rendu complet de l'exception racine, couverture de
  `CardsApiClient.post`.

### Fixed
- Documentation : README et changelog alignes sur les methodes reellement exposees
  par `CardsService` (y compris `search`, `collection`, `autocomplete`, `random`).
