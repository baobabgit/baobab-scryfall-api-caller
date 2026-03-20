"""Tests de ScryfallListResponseParser."""

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.pagination import ScryfallListResponseParser


class TestScryfallListResponseParser:
    """Valide le parsing et le mapping des reponses listes."""

    def test_parse_nominal_with_next_page(self) -> None:
        """Le parseur doit produire une ListResponse complete."""
        parser = ScryfallListResponseParser()
        raw_response = {
            "object": "list",
            "data": [{"name": "Black Lotus"}, {"name": "Ancestral Recall"}],
            "has_more": True,
            "next_page": "https://api.scryfall.com/cards/search?page=2",
            "total_cards": 2,
            "warnings": ["soft warning"],
        }

        parsed = parser.parse(
            raw_response=raw_response, item_mapper=lambda raw_item: raw_item["name"]
        )
        assert parsed.data == ["Black Lotus", "Ancestral Recall"]
        assert parsed.has_more is True
        assert parsed.next_page == "https://api.scryfall.com/cards/search?page=2"
        assert parsed.metadata.total_cards == 2
        assert parsed.metadata.warnings[0].message == "soft warning"

    def test_parse_empty_list(self) -> None:
        """Une liste vide doit etre parsee sans erreur."""
        parser = ScryfallListResponseParser()
        raw_response = {"object": "list", "data": [], "has_more": False}
        parsed = parser.parse(raw_response=raw_response, item_mapper=lambda raw_item: raw_item)
        assert not parsed.data
        assert parsed.has_more is False
        assert parsed.next_page is None

    def test_parse_invalid_warning_raises(self) -> None:
        """Un warning invalide doit remonter une exception metier."""
        parser = ScryfallListResponseParser()
        raw_response = {
            "object": "list",
            "data": [],
            "has_more": False,
            "warnings": [123],
        }
        try:
            parser.parse(raw_response=raw_response, item_mapper=lambda raw_item: raw_item)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
