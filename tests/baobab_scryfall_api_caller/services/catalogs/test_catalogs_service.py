"""Tests du service metier CatalogsService."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog
from baobab_scryfall_api_caller.services.catalogs.catalogs_service import CatalogsService


def _catalog_response(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "catalog",
        "uri": "https://api.scryfall.com/catalog/card-names",
        "total_values": 1,
        "data": ["Lightning Bolt"],
    }
    base.update(overrides)
    return base


class FakeWebApiCaller:
    """Simule baobab-web-api-caller pour CatalogsService."""

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


class TestCatalogsService:
    """Scenarios generiques, helpers, validation et erreurs."""

    def test_get_catalog_nominal(self) -> None:
        """Acces generique nominal."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        result = service.get_catalog("  CARD-NAMES ")
        assert isinstance(result, Catalog)
        assert result.catalog_key == "card-names"
        assert result.values == ("Lightning Bolt",)
        assert caller.calls[0]["route"] == "/catalog/card-names"

    def test_get_catalog_empty_data(self) -> None:
        """Catalogue avec liste vide."""
        caller = FakeWebApiCaller(
            response=_catalog_response(total_values=0, data=[]),
        )
        service = CatalogsService(web_api_caller=caller)
        result = service.get_catalog("word-bank")
        assert result.values == ()

    def test_get_card_names_helper(self) -> None:
        """Helper get_card_names delegue au generique."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        result = service.get_card_names()
        assert result.catalog_key == "card-names"
        assert caller.calls[0]["route"] == "/catalog/card-names"

    def test_get_creature_types_helper(self) -> None:
        """Helper creature-types."""
        caller = FakeWebApiCaller(
            response=_catalog_response(
                uri="https://api.scryfall.com/catalog/creature-types",
                data=["Human"],
            ),
        )
        service = CatalogsService(web_api_caller=caller)
        result = service.get_creature_types()
        assert result.catalog_key == "creature-types"
        assert caller.calls[0]["route"] == "/catalog/creature-types"

    def test_get_land_types_helper(self) -> None:
        """Helper land-types."""
        caller = FakeWebApiCaller(
            response=_catalog_response(
                uri="https://api.scryfall.com/catalog/land-types",
                data=["Island"],
            ),
        )
        service = CatalogsService(web_api_caller=caller)
        service.get_land_types()
        assert caller.calls[0]["route"] == "/catalog/land-types"

    def test_get_card_types_helper(self) -> None:
        """Helper card-types."""
        caller = FakeWebApiCaller(
            response=_catalog_response(
                uri="https://api.scryfall.com/catalog/card-types",
                data=["Creature"],
            ),
        )
        service = CatalogsService(web_api_caller=caller)
        service.get_card_types()
        assert caller.calls[0]["route"] == "/catalog/card-types"

    def test_get_artist_names_helper(self) -> None:
        """Helper artist-names."""
        caller = FakeWebApiCaller(
            response=_catalog_response(
                uri="https://api.scryfall.com/catalog/artist-names",
                data=["Artist"],
            ),
        )
        service = CatalogsService(web_api_caller=caller)
        service.get_artist_names()
        assert caller.calls[0]["route"] == "/catalog/artist-names"

    def test_validation_catalog_key_not_string(self) -> None:
        """Une cle non chaine doit etre rejetee."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog(123)  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_empty_key(self) -> None:
        """Une cle vide doit etre rejetee."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog("   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_invalid_key_pattern(self) -> None:
        """Un motif de cle invalide doit etre rejete."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog("bad_key")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_key_too_long(self) -> None:
        """Une cle trop longue doit etre rejetee."""
        caller = FakeWebApiCaller(response=_catalog_response())
        service = CatalogsService(web_api_caller=caller)
        long_key = "x" * 81
        try:
            service.get_catalog(long_key)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_not_found(self) -> None:
        """Un 404 HTTP doit produire ScryfallNotFoundException."""
        caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog("card-names")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_transport_error(self) -> None:
        """Une erreur transport doit etre traduite."""
        caller = FakeWebApiCaller(error=RuntimeError("boom"))
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog("card-names")
        except ScryfallRequestException as exception:
            assert "boom" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_invalid_response_shape(self) -> None:
        """Une reponse non catalogue doit lever une erreur de format."""
        caller = FakeWebApiCaller(response={"object": "list", "data": []})
        service = CatalogsService(web_api_caller=caller)
        try:
            service.get_catalog("card-names")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
