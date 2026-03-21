# Notes de release — baobab-scryfall-api-caller 0.2.0

**Date** : 2026-03-22

## Resume

Deuxieme release semver : le **perimetre V1** du cahier des charges reste assure ;
cette version consolide les extensions livrees depuis **0.1.0** (modeles, cache HTTP
optionnel, telechargement bulk assiste, pagination, rulings/sets etendus, experience
developpeur et tests d'integration reseau).

## Points clefs

- **Compatibilite** : `requires-python >= 3.11` ; dependance runtime
  `baobab-web-api-caller>=0.1.0,<2.0.0` (inchangee).
- **API publique racine** : `ScryfallApiCaller`, `WebApiTransportProtocol`, `__version__`
  — extensions compatibles (nouveaux parametres optionnels, champs de modeles en fin de
  definition).
- **Documentation** : `CHANGELOG.md`, `README.md`, `docs/V1_compliance.md`,
  `CONTRIBUTING.md`.

## Installation

```bash
pip install baobab-scryfall-api-caller==0.2.0
```

Ou suivez `README.md` pour l'installation editable et les tests.

## Detail des changements

Voir la section **[0.2.0] dans `CHANGELOG.md`](../CHANGELOG.md).
