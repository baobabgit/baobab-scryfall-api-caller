"""Tests du service metier CardsService."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.services.cards import CardsService


class FakeWebApiCaller:
    """Double de test du transport HTTP."""

    def __init__(self, mapping: dict[str, Any]) -> None:
        self.mapping = mapping

    def get(self, *, route: str, params: dict[str, Any] | None, headers: dict[str, str]) -> Any:
        """Simule la methode get du caller HTTP."""
        key = f"{route}|{params}"
        assert headers.get("Accept") == "application/json"
        value = self.mapping.get(key)
        if isinstance(value, Exception):
            raise value
        if value is None:
            return {"object": "error", "status": 404, "details": "Not found"}
        return value


class TestCardsService:
    """Valide le service Cards sur le perimetre de feature."""

    def test_get_by_id_success(self) -> None:
        """La lecture par Scryfall id doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/card-id|None": {"id": "card-id", "name": "Black Lotus"},
                }
            )
        )
        card = service.get_by_id("card-id")
        assert card.id == "card-id"
        assert card.name == "Black Lotus"

    def test_get_by_mtgo_id_success(self) -> None:
        """La lecture par mtgo id doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/mtgo/123|None": {"id": "card-id", "name": "Black Lotus"},
                }
            )
        )
        card = service.get_by_mtgo_id(123)
        assert card.name == "Black Lotus"

    def test_get_by_cardmarket_id_success(self) -> None:
        """La lecture par cardmarket id doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/cardmarket/456|None": {"id": "card-id", "name": "Black Lotus"},
                }
            )
        )
        card = service.get_by_cardmarket_id(456)
        assert card.id == "card-id"

    def test_get_by_set_and_number_success(self) -> None:
        """La lecture par set + numero doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/lea/233|None": {"id": "card-id", "name": "Black Lotus"},
                }
            )
        )
        card = service.get_by_set_and_number("LEA", "233")
        assert card.name == "Black Lotus"

    def test_get_named_exact_success(self) -> None:
        """La lecture nommee en mode exact doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/named|{'exact': 'Black Lotus'}": {
                        "id": "card-id",
                        "name": "Black Lotus",
                    },
                }
            )
        )
        card = service.get_named(exact="Black Lotus")
        assert card.id == "card-id"

    def test_get_named_fuzzy_success(self) -> None:
        """La lecture nommee en mode fuzzy doit fonctionner."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/named|{'fuzzy': 'Black L'}": {"id": "card-id", "name": "Black Lotus"},
                }
            )
        )
        card = service.get_named(fuzzy="Black L")
        assert card.name == "Black Lotus"

    def test_local_validation_invalid_named_combination(self) -> None:
        """Fuzzy + exact simultanes doivent etre rejetes."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_named(exact="Black Lotus", fuzzy="Black L")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_named_requires_exact_or_fuzzy(self) -> None:
        """Sans exact ni fuzzy, la validation locale doit echouer."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_named()
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_by_mtgo_id_must_be_positive(self) -> None:
        """Un identifiant MTGO non strictement positif doit etre rejete."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_by_mtgo_id(0)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_get_named_exact_must_be_string(self) -> None:
        """Le mode exact doit recevoir une chaine."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_named(exact=123)  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_local_validation_empty_string(self) -> None:
        """Une chaine vide doit etre rejetee en validation locale."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_by_id(" ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_local_validation_type_error(self) -> None:
        """Un type invalide doit etre rejete en validation locale."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_by_mtgo_id("123")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_not_found(self) -> None:
        """Une carte absente doit remonter une exception not-found."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.get_by_id("unknown")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_transport_error(self) -> None:
        """Une erreur transport doit etre traduite par la couche metier."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/card-id|None": RuntimeError("Socket closed")}
            )
        )
        try:
            service.get_by_id("card-id")
        except ScryfallRequestException as exception:
            assert "Socket closed" in str(exception)
        else:
            assert False, "Expected translated transport exception"

    def test_response_malformed(self) -> None:
        """Une reponse invalide doit remonter une erreur de format."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(mapping={"/cards/card-id|None": {"id": "card-id"}})
        )
        try:
            service.get_by_id("card-id")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
