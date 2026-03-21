"""Mapper de reponse POST /cards/collection vers modeles metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.card_mapper import CardMapper
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.cards.card_collection_result import CardCollectionResult


class CardCollectionMapper:
    """Parse une reponse liste Scryfall avec champ ``not_found``."""

    def __init__(self, card_mapper: CardMapper | None = None) -> None:
        """Initialise le mapper avec un `CardMapper` injectable."""
        self._card_mapper = card_mapper or CardMapper()

    def map_collection_response(self, raw_response: Any) -> CardCollectionResult:
        """Transforme un payload collection en `CardCollectionResult`."""
        if not isinstance(raw_response, dict):
            raise ScryfallResponseFormatException(
                "Card collection response must be a dictionary.",
                response_detail=raw_response,
            )

        if raw_response.get("object") != "list":
            raise ScryfallResponseFormatException(
                "Card collection response has an invalid 'object' field.",
                response_detail=raw_response,
            )

        raw_data = raw_response.get("data")
        if not isinstance(raw_data, list):
            raise ScryfallResponseFormatException(
                "Card collection response has an invalid 'data' field.",
                response_detail=raw_response,
            )

        raw_not_found = raw_response.get("not_found", [])
        if raw_not_found is None:
            raw_not_found = []
        if not isinstance(raw_not_found, list):
            raise ScryfallResponseFormatException(
                "Card collection response has an invalid 'not_found' field.",
                response_detail=raw_response,
            )

        cards: list[Card] = []
        for index, raw_card in enumerate(raw_data):
            if not isinstance(raw_card, dict):
                raise ScryfallResponseFormatException(
                    f"Card collection 'data' item at index {index} must be a dictionary.",
                    response_detail=raw_response,
                )
            cards.append(self._card_mapper.map_card(raw_card))

        not_found_items: list[dict[str, Any]] = []
        for index, item in enumerate(raw_not_found):
            if not isinstance(item, dict):
                raise ScryfallResponseFormatException(
                    f"Card collection 'not_found' item at index {index} must be a dictionary.",
                    response_detail=raw_response,
                )
            not_found_items.append(item)

        return CardCollectionResult(
            cards=tuple(cards),
            not_found=tuple(not_found_items),
        )
