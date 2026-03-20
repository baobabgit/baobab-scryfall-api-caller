"""Tests du service metier RulingsService."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.rulings.ruling import Ruling
from baobab_scryfall_api_caller.services.rulings.rulings_service import RulingsService


def _ruling_item(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "ruling",
        "oracle_id": "abcdef01-2345-6789-abcd-ef0123456789",
        "source": "wotc",
        "published_at": "2007-02-01",
        "comment": "Ruling text.",
    }
    base.update(overrides)
    return base


class FakeWebApiCaller:
    """Simule baobab-web-api-caller pour RulingsService."""

    def __init__(self, *, response: Any = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict[str, Any]] = []

    def get(self, *, route: str, params: dict[str, Any] | None, headers: dict[str, str]) -> Any:
        """Enregistre l'appel et retourne la reponse configuree."""
        self.calls.append({"route": route, "params": params, "headers": headers})
        if self.error is not None:
            raise self.error
        return self.response


class TestRulingsService:
    """Scenarios nominal, vide, validation, erreurs et format."""

    def test_list_for_card_id_nominal(self) -> None:
        """Mapping nominal de plusieurs rulings."""
        card_id = "00000000-0000-4000-8000-000000000001"
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [_ruling_item(), _ruling_item(comment="Second.")],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = RulingsService(web_api_caller=caller)
        result = service.list_for_card_id(card_id)
        assert len(result.data) == 2
        assert all(isinstance(r, Ruling) for r in result.data)
        assert caller.calls[0]["route"] == f"/cards/{card_id}/rulings"

    def test_list_for_card_id_empty_list(self) -> None:
        """Une liste vide doit etre acceptee."""
        card_id = "00000000-0000-4000-8000-000000000002"
        list_payload = {"object": "list", "has_more": False, "data": []}
        caller = FakeWebApiCaller(response=list_payload)
        service = RulingsService(web_api_caller=caller)
        result = service.list_for_card_id(card_id)
        assert result.data == []

    def test_list_for_card_id_with_page(self) -> None:
        """Le parametre page optionnel doit etre transmis."""
        card_id = "00000000-0000-4000-8000-000000000003"
        list_payload = {"object": "list", "has_more": False, "data": []}
        caller = FakeWebApiCaller(response=list_payload)
        service = RulingsService(web_api_caller=caller)
        service.list_for_card_id(card_id, page=2)
        assert caller.calls[0]["params"] == {"page": 2}

    def test_validation_invalid_uuid(self) -> None:
        """Un identifiant carte invalide doit lever en validation locale."""
        caller = FakeWebApiCaller(response={"object": "list", "has_more": False, "data": []})
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id("not-a-uuid")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_empty_card_id(self) -> None:
        """Un identifiant vide doit etre rejete."""
        caller = FakeWebApiCaller(response={"object": "list", "has_more": False, "data": []})
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id("   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_invalid_page(self) -> None:
        """Une page invalide doit etre rejetee."""
        cid = "00000000-0000-4000-8000-000000000004"
        caller = FakeWebApiCaller(response={"object": "list", "has_more": False, "data": []})
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid, page=0)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_page_not_int(self) -> None:
        """Un type de page non entier doit etre rejete."""
        cid = "00000000-0000-4000-8000-000000000010"
        caller = FakeWebApiCaller(response={"object": "list", "has_more": False, "data": []})
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid, page="1")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_not_found(self) -> None:
        """Un 404 HTTP doit produire ScryfallNotFoundException."""
        cid = "00000000-0000-4000-8000-000000000005"
        caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid)
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_transport_error(self) -> None:
        """Une erreur transport doit etre traduite."""
        cid = "00000000-0000-4000-8000-000000000006"
        caller = FakeWebApiCaller(error=RuntimeError("timeout"))
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid)
        except ScryfallRequestException as exception:
            assert "timeout" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_malformed_list_response(self) -> None:
        """Une reponse liste invalide doit lever une erreur de format."""
        cid = "00000000-0000-4000-8000-000000000007"
        caller = FakeWebApiCaller(response={"object": "set", "data": []})
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_item_mapping_failure(self) -> None:
        """Un element de liste invalide doit echouer au mapping."""
        cid = "00000000-0000-4000-8000-000000000008"
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [_ruling_item(object="card")],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = RulingsService(web_api_caller=caller)
        try:
            service.list_for_card_id(cid)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_uuid_canonicalization(self) -> None:
        """Les UUID en entree doivent etre canonises (casse)."""
        cid_lower = "00000000-0000-4000-8000-000000000009"
        list_payload = {"object": "list", "has_more": False, "data": []}
        caller = FakeWebApiCaller(response=list_payload)
        service = RulingsService(web_api_caller=caller)
        service.list_for_card_id(cid_lower.upper())
        assert caller.calls[0]["route"] == f"/cards/{cid_lower}/rulings"
