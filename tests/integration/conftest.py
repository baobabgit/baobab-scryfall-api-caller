"""Fixtures partagees pour les tests d'integration Scryfall."""

from __future__ import annotations

import pytest
from baobab_web_api_caller import (
    BaobabServiceCaller,
    HttpTransportCaller,
    RequestsSessionFactory,
)

from baobab_scryfall_api_caller import ScryfallApiCaller

from tests.integration.live_transport_config import build_live_service_config


@pytest.fixture(scope="session")
def live_scryfall_client() -> ScryfallApiCaller:
    """Construit la chaine reelle : ServiceConfig + transport + BaobabServiceCaller.

    Headers par defaut (``User-Agent``, ``Accept``) et throttling sont definis dans
    :mod:`tests.integration.live_transport_config` pour respecter l'API Scryfall.
    """
    service_config = build_live_service_config()
    transport = HttpTransportCaller.from_service_config(
        service_config=service_config,
        session_factory=RequestsSessionFactory(),
    )
    web_api_caller = BaobabServiceCaller(
        service_config=service_config,
        web_api_caller=transport,
    )
    return ScryfallApiCaller(web_api_caller=web_api_caller)
