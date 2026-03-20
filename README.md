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

Le projet est en phase de bootstrap technique :

- structure de packages source/tests en place ;
- configuration qualite centralisee dans `pyproject.toml` ;
- packaging initial configure ;
- documentation minimale initialisee ;
- tests de base de bootstrap disponibles.

Les services metier Scryfall ne sont pas encore implementes a ce stade.

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
