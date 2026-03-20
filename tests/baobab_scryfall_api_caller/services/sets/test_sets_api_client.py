"""Tests du client technique SetsApiClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallNotFoundException
from baobab_scryfall_api_caller.services.sets.sets_api_client import SetsApiClient


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


class TestSetsApiClient:
    """Valide les appels HTTP du domaine sets."""

    def test_get_nominal(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "set", "id": "x", "code": "neo", "name": "Neo"},
        )
        client = SetsApiClient(web_api_caller=web_api_caller)
        payload = client.get(route="/sets/neo")
        assert payload["code"] == "neo"
        assert web_api_caller.last_call is not None

    def test_get_not_found(self) -> None:
        """Un 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        client = SetsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/sets/missing")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"
