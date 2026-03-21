"""Tests de CardCollectionMapper."""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.card_collection_mapper import CardCollectionMapper


class TestCardCollectionMapper:
    """Valide le mapping des reponses collection."""

    def test_map_nominal(self) -> None:
        """Reponse valide avec data et not_found."""
        mapper = CardCollectionMapper()
        result = mapper.map_collection_response(
            {
                "object": "list",
                "data": [{"id": "a", "name": "One"}],
                "not_found": [{"name": "Missing"}],
            }
        )
        assert result.cards[0].id == "a"
        assert result.not_found == ({"name": "Missing"},)

    def test_map_not_found_absent(self) -> None:
        """not_found absent est traite comme liste vide."""
        mapper = CardCollectionMapper()
        result = mapper.map_collection_response(
            {
                "object": "list",
                "data": [{"id": "a", "name": "One"}],
            }
        )
        assert result.not_found == ()

    def test_map_not_found_null(self) -> None:
        """not_found explicite a null est traite comme liste vide."""
        mapper = CardCollectionMapper()
        result = mapper.map_collection_response(
            {
                "data": [],
                "not_found": None,
                "object": "list",
            }
        )
        assert result.not_found == ()

    def test_map_rejects_non_dict(self) -> None:
        """Un corps non dict doit lever."""
        mapper = CardCollectionMapper()
        try:
            mapper.map_collection_response([])
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_rejects_wrong_object(self) -> None:
        """object != list doit lever."""
        mapper = CardCollectionMapper()
        try:
            mapper.map_collection_response({"object": "card", "data": []})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_rejects_invalid_data_item(self) -> None:
        """Un element de data non dict doit lever."""
        mapper = CardCollectionMapper()
        try:
            mapper.map_collection_response({"object": "list", "data": [1]})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_rejects_invalid_not_found_item(self) -> None:
        """Un element de not_found non dict doit lever."""
        mapper = CardCollectionMapper()
        try:
            mapper.map_collection_response(
                {"data": [], "not_found": ["x"], "object": "list"},
            )
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
