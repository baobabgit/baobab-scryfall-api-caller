"""Tests de AutocompleteMapper."""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.autocomplete_mapper import AutocompleteMapper


class TestAutocompleteMapper:
    """Valide le mapping des reponses autocomplete."""

    def test_map_autocomplete_nominal(self) -> None:
        """Un payload catalogue valide produit un AutocompleteResult."""
        mapper = AutocompleteMapper()
        result = mapper.map_autocomplete(
            {
                "object": "catalog",
                "id": "abc",
                "uri": "/cards/autocomplete",
                "total_values": 2,
                "data": ["Lightning Bolt", "Lightning Helix"],
            }
        )
        assert result.suggestions == ("Lightning Bolt", "Lightning Helix")
        assert result.total_values == 2

    def test_map_autocomplete_without_total_values(self) -> None:
        """total_values peut etre absent."""
        mapper = AutocompleteMapper()
        result = mapper.map_autocomplete(
            {
                "object": "catalog",
                "data": [],
            }
        )
        assert result.suggestions == ()
        assert result.total_values is None

    def test_map_autocomplete_rejects_non_dict(self) -> None:
        """Un corps non dict doit lever."""
        mapper = AutocompleteMapper()
        try:
            mapper.map_autocomplete([])
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_autocomplete_rejects_wrong_object(self) -> None:
        """object != catalog doit lever."""
        mapper = AutocompleteMapper()
        try:
            mapper.map_autocomplete({"object": "list", "data": []})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_autocomplete_rejects_non_list_data(self) -> None:
        """data doit etre une liste."""
        mapper = AutocompleteMapper()
        try:
            mapper.map_autocomplete({"object": "catalog", "data": "x"})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_autocomplete_rejects_non_string_entry(self) -> None:
        """Chaque entree doit etre une chaine."""
        mapper = AutocompleteMapper()
        try:
            mapper.map_autocomplete({"object": "catalog", "data": [1]})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_autocomplete_rejects_invalid_total_values(self) -> None:
        """total_values negatif ou non entier doit lever."""
        mapper = AutocompleteMapper()
        try:
            mapper.map_autocomplete({"object": "catalog", "data": [], "total_values": -1})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
