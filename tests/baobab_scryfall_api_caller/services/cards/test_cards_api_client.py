"""Tests du client technique CardsApiClient."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
)
from baobab_scryfall_api_caller.services.cards.cards_api_client import CardsApiClient


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


class FakeResponse:
    """Double de reponse HTTP avec status + body json."""

    def __init__(self, *, status_code: int, payload: dict[str, Any]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, Any]:
        """Retourne le payload JSON simule."""
        return self._payload


class TestCardsApiClient:
    """Valide les scenarios d'appel et de traduction d'erreurs."""

    def test_get_nominal_dict_payload(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(response={"id": "card-id", "name": "Black Lotus"})
        client = CardsApiClient(web_api_caller=web_api_caller)
        payload = client.get(route="/cards/card-id")
        assert payload["id"] == "card-id"
        assert web_api_caller.last_call is not None
        assert web_api_caller.last_call["headers"]["Accept"] == "application/json"

    def test_get_not_found_payload(self) -> None:
        """Un payload d'erreur 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"}
        )
        client = CardsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/cards/missing-id")
        except ScryfallNotFoundException as exception:
            assert exception.http_status == 404
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_get_transport_error(self) -> None:
        """Une erreur transport doit etre traduite en erreur de requete."""
        web_api_caller = FakeWebApiCaller(error=RuntimeError("Connection aborted"))
        client = CardsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/cards/card-id")
        except ScryfallRequestException as exception:
            assert "Connection aborted" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_get_http_error_response(self) -> None:
        """Un status HTTP >= 400 doit produire une exception metier."""
        web_api_caller = FakeWebApiCaller(
            response=FakeResponse(
                status_code=500,
                payload={"object": "error", "details": "Internal server error"},
            )
        )
        client = CardsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/cards/card-id")
        except ScryfallRequestException as exception:
            assert exception.http_status == 500
        else:
            assert False, "Expected ScryfallRequestException"

    def test_get_malformed_response(self) -> None:
        """Une reponse mal formee doit lever une erreur de format."""
        web_api_caller = FakeWebApiCaller(response="not-a-dict")
        client = CardsApiClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/cards/card-id")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
