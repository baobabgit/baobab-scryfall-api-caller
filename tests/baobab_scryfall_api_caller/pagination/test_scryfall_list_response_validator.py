"""Tests de ScryfallListResponseValidator."""

from baobab_scryfall_api_caller.exceptions import (
    ScryfallPaginationException,
    ScryfallResponseFormatException,
)
from baobab_scryfall_api_caller.pagination import ScryfallListResponseValidator


class TestScryfallListResponseValidator:
    """Valide la robustesse de validation des payloads de liste."""

    def test_valid_payload(self) -> None:
        """Le payload nominal doit etre accepte."""
        validator = ScryfallListResponseValidator()
        raw = {
            "object": "list",
            "data": [{"id": "x"}],
            "has_more": True,
            "next_page": "https://api.scryfall.com/cards/search?page=2",
            "warnings": ["soft warning"],
        }
        validated = validator.validate(raw)
        assert validated is raw

    def test_empty_list_payload(self) -> None:
        """Une liste vide reste valide."""
        validator = ScryfallListResponseValidator()
        raw = {"object": "list", "data": [], "has_more": False}
        validated = validator.validate(raw)
        assert not validated["data"]

    def test_has_more_true_without_next_page_raises(self) -> None:
        """has_more=true sans next_page doit lever une erreur pagination."""
        validator = ScryfallListResponseValidator()
        try:
            validator.validate({"object": "list", "data": [], "has_more": True})
        except ScryfallPaginationException:
            assert True
        else:
            assert False, "Expected ScryfallPaginationException"

    def test_invalid_object_field_raises(self) -> None:
        """Un objet non list doit lever une erreur de format."""
        validator = ScryfallListResponseValidator()
        try:
            validator.validate({"object": "card", "data": []})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_invalid_data_type_raises(self) -> None:
        """Un champ data invalide doit lever une erreur de format."""
        validator = ScryfallListResponseValidator()
        try:
            validator.validate({"object": "list", "data": {}})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_invalid_has_more_type_raises(self) -> None:
        """Un has_more non booleen doit etre rejete."""
        validator = ScryfallListResponseValidator()
        try:
            validator.validate({"object": "list", "data": [], "has_more": "yes"})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
