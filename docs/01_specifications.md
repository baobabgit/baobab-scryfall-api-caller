# Cahier des charges — baobab-scryfall-api-caller

## 1. Objet du projet

La librairie `baobab-scryfall-api-caller` a pour objectif de fournir un client Python structuré, typé, maintenable et testable pour consommer l’API Web de Scryfall, en s’appuyant sur `baobab-web-api-caller` comme couche de transport HTTP mutualisée.

Cette librairie ne doit pas réimplémenter un client HTTP générique. Elle doit encapsuler la logique métier propre à Scryfall :
- construction des routes ;
- sérialisation des paramètres de requête ;
- validation des entrées ;
- désérialisation et mapping des réponses ;
- gestion des objets paginés ;
- traduction des erreurs HTTP et Scryfall vers des exceptions métier dédiées.

---

## 2. Objectifs

Les objectifs du projet sont les suivants :

- fournir une API Python claire, cohérente et simple d’usage ;
- encapsuler proprement les services exposés par l’API Scryfall ;
- s’appuyer strictement sur `baobab-web-api-caller` pour tout appel réseau ;
- garantir un haut niveau de qualité logicielle ;
- respecter les contraintes de développement déjà retenues pour `baobab-web-api-caller` ;
- permettre une extension progressive du périmètre sans casser l’API publique.

---

## 3. Dépendances et principes d’intégration

## 3.1 Dépendance obligatoire

La librairie `baobab-scryfall-api-caller` doit utiliser `baobab-web-api-caller` comme sous-module technique d’appel HTTP.

## 3.2 Règles d’intégration

- aucun appel HTTP direct n’est autorisé hors de `baobab-web-api-caller` ;
- toute requête réseau doit passer par les abstractions fournies par cette librairie ;
- la logique Scryfall doit rester séparée de la logique de transport ;
- les mécanismes génériques HTTP ne doivent pas être dupliqués dans cette librairie.

## 3.3 Capacités minimales attendues du sous-module

Le sous-module `baobab-web-api-caller` doit permettre a minima :
- requêtes HTTP `GET` ;
- requêtes HTTP `POST` avec payload JSON ;
- gestion des query parameters ;
- injection de headers ;
- lecture de réponses JSON ;
- lecture de réponses non JSON si nécessaire ;
- gestion des codes d’erreur HTTP ;
- configuration des timeouts ;
- gestion propre du cycle de vie des sessions et des réponses.

---

## 4. Périmètre fonctionnel de la V1

La version initiale doit couvrir un sous-ensemble cohérent et directement utile de l’API Scryfall.

## 4.1 Services cartes

La librairie doit permettre :

- récupération d’une carte par identifiant Scryfall ;
- récupération d’une carte par identifiant MTGO ;
- récupération d’une carte par identifiant Cardmarket ;
- récupération d’une carte par code de set + numéro de collection ;
- récupération d’une carte par nom via endpoint `named` ;
- recherche de cartes via endpoint `search` ;
- récupération de cartes en lot via endpoint `collection` ;
- autocomplétion de noms de cartes ;
- récupération d’une carte aléatoire.

## 4.2 Services sets

La librairie doit permettre :

- la récupération de la liste complète des sets ;
- la récupération d’un set par code ;
- la récupération d’un set par identifiant Scryfall.

## 4.3 Services rulings

La librairie doit permettre :

- la récupération des rulings d’une carte par identifiant Scryfall.

L’architecture devra permettre d’ajouter facilement d’autres variantes plus tard.

## 4.4 Services catalogues

La librairie doit permettre :

- un accès générique à un catalogue Scryfall ;
- des helpers explicites pour les catalogues les plus utilisés.

## 4.5 Services bulk data

La librairie doit permettre :

- de lister les jeux de données bulk disponibles ;
- de récupérer les métadonnées d’un dataset bulk ;
- d’exposer l’URL de téléchargement fournie par Scryfall ;
- de préparer une extension future vers téléchargement assisté.

---

## 5. Hors périmètre de la V1

Ne sont pas obligatoires en V1 :

- couverture exhaustive de tous les endpoints secondaires ;
- téléchargement automatique des fichiers bulk ;
- cache applicatif ;
- stratégie avancée de retry ;
- persistance locale ;
- CLI ;
- intégration asynchrone ;
- support multi-backend HTTP ;
- instrumentation avancée.

Ces éléments pourront être prévus par l’architecture mais ne doivent pas bloquer la V1.

---

## 6. Exigences fonctionnelles détaillées

## 6.1 Appels cartes

### 6.1.1 Récupération par identifiant

Le client doit permettre de récupérer une carte à partir de différents identifiants supportés par Scryfall.

### 6.1.2 Recherche nominale

Le client doit exposer les modes de recherche pertinents du endpoint `named`, notamment :
- `exact`
- `fuzzy`

### 6.1.3 Recherche avancée

Le client doit permettre d’envoyer une requête Scryfall via le paramètre `q` sans modifier le DSL de recherche fourni par l’utilisateur.

### 6.1.4 Collection

Le client doit permettre d’envoyer une collection d’identifiants vers l’endpoint prévu à cet effet.

Validation obligatoire :
- refus côté client si plus de 75 références sont fournies.

### 6.1.5 Autocomplete

Le client doit exposer une méthode simple retournant les suggestions de noms.

### 6.1.6 Random

Le client doit permettre :
- un appel sans filtre ;
- un appel avec filtre `q`.

## 6.2 Appels sets

Le client doit permettre :
- listage complet ;
- récupération par code ;
- récupération par identifiant.

## 6.3 Appels rulings

Le client doit permettre la lecture des rulings associés à une carte.

## 6.4 Catalogues

Le client doit permettre :
- un accès générique ;
- des méthodes spécialisées pour les catalogues fréquents.

## 6.5 Bulk data

Le client doit exposer :
- liste des jeux bulk ;
- détail d’un bulk dataset ;
- URL de téléchargement ;
- métadonnées utiles au consommateur.

---

## 7. Exigences non fonctionnelles

## 7.1 Qualité

Le code doit être :
- lisible ;
- modulaire ;
- typé ;
- documenté ;
- testable ;
- maintenable.

## 7.2 Stabilité API

L’API publique exposée par la librairie doit être stable et explicite.

## 7.3 Extensibilité

L’architecture doit permettre l’ajout futur de nouveaux endpoints sans refonte majeure.

## 7.4 Performance

La librairie doit rester légère. Aucun traitement inutile ou surcouche excessive ne doit être introduit.

## 7.5 Sécurité

La librairie ne doit pas masquer les erreurs critiques et doit conserver suffisamment de contexte pour le diagnostic.

---

## 8. Contraintes de développement

Les contraintes de développement doivent être les mêmes que celles retenues pour `baobab-web-api-caller`.

## 8.1 Architecture orientée classes

- code organisé en classes cohérentes ;
- responsabilité claire par classe ;
- une classe par fichier.

## 8.2 Structure du projet

- séparation claire entre sources, tests et documentation ;
- structure stable et compréhensible ;
- organisation miroir entre `src/` et `tests/`.

## 8.3 Typage

- toutes les API publiques doivent être annotées ;
- les structures internes importantes doivent également être typées.

## 8.4 Documentation

- docstrings obligatoires sur les éléments publics ;
- documentation de haut niveau dans le dépôt.

## 8.5 Exceptions projet

Toute erreur spécifique au projet doit faire l’objet d’une exception dédiée.

## 8.6 Qualité outillée

La configuration qualité doit être centralisée dans `pyproject.toml`.

---

## 9. Architecture cible

Arborescence recommandée :

```text
src/baobab_scryfall_api_caller/
├── __init__.py
├── client/
│   └── scryfall_api_caller.py
├── services/
│   ├── cards/
│   │   ├── cards_service.py
│   │   ├── card_search_service.py
│   │   ├── card_collection_service.py
│   │   └── card_autocomplete_service.py
│   ├── sets/
│   │   └── sets_service.py
│   ├── rulings/
│   │   └── rulings_service.py
│   ├── catalogs/
│   │   └── catalogs_service.py
│   └── bulk_data/
│       └── bulk_data_service.py
├── models/
│   ├── cards/
│   ├── sets/
│   ├── rulings/
│   ├── catalogs/
│   ├── bulk_data/
│   └── common/
├── exceptions/
│   ├── baobab_scryfall_api_caller_exception.py
│   ├── scryfall_request_exception.py
│   ├── scryfall_not_found_exception.py
│   ├── scryfall_validation_exception.py
│   ├── scryfall_rate_limit_exception.py
│   ├── scryfall_response_format_exception.py
│   ├── scryfall_pagination_exception.py
│   └── scryfall_bulk_data_exception.py
├── mappers/
├── pagination/
├── constants/
└── utils/
```

Cette arborescence est indicative. Elle peut être ajustée, à condition de conserver :
- clarté ;
- cohérence ;
- séparation des responsabilités ;
- testabilité.

---

## 10. API Python attendue

## 10.1 Client principal

Un point d’entrée principal doit être fourni, par exemple :

```python
client = ScryfallApiCaller(web_api_caller=web_api_caller)
```

## 10.2 Services exposés

Le client doit exposer des services spécialisés, par exemple :
- `client.cards`
- `client.sets`
- `client.rulings`
- `client.catalogs`
- `client.bulk_data`

## 10.3 Exemples d’usage cible

```python
client = ScryfallApiCaller(web_api_caller=web_api_caller)

card = client.cards.get_by_id("00000000-0000-0000-0000-000000000000")
named = client.cards.get_named(fuzzy="Black Lotus")
results = client.cards.search(q="t:dragon cmc<=3")
cards = client.cards.get_collection(identifiers=[...])
choices = client.cards.autocomplete(query="Ligh")
random_card = client.cards.get_random(q="t:angel")
sets = client.sets.list_all()
set_data = client.sets.get_by_code("lea")
rulings = client.rulings.get_by_scryfall_id("00000000-0000-0000-0000-000000000000")
catalog = client.catalogs.get_card_names()
bulk_items = client.bulk_data.list_all()
```

---

## 11. Modèles métiers à prévoir

La librairie doit modéliser au minimum les objets suivants :

- `Card`
- `CardFace`
- `Set`
- `Ruling`
- `Catalog`
- `BulkData`
- `ListResponse[T]`

Objets de requête recommandés :
- `CardSearchQuery`
- `NamedCardQuery`
- `CardCollectionIdentifier`

Objets techniques recommandés :
- informations de pagination ;
- objets d’erreur Scryfall ;
- métadonnées de liste.

La modélisation peut être réalisée au moyen de classes dédiées, dataclasses, ou autre mécanisme cohérent avec les choix du projet.

---

## 12. Gestion de la pagination

La librairie doit gérer les réponses paginées de Scryfall.

## 12.1 Exigences minimales

Un objet de liste doit exposer au moins :
- les données ;
- `has_more` ;
- `next_page` ;
- les éventuels avertissements ;
- les éventuelles informations complémentaires utiles.

## 12.2 Exigences d’usage

Le consommateur doit pouvoir :
- accéder aux métadonnées de pagination ;
- itérer simplement sur les résultats ;
- récupérer l’URL ou les paramètres de page suivante.

---

## 13. Gestion des headers, paramètres et comportement HTTP

## 13.1 Headers par défaut

Le client doit permettre d’injecter proprement les headers nécessaires à l’API Scryfall.

## 13.2 Paramètres de requête

La sérialisation des query params doit être :
- fiable ;
- explicite ;
- testée.

## 13.3 Corps JSON

Les endpoints nécessitant un payload JSON doivent être supportés proprement.

## 13.4 Réponses JSON

Le mapping de réponse doit être robuste face :
- aux champs attendus ;
- aux champs optionnels ;
- aux réponses partielles ;
- aux structures inattendues.

---

## 14. Gestion des erreurs

## 14.1 Principe général

Toutes les erreurs spécifiques à la librairie doivent être représentées par des exceptions métier dédiées.

## 14.2 Hiérarchie minimale recommandée

```text
BaobabScryfallApiCallerException
├── ScryfallRequestException
├── ScryfallNotFoundException
├── ScryfallValidationException
├── ScryfallRateLimitException
├── ScryfallResponseFormatException
├── ScryfallPaginationException
└── ScryfallBulkDataException
```

## 14.3 Exigences

Les exceptions doivent, quand pertinent, conserver :
- le code HTTP ;
- le message d’erreur ;
- l’URL appelée ;
- les paramètres de requête ;
- le payload utile au diagnostic ;
- la réponse brute ou sa partie utile.

## 14.4 Traduction des erreurs

La librairie doit traduire :
- les erreurs réseau ;
- les erreurs HTTP ;
- les erreurs de format ;
- les erreurs de validation locales ;
- les erreurs Scryfall spécifiques.

---

## 15. Validation métier

Les validations minimales à faire côté client incluent :

- collection limitée à 75 identifiants ;
- vérification des paramètres obligatoires ;
- interdiction des combinaisons incompatibles ;
- validation des types attendus ;
- validation des structures de payload pour les appels `POST`.

Ces validations doivent produire des exceptions projet dédiées.

---

## 16. Tests

## 16.1 Règles générales

- un fichier de test par classe ;
- organisation des tests en classes `Test...` ;
- structure miroir avec `src/` ;
- couverture minimale de 90 %.

## 16.2 Cas de test à couvrir

Les tests doivent couvrir :
- cas nominaux de chaque endpoint V1 ;
- validation locale des paramètres ;
- sérialisation des query params ;
- sérialisation des payloads JSON ;
- mapping des réponses ;
- pagination ;
- traduction des erreurs HTTP ;
- traduction des erreurs Scryfall ;
- réponses partielles ;
- réponses inattendues ;
- limites métier spécifiques ;
- gestion correcte des exceptions.

## 16.3 Typologie de tests

### Tests unitaires
Ils doivent utiliser des mocks ou doubles de test du sous-module `baobab-web-api-caller`.

### Tests d’intégration
Ils peuvent être prévus séparément, désactivables et non bloquants pour le développement local standard.

---

## 17. Qualité et outils

Les outils suivants doivent être intégrés au projet :

- `black`
- `pylint`
- `mypy`
- `flake8`
- `bandit`

## 17.1 Contraintes associées

- longueur maximale de ligne : 100 caractères ;
- configuration centralisée dans `pyproject.toml` ;
- typage obligatoire sur l’API publique ;
- docstrings obligatoires sur les éléments publics.

---

## 18. Documentation à livrer

Le dépôt doit contenir au minimum :

- `README.md`
- `CHANGELOG.md`
- `docs/dev_diary.md`

La documentation doit expliquer :
- le but du projet ;
- son architecture générale ;
- son installation ;
- ses dépendances ;
- les principaux exemples d’usage ;
- les choix techniques structurants ;
- les limites connues de la V1.

---

## 19. Journalisation et diagnostic

Sans imposer de système de logs complexe en V1, la librairie doit être conçue pour faciliter le diagnostic :
- messages d’erreur explicites ;
- contexte utile dans les exceptions ;
- possibilité future d’ajouter une journalisation plus poussée sans refonte.

---

## 20. Compatibilité et packaging

Le projet doit être packagé proprement comme librairie Python.

Il doit inclure :
- structure compatible avec packaging moderne ;
- dépendances déclarées ;
- métadonnées de projet ;
- versionnement cohérent ;
- export clair de l’API publique.

---

## 21. Stratégie de livraison

## 21.1 Priorité de développement recommandée

1. socle projet et packaging ;
2. hiérarchie d’exceptions ;
3. client principal ;
4. services cartes ;
5. pagination ;
6. sets ;
7. rulings ;
8. catalogues ;
9. bulk data ;
10. documentation et stabilisation ;
11. durcissement des tests ;
12. conformité qualité.

## 21.2 Lot V1 recommandé

La V1 doit livrer :
- client principal ;
- endpoints cartes principaux ;
- sets ;
- rulings par identifiant ;
- catalogues principaux ;
- bulk metadata ;
- pagination ;
- exceptions dédiées ;
- tests ;
- documentation.

---

## 22. Critères d’acceptation

Le projet sera considéré conforme si :

- `baobab-web-api-caller` est bien utilisé comme couche de transport ;
- aucun appel HTTP direct parasite n’est introduit ;
- les endpoints du périmètre V1 sont implémentés ;
- les exceptions spécifiques au projet sont en place ;
- la pagination Scryfall est correctement gérée ;
- les validations métier obligatoires sont présentes ;
- les tests passent avec une couverture minimale de 90 % ;
- les outils qualité passent sans erreur bloquante ;
- la documentation minimale exigée est présente ;
- l’API publique est typée, documentée et stable.

---

## 23. Résumé de la cible V1

La V1 de `baobab-scryfall-api-caller` doit fournir une librairie Python propre, fiable et extensible permettant de consommer les services Scryfall les plus utiles, sans dupliquer la couche HTTP déjà portée par `baobab-web-api-caller`, tout en respectant strictement les contraintes de développement du projet.
