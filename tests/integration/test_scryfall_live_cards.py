"""Tests d'integration reseau : domaine Cards (API reelle Scryfall)."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.models.cards.autocomplete_result import AutocompleteResult
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.cards.card_collection_identifier import (
    CardCollectionIdentifier,
)
from baobab_scryfall_api_caller.models.common.list_response import ListResponse

from tests.integration.scryfall_live_constants import (
    AUTOCOMPLETE_QUERY,
    DOC_EXAMPLE_CARD_ID,
    JUDGMENT_SECOND_CARD_ID,
    SEARCH_QUERY_BROAD,
)

pytestmark = pytest.mark.integration


class TestScryfallLiveCards:
    """Scenarios Cards contre api.scryfall.com via la facade."""

    def test_get_by_id_returns_mapped_card(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /cards/:id — identifiant documente, champs structurants presents."""
        card = live_scryfall_client.cards.get_by_id(DOC_EXAMPLE_CARD_ID)
        assert isinstance(card, Card)
        assert card.id == DOC_EXAMPLE_CARD_ID
        assert card.name
        assert card.oracle_id

    def test_search_returns_paginated_list(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /cards/search — structure ListResponse et coherence pagination."""
        page = live_scryfall_client.cards.search(q=SEARCH_QUERY_BROAD)
        assert isinstance(page, ListResponse)
        assert len(page.data) >= 1
        assert isinstance(page.metadata.has_more, bool)
        if page.metadata.has_more:
            assert page.metadata.next_page
            assert page.metadata.next_page.startswith("http")

    def test_get_collection_post_chain(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """POST /cards/collection — petit lot d'UUIDs Judgment, mapping des cartes."""
        result = live_scryfall_client.cards.get_collection(
            identifiers=[
                CardCollectionIdentifier(id=DOC_EXAMPLE_CARD_ID),
                CardCollectionIdentifier(id=JUDGMENT_SECOND_CARD_ID),
            ],
        )
        assert len(result.cards) >= 1
        assert isinstance(result.cards[0], Card)
        assert {c.id for c in result.cards} <= {
            DOC_EXAMPLE_CARD_ID,
            JUDGMENT_SECOND_CARD_ID,
        }

    def test_autocomplete_returns_suggestions(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /cards/autocomplete — type AutocompleteResult et suggestions non vides."""
        result = live_scryfall_client.cards.autocomplete(q=AUTOCOMPLETE_QUERY)
        assert isinstance(result, AutocompleteResult)
        assert len(result.suggestions) >= 1
        assert all(isinstance(s, str) and s for s in result.suggestions)

    def test_random_without_filter(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /cards/random sans filtre — retour mappe en Card."""
        card = live_scryfall_client.cards.random()
        assert isinstance(card, Card)
        assert card.id
        assert card.name

    def test_random_with_stable_query(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /cards/random avec q stable — toujours un Card."""
        card = live_scryfall_client.cards.random(q="t:creature")
        assert isinstance(card, Card)
        assert card.id
