# Tests d'intégration live (Scryfall)

Cette page complète le README et `docs/ci_integration_tests.md` : périmètre, chaîne
réelle, politique HTTP et exécution sans mélange avec les tests unitaires.

## Rôle

- Valider **end-to-end** le transport `baobab-web-api-caller`, le mapping et les
  exceptions sur des réponses **réelles** de `https://api.scryfall.com`.
- Ne **remplace pas** la suite unitaire (mocks, couverture ciblée sur `src/`).

## Chaîne injectée

Tous les scénarios réseau utilisent la même construction que le README, centralisée dans
`tests/integration/live_transport_config.py` :

`ServiceConfig` → `HttpTransportCaller` → `BaobabServiceCaller` → `ScryfallApiCaller`.

La fixture pytest `live_scryfall_client` appelle `build_live_scryfall_client()` (point
unique, sans duplication dans les fichiers de test).

## Politique HTTP (Scryfall)

Définie dans `live_transport_config.py` et appliquée via `ServiceConfig` :

- **Débit** : environ **6 requêtes/s** en moyenne (`RateLimitPolicy`, intervalle minimal
  **1/6 s** entre deux appels), volontairement conservateur.
- **`User-Agent`** : `baobab-scryfall-api-caller-integration-tests/<version> (+https://github.com/baobabgit/baobab-scryfall-api-caller)`.
- **`Accept`** : `application/json; charset=utf-8`.

Aucun appel HTTP ne contourne `baobab-web-api-caller`.

## Marqueur et séparation des suites

- Marqueur pytest : **`integration`** (`@pytest.mark.integration` sur les modules
  `tests/integration/`).
- Le dépôt configure **`--ignore=tests/integration`** dans les `addopts` par défaut :
  `python -m pytest` et `python -m pytest tests/` n’exécutent **que** les tests unitaires
  (avec couverture et seuil 90 %).
- Pour **uniquement** la suite live :

  ```bash
  python -m pytest tests/integration --no-cov -m integration
  ```

  Sur environnements avec `make` : `make test-integration` (équivalent).

**Important** : lancer seulement `tests/integration` **sans** `--no-cov` réutilise les
`addopts` globaux (`cov-fail-under=90`) sur une exécution partielle du package → échec
sans valeur ajoutée. Les runs live doivent donc inclure **`--no-cov`** (ou la cible
Makefile dédiée).

## Couverture

- Le seuil **90 %** s’applique aux **runs standards** (unitaires, tout `src/` exercé
  comme prévu).
- Les tests live ne visent pas à tenir ce seuil ; ne pas les mesurer avec les mêmes
  options que la CI locale habituelle.

## Dépendance `baobab-web-api-caller`

L’import `baobab_web_api_caller` doit provenir d’une **installation pip** (PyPI, wheel
fichier ou editable). Ne pas utiliser de manipulation de `sys.path`. Voir
`docs/ci_integration_tests.md` pour les scénarios CI.

## Données stables

Identifiants et requêtes : `tests/integration/scryfall_live_constants.py`. Préférence
pour des **round-trips** (ex. `sets.get_by_code` puis `sets.get_by_id`) plutôt que des
UUID figés quand cela évite la fragilité.

## Scripts optionnels

À la racine du dépôt :

- `scripts/run_live_integration_tests.ps1` (Windows PowerShell)
- `scripts/run_live_integration_tests.sh` (Unix / Git Bash)

Ils encapsulent la ligne `pytest` ci-dessus avec `--no-cov` et `-m integration`.
