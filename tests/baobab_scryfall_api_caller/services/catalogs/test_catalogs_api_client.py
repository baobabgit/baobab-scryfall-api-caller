"""Tests du client technique CatalogsApiClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallNotFoundException
from baobab_scryfall_api_caller.services.catalogs.catalogs_api_client import CatalogsApiClient


class FakeWebApiCaller:
    """Double de test pour simuler baobab-web-api-caller."""

    def __init__(self, *, response: Any = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.last_call: dict[str, Any] | None = None

    def get(self, *, route: str, params: dict[str, Any] | None, headers: dict[str, str]) -> Any:
        """Simule la methode get du caller HTTP."""
        self.last_call = {"route": route, "params": params, "headers": headers}
        if self.error is not None:
            raise self.error
        return self.response


class TestCatalogsApiClient:
    """Valide les appels HTTP du domaine catalogs."""

    def test_get_nominal(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(
            response={
                "object": "catalog",
                "uri": "https://api.scryfall.com/catalog/card-names",
                "total_values": 0,
                "data": [],
            },
        )
        client = CatalogsApiClient(web_api_caller=web_api_caller)
        payload = client.get(route="/catalog/card-names")
        assert payload["object"] == "catalog"
        assert web_api_caller.last_call is not None

    def test_get_not_found(self) -> None:
        """Un 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        client = CatalogsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/catalog/unknown-catalog-xyz")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"
