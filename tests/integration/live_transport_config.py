"""Configuration HTTP des tests d'integration Scryfall (headers + throttling).

Centralise les en-tetes exiges pour l'API Scryfall (notamment ``User-Agent``) et une
politique de debit conservative via ``baobab-web-api-caller`` : ``ServiceConfig`` +
:class:`~baobab_web_api_caller.config.rate_limit_policy.RateLimitPolicy`.

Debit cible : **6 requetes/seconde** en moyenne (intervalle minimal **1/6 s** entre
deux appels), volontairement sous la zone 5–8 req/s demandee pour rester prudent
vis-a-vis des limites Scryfall.
"""

from __future__ import annotations

from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.service_config import ServiceConfig

from baobab_scryfall_api_caller import __version__

SCRYFALL_API_BASE_URL = "https://api.scryfall.com"

# Entre 5 et 8 req/s : 6 req/s => intervalle 1/6 s (conservateur).
LIVE_REQUESTS_PER_SECOND = 6
LIVE_MIN_INTERVAL_SECONDS = 1.0 / float(LIVE_REQUESTS_PER_SECOND)

ACCEPT_HEADER_JSON = "application/json; charset=utf-8"


def _integration_user_agent() -> str:
    """User-Agent stable pour identifier les tests d'integration (doc Scryfall)."""
    return (
        f"baobab-scryfall-api-caller-integration-tests/{__version__} "
        "(+https://github.com/baobabgit/baobab-scryfall-api-caller)"
    )


def build_live_service_config() -> ServiceConfig:
    """Construit la ``ServiceConfig`` partagee par la fixture ``live_scryfall_client``."""
    return ServiceConfig(
        base_url=SCRYFALL_API_BASE_URL,
        default_headers={
            "User-Agent": _integration_user_agent(),
            "Accept": ACCEPT_HEADER_JSON,
        },
        rate_limit_policy=RateLimitPolicy(
            min_interval_seconds=LIVE_MIN_INTERVAL_SECONDS,
        ),
    )
