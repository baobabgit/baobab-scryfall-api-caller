"""Tests de BaobabQueryParamsNormalizer."""

from __future__ import annotations

from baobab_scryfall_api_caller.client.baobab_query_params_normalizer import (
    BaobabQueryParamsNormalizer,
)


class TestBaobabQueryParamsNormalizer:
    """Conversion des query params Scryfall vers baobab-web-api-caller."""

    def test_none_returns_none(self) -> None:
        """Sans parametres, le resultat doit rester absent."""
        assert BaobabQueryParamsNormalizer.normalize(None) is None

    def test_int_values_become_strings(self) -> None:
        """Les entiers doivent etre serialises en chaines."""
        result = BaobabQueryParamsNormalizer.normalize({"page": 2})
        assert result == {"page": "2"}

    def test_list_values_become_string_sequences(self) -> None:
        """Les listes doivent devenir des sequences de chaines."""
        result = BaobabQueryParamsNormalizer.normalize({"id": ["a", "b"]})
        assert result == {"id": ["a", "b"]}
