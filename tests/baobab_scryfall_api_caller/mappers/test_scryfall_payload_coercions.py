"""Tests des coercitions de champs Scryfall partagees."""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.scryfall_payload_coercions import (
    as_bool,
    as_int,
    as_optional_int,
    as_optional_str,
)


class TestScryfallPayloadCoercions:
    """Valide les helpers de coercition."""

    def test_as_optional_str_none(self) -> None:
        """None doit rester None."""
        assert as_optional_str(None, invalid_message="x") is None

    def test_as_optional_str_invalid(self) -> None:
        """Une valeur non str doit lever."""
        try:
            as_optional_str(1, invalid_message="bad")
        except ScryfallResponseFormatException as exception:
            assert exception.response_detail == 1
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_as_optional_int_invalid(self) -> None:
        """Une valeur non int optionnelle doit lever."""
        try:
            as_optional_int("1", invalid_message="bad")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_as_int_with_default(self) -> None:
        """None doit retourner la valeur par defaut."""
        assert as_int(None, default=3, invalid_message="bad") == 3

    def test_as_int_invalid(self) -> None:
        """Une valeur non int doit lever."""
        try:
            as_int("2", default=0, invalid_message="bad")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_as_bool_invalid(self) -> None:
        """Une valeur non bool doit lever."""
        try:
            as_bool(0, default=False, invalid_message="bad")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_as_bool_none_uses_default(self) -> None:
        """None doit retourner la valeur par defaut booleenne."""
        assert as_bool(None, default=True, invalid_message="bad") is True
