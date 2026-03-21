"""Tests du client HTTP partage ScryfallHttpClient."""

from __future__ import annotations

from typing import Any

from baobab_web_api_caller.core.baobab_response import BaobabResponse

from baobab_scryfall_api_caller.client.scryfall_http_client import ScryfallHttpClient
from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
)


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

    def post(
        self,
        *,
        route: str,
        params: dict[str, Any] | None,
        json: dict[str, Any],
        headers: dict[str, str],
    ) -> Any:
        """Simule la methode post du caller HTTP."""
        self.last_call = {"route": route, "params": params, "json": json, "headers": headers}
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


class BaobabStyleTransportStub:
    """Simule BaobabServiceCaller (path, query_params, json_body) sans reseau."""

    def __init__(self, *, response: Any) -> None:
        self.response = response
        self.last_get: dict[str, Any] | None = None
        self.last_post: dict[str, Any] | None = None

    def get(
        self,
        path: str,
        *,
        query_params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Signature alignee sur BaobabServiceCaller.get."""
        self.last_get = {"path": path, "query_params": query_params, "headers": headers}
        return self.response

    def post(
        self,
        path: str,
        *,
        query_params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        json_body: object | None = None,
    ) -> Any:
        """Signature alignee sur BaobabServiceCaller.post."""
        self.last_post = {
            "path": path,
            "query_params": query_params,
            "headers": headers,
            "json_body": json_body,
        }
        return self.response


class FakeBrokenJsonResponse:
    """Double de reponse avec json non dict."""

    status_code = 200

    @staticmethod
    def json() -> list[str]:
        """Retourne volontairement un type invalide."""
        return ["invalid"]


class TestScryfallHttpClient:
    """Valide les scenarios d'appel et de traduction d'erreurs."""

    def test_get_with_baobab_response_json_data(self) -> None:
        """Reponses BaobabResponse (json_data) doivent etre mappees en dict."""
        response = BaobabResponse(
            status_code=200,
            headers={},
            json_data={"id": "abc", "object": "card", "name": "Test"},
        )
        stub = BaobabStyleTransportStub(response=response)
        client = ScryfallHttpClient(web_api_caller=stub)
        payload = client.get(route="/cards/abc")
        assert payload["id"] == "abc"
        assert stub.last_get is not None
        assert stub.last_get["path"] == "/cards/abc"

    def test_post_with_baobab_response_json_data(self) -> None:
        """POST avec reponse BaobabResponse doit extraire json_data."""
        response = BaobabResponse(
            status_code=200,
            headers={},
            json_data={"object": "list", "data": []},
        )
        stub = BaobabStyleTransportStub(response=response)
        client = ScryfallHttpClient(web_api_caller=stub)
        payload = client.post(route="/cards/collection", payload={"identifiers": []})
        assert payload["object"] == "list"
        assert stub.last_post is not None
        assert stub.last_post["json_body"] == {"identifiers": []}

    def test_get_nominal_dict_payload(self) -> None:
        """Le client doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(response={"id": "x", "name": "y"})
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        payload = client.get(route="/resource")
        assert payload["id"] == "x"
        assert web_api_caller.last_call is not None
        assert web_api_caller.last_call["headers"]["Accept"] == "application/json"

    def test_get_not_found_payload(self) -> None:
        """Un payload d'erreur 404 doit etre traduit en not-found."""
        web_api_caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"}
        )
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/missing")
        except ScryfallNotFoundException as exception:
            assert exception.http_status == 404
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_get_transport_error(self) -> None:
        """Une erreur transport doit etre traduite en erreur de requete."""
        web_api_caller = FakeWebApiCaller(error=RuntimeError("Connection aborted"))
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/resource")
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
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/resource")
        except ScryfallRequestException as exception:
            assert exception.http_status == 500
        else:
            assert False, "Expected ScryfallRequestException"

    def test_get_malformed_response(self) -> None:
        """Une reponse mal formee doit lever une erreur de format."""
        web_api_caller = FakeWebApiCaller(response="not-a-dict")
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/resource")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_post_nominal_dict_payload(self) -> None:
        """Le POST doit retourner un payload dict nominal."""
        web_api_caller = FakeWebApiCaller(response={"object": "list", "data": []})
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        payload = client.post(route="/batch", payload={"k": "v"})
        assert payload["object"] == "list"

    def test_post_transport_error(self) -> None:
        """Une erreur transport en POST doit etre traduite."""
        web_api_caller = FakeWebApiCaller(error=RuntimeError("Post failed"))
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.post(route="/batch", payload={})
        except ScryfallRequestException as exception:
            assert "Post failed" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_post_http_error_payload(self) -> None:
        """Un POST avec statut HTTP >= 400 doit lever une exception metier."""
        web_api_caller = FakeWebApiCaller(
            response=FakeResponse(
                status_code=503,
                payload={"object": "error", "details": "Service unavailable"},
            )
        )
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.post(route="/cards/collection", payload={"identifiers": []})
        except ScryfallRequestException as exception:
            assert exception.http_status == 503
        else:
            assert False, "Expected ScryfallRequestException"

    def test_post_object_error_without_http_status_field(self) -> None:
        """Erreur Scryfall dans le corps avec statut HTTP nominal."""
        web_api_caller = FakeWebApiCaller(
            response=FakeResponse(
                status_code=200,
                payload={"object": "error", "status": 422, "details": "Invalid"},
            )
        )
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.post(route="/cards/collection", payload={"identifiers": []})
        except ScryfallRequestException as exception:
            assert exception.http_status == 422
        else:
            assert False, "Expected ScryfallRequestException"

    def test_post_error_without_details_uses_fallback_message(self) -> None:
        """Message de reponse d'erreur sans chaine `details` explicite."""
        web_api_caller = FakeWebApiCaller(
            response=FakeResponse(
                status_code=400,
                payload={"object": "error"},
            )
        )
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.post(route="/cards/collection", payload={"identifiers": []})
        except ScryfallRequestException as exception:
            assert exception.http_status == 400
            assert "400" in exception.message or "failed" in exception.message.lower()
        else:
            assert False, "Expected ScryfallRequestException"

    def test_post_malformed_response(self) -> None:
        """Un POST dont la reponse n'est pas un dict exploitable doit echouer."""
        web_api_caller = FakeWebApiCaller(response="not-json")
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.post(route="/batch", payload={})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_get_json_method_non_dict_raises(self) -> None:
        """Une reponse json non dict doit lever une erreur de format."""
        web_api_caller = FakeWebApiCaller(response=FakeBrokenJsonResponse())
        client = ScryfallHttpClient(web_api_caller=web_api_caller)
        try:
            client.get(route="/resource")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
