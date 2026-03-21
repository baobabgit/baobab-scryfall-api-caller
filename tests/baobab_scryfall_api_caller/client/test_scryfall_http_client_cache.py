"""Tests du cache optionnel dans ScryfallHttpClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.cache import InMemoryJsonCache
from baobab_scryfall_api_caller.client.scryfall_http_client import ScryfallHttpClient
from baobab_scryfall_api_caller.exceptions import ScryfallNotFoundException


class CountingFakeWebApiCaller:
    """Transport de test : compte les appels get reussis."""

    def __init__(self, *, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.get_calls = 0

    def get(self, *, route: str, params: dict[str, Any] | None, headers: dict[str, str]) -> Any:
        self.get_calls += 1
        return self.payload


class TestScryfallHttpClientCache:
    """Miss puis hit ; erreurs non cachees ; desactive par defaut."""

    def test_second_get_uses_cache_for_catalog(self) -> None:
        """Deux GET identiques : un seul appel transport si cache active."""
        catalog_payload = {
            "object": "catalog",
            "uri": "https://api.scryfall.com/catalog/x",
            "total_values": 1,
            "data": ["a"],
        }
        transport = CountingFakeWebApiCaller(payload=catalog_payload)
        cache = InMemoryJsonCache()
        http = ScryfallHttpClient(
            web_api_caller=transport,
            response_cache=cache,
        )
        r1 = http.get(route="/catalog/x", params=None)
        r2 = http.get(route="/catalog/x", params=None)
        assert r1 == r2
        assert transport.get_calls == 1

    def test_without_cache_always_hits_transport(self) -> None:
        """Sans cache : chaque get appelle le transport."""
        catalog_payload = {
            "object": "catalog",
            "uri": "u",
            "total_values": 0,
            "data": [],
        }
        transport = CountingFakeWebApiCaller(payload=catalog_payload)
        http = ScryfallHttpClient(web_api_caller=transport)
        http.get(route="/catalog/x", params=None)
        http.get(route="/catalog/x", params=None)
        assert transport.get_calls == 2

    def test_error_response_not_cached(self) -> None:
        """Les reponses erreur ne sont pas stockees : chaque appel touche le transport."""
        err_payload = {"object": "error", "status": 404, "details": "Not found"}
        transport = CountingFakeWebApiCaller(payload=err_payload)
        cache = InMemoryJsonCache()
        http = ScryfallHttpClient(
            web_api_caller=transport,
            response_cache=cache,
        )
        for _ in range(2):
            try:
                http.get(route="/catalog/x", params=None)
            except ScryfallNotFoundException:
                pass
            else:
                assert False, "expected not found"
        assert transport.get_calls == 2

    def test_predicate_can_disable_caching_for_route(self) -> None:
        """Predicate False : pas de stockage malgre cache fourni."""
        catalog_payload = {
            "object": "catalog",
            "uri": "u",
            "total_values": 0,
            "data": [],
        }
        transport = CountingFakeWebApiCaller(payload=catalog_payload)
        cache = InMemoryJsonCache()
        http = ScryfallHttpClient(
            web_api_caller=transport,
            response_cache=cache,
            cacheable_get_predicate=lambda _r, _p: False,
        )
        http.get(route="/catalog/x", params=None)
        http.get(route="/catalog/x", params=None)
        assert transport.get_calls == 2
