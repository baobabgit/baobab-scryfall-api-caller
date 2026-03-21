"""Tests du client technique BulkDataApiClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallNotFoundException
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_api_client import BulkDataApiClient


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


class TestBulkDataApiClient:
    """Valide les appels HTTP du domaine bulk data."""

    def test_get_nominal(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "list", "has_more": False, "data": []},
        )
        client = BulkDataApiClient(web_api_caller=web_api_caller)
        payload = client.get(route="/bulk-data")
        assert payload["object"] == "list"

    def test_get_not_found(self) -> None:
        """Un 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        client = BulkDataApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/bulk-data/missing")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"
