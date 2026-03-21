"""Tests du service metier CardsService."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallPaginationException,
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

    def test_search_nominal(self) -> None:
        """La recherche renvoie une ListResponse de cartes mappees."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [{"id": "c1", "name": "Shivan Dragon"}],
            "total_cards": 1,
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/search|{'q': 'type:creature'}": list_payload}
            )
        )
        page = service.search(q="type:creature")
        assert page.data[0].id == "c1"
        assert page.metadata.has_more is False
        assert page.next_page is None
        assert page.metadata.total_cards == 1

    def test_search_paginated(self) -> None:
        """La recherche avec page transmet page et parse has_more / next_page."""
        list_payload = {
            "object": "list",
            "has_more": True,
            "next_page": "https://api.scryfall.com/cards/search?q=a&page=2",
            "data": [{"id": "c1", "name": "A"}],
            "total_cards": 100,
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/search|{'q': 'a', 'page': 2}": list_payload}
            )
        )
        page = service.search(q="a", page=2)
        assert page.has_more is True
        assert page.next_page is not None
        assert "page=2" in page.next_page

    def test_search_empty_result(self) -> None:
        """Une recherche sans resultat renvoie une liste vide valide."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [],
            "total_cards": 0,
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/search|{'q': 'name:nope_xyz_123'}": list_payload}
            )
        )
        page = service.search(q="name:nope_xyz_123")
        assert page.data == []
        assert page.metadata.total_cards == 0

    def test_search_malformed_list_response(self) -> None:
        """Une liste API invalide doit lever ScryfallResponseFormatException."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/search|{'q': 'x'}": {"object": "card", "id": "x"}}
            )
        )
        try:
            service.search(q="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_search_pagination_inconsistent(self) -> None:
        """has_more sans next_page doit lever ScryfallPaginationException."""
        list_payload = {
            "object": "list",
            "has_more": True,
            "data": [],
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(mapping={"/cards/search|{'q': 'x'}": list_payload})
        )
        try:
            service.search(q="x")
        except ScryfallPaginationException:
            assert True
        else:
            assert False, "Expected ScryfallPaginationException"

    def test_search_malformed_card_in_data(self) -> None:
        """Un element de data non mappable doit lever."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [{"id": "c1"}],
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(mapping={"/cards/search|{'q': 'x'}": list_payload})
        )
        try:
            service.search(q="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_search_validation_page_type(self) -> None:
        """Un page non entier doit etre rejete localement."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.search(q="a", page="2")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_autocomplete_nominal(self) -> None:
        """Autocomplete renvoie des suggestions typees."""
        payload = {
            "object": "catalog",
            "total_values": 1,
            "data": ["Lightning Bolt"],
        }
        service = CardsService(
            web_api_caller=FakeWebApiCaller(mapping={"/cards/autocomplete|{'q': 'lig'}": payload})
        )
        result = service.autocomplete(q="lig")
        assert result.suggestions == ("Lightning Bolt",)
        assert result.total_values == 1

    def test_autocomplete_validation_empty(self) -> None:
        """Une query vide doit etre rejetee."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.autocomplete(q="   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_autocomplete_invalid_payload(self) -> None:
        """Une reponse autocomplete invalide doit lever."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/autocomplete|{'q': 'x'}": {"object": "list", "data": []}}
            )
        )
        try:
            service.autocomplete(q="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_random_nominal(self) -> None:
        """Random sans filtre renvoie une carte."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/random|None": {"id": "r1", "name": "Random"}}
            )
        )
        card = service.random()
        assert card.id == "r1"

    def test_random_with_q(self) -> None:
        """Random avec DSL q transmet le parametre."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={
                    "/cards/random|{'q': 'type:creature'}": {
                        "id": "r2",
                        "name": "Grizzly Bears",
                    }
                }
            )
        )
        card = service.random(q="type:creature")
        assert card.name == "Grizzly Bears"

    def test_random_transport_error(self) -> None:
        """Une erreur transport sur random doit etre traduite."""
        service = CardsService(
            web_api_caller=FakeWebApiCaller(
                mapping={"/cards/random|None": RuntimeError("network down")}
            )
        )
        try:
            service.random()
        except ScryfallRequestException as exc:
            assert "network down" in str(exc)
        else:
            assert False, "Expected ScryfallRequestException"

    def test_random_q_validation(self) -> None:
        """Random avec q vide doit lever en validation locale."""
        service = CardsService(web_api_caller=FakeWebApiCaller(mapping={}))
        try:
            service.random(q="  ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"
