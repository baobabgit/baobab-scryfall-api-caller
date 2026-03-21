# Notes de release — baobab-scryfall-api-caller 1.0.0

**Date** : 2026-03-23

## Resume

Premiere release **stable** au sens [semver](https://semver.org/lang/fr/) : le package
s'engage sur une API publique stable (`ScryfallApiCaller`, exports racine, services
domaine) pour les versions **1.x.y** compatibles.

Le comportement est **identique** a la version **0.2.0** ; seuls le numero de version
et la documentation de positionnement changent.

## Points clefs

- **Compatibilite** : `requires-python >= 3.11` ; dependance runtime
  `baobab-web-api-caller>=0.1.0,<2.0.0` (inchangee).
- **API publique racine** : `ScryfallApiCaller`, `WebApiTransportProtocol`, `__version__`.
- **Limitations** : inchangées — transport injecte, bulk opt-in, tests live optionnels
  (voir `README.md`).

## Installation

```bash
pip install baobab-scryfall-api-caller==1.0.0
```

## Historique fonctionnel

Le cumul des evolutions depuis 0.1.0 est dans [`CHANGELOG.md`](../CHANGELOG.md)
(sections `[0.2.0]`, `[0.1.0]`).
