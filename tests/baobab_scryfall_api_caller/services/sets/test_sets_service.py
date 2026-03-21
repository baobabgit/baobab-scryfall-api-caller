"""Tests du service metier SetsService."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.sets.set import Set
from baobab_scryfall_api_caller.services.sets.sets_service import SetsService


def _valid_set_dict(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "set",
        "id": "2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f",
        "code": "neo",
        "name": "Kamigawa: Neon Dynasty",
        "set_type": "expansion",
        "card_count": 10,
        "digital": False,
        "foil_only": False,
        "nonfoil_only": False,
        "foil": True,
        "nonfoil": True,
    }
    base.update(overrides)
    return base


class FakeWebApiCaller:
    """Simule baobab-web-api-caller pour SetsService."""

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


class TestSetsService:
    """Couverture des scenarios list, get par code, get par id et validations."""

    def test_list_sets_nominal(self) -> None:
        """La liste doit parser une reponse paginee valide."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [
                _valid_set_dict(code="neo", id="11111111-1111-4111-8111-111111111111"),
                _valid_set_dict(code="mid", id="22222222-2222-4222-8222-222222222222"),
            ],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = SetsService(web_api_caller=caller)
        result = service.list_sets()
        assert len(result.data) == 2
        assert isinstance(result.data[0], Set)
        assert caller.calls[0]["route"] == "/sets"
        assert caller.calls[0]["params"] is None

    def test_list_sets_with_page_param(self) -> None:
        """Le parametre page doit etre transmis."""
        list_payload = {"object": "list", "has_more": False, "data": [_valid_set_dict()]}
        caller = FakeWebApiCaller(response=list_payload)
        service = SetsService(web_api_caller=caller)
        service.list_sets(page=2)
        assert caller.calls[0]["params"] == {"page": 2}

    def test_list_sets_invalid_page_type(self) -> None:
        """Un type de page invalide doit lever une validation."""
        caller = FakeWebApiCaller(response={})
        service = SetsService(web_api_caller=caller)
        try:
            service.list_sets(page="2")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_list_sets_invalid_page_value(self) -> None:
        """Une page <= 0 doit etre rejetee."""
        caller = FakeWebApiCaller(response={})
        service = SetsService(web_api_caller=caller)
        try:
            service.list_sets(page=0)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_code_nominal(self) -> None:
        """Recuperation par code nominal."""
        caller = FakeWebApiCaller(response=_valid_set_dict())
        service = SetsService(web_api_caller=caller)
        result = service.get_by_code(" NEO ")
        assert result.code == "neo"
        assert caller.calls[0]["route"] == "/sets/neo"

    def test_get_by_code_validation_empty(self) -> None:
        """Un code vide doit etre rejete."""
        caller = FakeWebApiCaller(response=_valid_set_dict())
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_code("   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_code_validation_invalid_pattern(self) -> None:
        """Un code hors format doit etre rejete."""
        caller = FakeWebApiCaller(response=_valid_set_dict())
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_code("no-way-too-long-code")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_code_validation_non_string(self) -> None:
        """Un code d'extension non chaine doit etre rejete."""
        caller = FakeWebApiCaller(response=_valid_set_dict())
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_code(None)  # type: ignore[arg-type]
        except ScryfallValidationException as exception:
            assert "must be a string" in exception.message
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_id_nominal(self) -> None:
        """Recuperation par UUID Scryfall."""
        set_id = "2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f"
        caller = FakeWebApiCaller(response=_valid_set_dict(id=set_id))
        service = SetsService(web_api_caller=caller)
        result = service.get_by_id(set_id.upper())
        assert result.id == set_id
        assert caller.calls[0]["route"] == f"/sets/{set_id}"

    def test_get_by_id_validation_invalid_uuid(self) -> None:
        """Un UUID invalide doit etre rejete en validation locale."""
        caller = FakeWebApiCaller(response=_valid_set_dict())
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_id("not-a-uuid")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_code_not_found(self) -> None:
        """Un 404 HTTP doit produire ScryfallNotFoundException."""
        caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_code("neo")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_http_transport_error(self) -> None:
        """Une erreur transport doit etre traduite."""
        caller = FakeWebApiCaller(error=RuntimeError("network down"))
        service = SetsService(web_api_caller=caller)
        try:
            service.get_by_code("neo")
        except ScryfallRequestException as exception:
            assert "network down" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_invalid_list_payload(self) -> None:
        """Une liste mal formee doit lever une erreur de format."""
        caller = FakeWebApiCaller(response={"object": "set", "data": []})
        service = SetsService(web_api_caller=caller)
        try:
            service.list_sets()
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_list_item_invalid_for_mapping(self) -> None:
        """Un element de liste non mappable doit echouer au mapping."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [{"object": "set", "id": "", "code": "x", "name": "y"}],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = SetsService(web_api_caller=caller)
        try:
            service.list_sets()
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
