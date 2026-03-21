"""Fixtures partagees pour les tests d'integration Scryfall."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller import ScryfallApiCaller

from tests.integration.live_transport_config import build_live_scryfall_client


@pytest.fixture(scope="session")
def live_scryfall_client() -> ScryfallApiCaller:
    """Facade : voir :mod:`tests.integration.live_transport_config` pour la chaine HTTP."""
    return build_live_scryfall_client()
