"""Tests de surface API V1 du domaine Cards (non regression signatures)."""

from __future__ import annotations

import inspect

from baobab_scryfall_api_caller.services.cards.cards_service import CardsService


class TestCardsServiceV1Surface:
    """Garantit l'exposition stable des operations Cards V1."""

    def test_public_methods_match_v1_contract(self) -> None:
        """Les methodes publiques attendues pour la V1 Cards sont presentes."""
        expected = frozenset(
            {
                "get_by_id",
                "get_by_mtgo_id",
                "get_by_cardmarket_id",
                "get_by_set_and_number",
                "get_named",
                "search",
                "autocomplete",
                "random",
                "get_collection",
            }
        )
        public = {
            name
            for name, _ in inspect.getmembers(CardsService, predicate=inspect.isfunction)
            if not name.startswith("_")
        }
        assert expected <= public, f"Missing public API: {expected - public}"
