"""Validation de la configuration HTTP des tests live (sans appel reseau)."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller import ScryfallApiCaller

from tests.integration.live_transport_config import (
    ACCEPT_HEADER_JSON,
    LIVE_MIN_INTERVAL_SECONDS,
    LIVE_REQUESTS_PER_SECOND,
    build_live_scryfall_client,
    build_live_service_config,
)

pytestmark = pytest.mark.integration


class TestLiveTransportPolicy:
    """Politique de debit et en-tetes pour l'integration Scryfall."""

    def test_target_rate_is_between_five_and_eight_per_second(self) -> None:
        """Intervalle minimal coherent avec une moyenne entre 5 et 8 req/s."""
        assert 1.0 / 8.0 <= LIVE_MIN_INTERVAL_SECONDS <= 1.0 / 5.0
        assert LIVE_REQUESTS_PER_SECOND == 6

    def test_service_config_includes_headers_and_rate_limit(self) -> None:
        """``ServiceConfig`` porte User-Agent, Accept et RateLimitPolicy."""
        cfg = build_live_service_config()
        assert cfg.default_headers["User-Agent"].startswith(
            "baobab-scryfall-api-caller-integration-tests/",
        )
        assert (
            "github.com/baobabgit/baobab-scryfall-api-caller" in cfg.default_headers["User-Agent"]
        )
        assert cfg.default_headers["Accept"] == ACCEPT_HEADER_JSON
        assert cfg.rate_limit_policy.min_interval_seconds == LIVE_MIN_INTERVAL_SECONDS

    def test_build_live_scryfall_client_returns_facade(self) -> None:
        """La fabrique assemble la chaine documentee sans appel reseau."""
        client = build_live_scryfall_client()
        assert isinstance(client, ScryfallApiCaller)
