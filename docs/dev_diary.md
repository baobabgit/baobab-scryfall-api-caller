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
