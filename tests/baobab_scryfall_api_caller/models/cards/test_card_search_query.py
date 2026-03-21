"""Tests de CardSearchQuery."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.models.cards.card_search_query import CardSearchQuery


class TestCardSearchQuery:
    """Serialisation stable et validations legeres."""

    def test_to_query_string_multiple_criteria_order(self) -> None:
        """L'ordre d'ajout est preserve (AND par espaces)."""
        q = CardSearchQuery().type_line("Creature").cmc(3)
        assert q.to_query_string() == "t:Creature cmc=3"
        assert q.build() == q.to_query_string()

    def test_raw_combines_with_helpers(self) -> None:
        """raw() peut combiner des operateurs arbitraires."""
        q = CardSearchQuery().raw("color:rg").name_contains("Lightning")
        assert q.to_query_string() == "color:rg name:Lightning"

    def test_set_code_lowercased(self) -> None:
        """Le code set est normalise en minuscules."""
        q = CardSearchQuery().set_code("NEO")
        assert q.to_query_string() == "s:neo"

    def test_cmc_operators(self) -> None:
        """Operateurs cmc valides."""
        assert CardSearchQuery().cmc(2, op="<").to_query_string() == "cmc<2"
        assert CardSearchQuery().cmc(0, op=">=").to_query_string() == "cmc>=0"

    def test_empty_builder_raises(self) -> None:
        """Aucun critere : erreur explicite."""
        with pytest.raises(ScryfallValidationException) as excinfo:
            CardSearchQuery().to_query_string()
        assert "no criteria" in excinfo.value.message.lower()

    def test_rejects_empty_fragments(self) -> None:
        """Fragments vides interdits."""
        with pytest.raises(ScryfallValidationException):
            CardSearchQuery().raw("   ")

    def test_rejects_invalid_cmc_op(self) -> None:
        """Operateur cmc inconnu."""
        with pytest.raises(ScryfallValidationException):
            CardSearchQuery().cmc(3, op="!=")

    def test_rejects_non_int_cmc(self) -> None:
        """cmc doit etre un int."""
        with pytest.raises(ScryfallValidationException):
            CardSearchQuery().cmc(3.0)  # type: ignore[arg-type]

    def test_repr_lists_terms(self) -> None:
        """Repr lisible pour le debug."""
        q = CardSearchQuery().type_line("Goblin")
        assert "Goblin" in repr(q)

    def test_stable_twice_same_sequence(self) -> None:
        """Deux constructions identiques produisent la meme chaine."""
        a = CardSearchQuery().oracle("flying").set_code("neo")
        b = CardSearchQuery().oracle("flying").set_code("neo")
        assert a.to_query_string() == b.to_query_string()
