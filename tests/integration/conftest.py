"""Fixtures partagees pour les tests d'integration Scryfall."""

from __future__ import annotations

import pytest
from baobab_web_api_caller import (
    BaobabServiceCaller,
    HttpTransportCaller,
    RequestsSessionFactory,
    ServiceConfig,
)

from baobab_scryfall_api_caller import ScryfallApiCaller


@pytest.fixture(scope="session")
def live_scryfall_client() -> ScryfallApiCaller:
    """Construit la chaine reelle : ServiceConfig + transport + BaobabServiceCaller.

    Cible ``https://api.scryfall.com`` comme dans le README du projet.
    """
    service_config = ServiceConfig(base_url="https://api.scryfall.com")
    transport = HttpTransportCaller.from_service_config(
        service_config=service_config,
        session_factory=RequestsSessionFactory(),
    )
    web_api_caller = BaobabServiceCaller(
        service_config=service_config,
        web_api_caller=transport,
    )
    return ScryfallApiCaller(web_api_caller=web_api_caller)
