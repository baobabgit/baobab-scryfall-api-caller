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
