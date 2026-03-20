"""Tests du client technique RulingsApiClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallNotFoundException
from baobab_scryfall_api_caller.services.rulings.rulings_api_client import RulingsApiClient


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


class TestRulingsApiClient:
    """Valide les appels HTTP du domaine rulings."""

    def test_get_nominal(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        cid = "00000000-0000-4000-8000-000000000001"
        web_api_caller = FakeWebApiCaller(
            response={"object": "list", "has_more": False, "data": []},
        )
        client = RulingsApiClient(web_api_caller=web_api_caller)
        payload = client.get(route=f"/cards/{cid}/rulings")
        assert payload["object"] == "list"
        assert web_api_caller.last_call is not None

    def test_get_not_found(self) -> None:
        """Un 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        client = RulingsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/cards/x/rulings")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"
