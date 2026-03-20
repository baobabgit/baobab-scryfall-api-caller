"""Service metier Cards (premier perimetre)."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.card_mapper import CardMapper
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.services.cards.cards_api_client import CardsApiClient


class CardsService:
    """Expose les operations Cards V1 du perimetre courant."""

    def __init__(
        self,
        *,
        web_api_caller: Any,
        api_client: CardsApiClient | None = None,
        card_mapper: CardMapper | None = None,
    ) -> None:
        """Initialise le service Cards avec ses dependances."""
        self.api_client = api_client or CardsApiClient(web_api_caller=web_api_caller)
        self.card_mapper = card_mapper or CardMapper()

    def get_by_id(self, card_id: str) -> Card:
        """Recupere une carte par identifiant Scryfall."""
        normalized_card_id = self._require_non_empty_str(card_id=card_id, field_name="card_id")
        payload = self.api_client.get(route=f"/cards/{normalized_card_id}")
        return self.card_mapper.map_card(payload)

    def get_by_mtgo_id(self, mtgo_id: int) -> Card:
        """Recupere une carte par identifiant MTGO."""
        normalized_mtgo_id = self._require_positive_int(value=mtgo_id, field_name="mtgo_id")
        payload = self.api_client.get(route=f"/cards/mtgo/{normalized_mtgo_id}")
        return self.card_mapper.map_card(payload)

    def get_by_cardmarket_id(self, cardmarket_id: int) -> Card:
        """Recupere une carte par identifiant Cardmarket."""
        normalized_cardmarket_id = self._require_positive_int(
            value=cardmarket_id,
            field_name="cardmarket_id",
        )
        payload = self.api_client.get(route=f"/cards/cardmarket/{normalized_cardmarket_id}")
        return self.card_mapper.map_card(payload)

    def get_by_set_and_number(self, set_code: str, collector_number: str) -> Card:
        """Recupere une carte par couple code set + numero de collection."""
        normalized_set_code = self._require_non_empty_str(card_id=set_code, field_name="set_code")
        normalized_collector_number = self._require_non_empty_str(
            card_id=collector_number,
            field_name="collector_number",
        )
        payload = self.api_client.get(
            route=f"/cards/{normalized_set_code.lower()}/{normalized_collector_number}",
        )
        return self.card_mapper.map_card(payload)

    def get_named(self, *, exact: str | None = None, fuzzy: str | None = None) -> Card:
        """Recupere une carte via endpoint named (exact ou fuzzy)."""
        if exact and fuzzy:
            raise ScryfallValidationException(
                "Only one of 'exact' or 'fuzzy' can be provided for named lookup.",
                params={"exact": exact, "fuzzy": fuzzy},
            )
        if not exact and not fuzzy:
            raise ScryfallValidationException(
                "One of 'exact' or 'fuzzy' must be provided for named lookup.",
                params={"exact": exact, "fuzzy": fuzzy},
            )

        params: dict[str, str]
        if exact is not None:
            normalized_exact = self._require_non_empty_str(card_id=exact, field_name="exact")
            params = {"exact": normalized_exact}
        else:
            normalized_fuzzy = self._require_non_empty_str(card_id=fuzzy, field_name="fuzzy")
            params = {"fuzzy": normalized_fuzzy}

        payload = self.api_client.get(route="/cards/named", params=params)
        return self.card_mapper.map_card(payload)

    @staticmethod
    def _require_non_empty_str(*, card_id: str | None, field_name: str) -> str:
        if not isinstance(card_id, str):
            raise ScryfallValidationException(
                f"'{field_name}' must be a string.",
                params={field_name: card_id},
            )
        normalized = card_id.strip()
        if not normalized:
            raise ScryfallValidationException(
                f"'{field_name}' cannot be empty.",
                params={field_name: card_id},
            )
        return normalized

    @staticmethod
    def _require_positive_int(*, value: int, field_name: str) -> int:
        if not isinstance(value, int):
            raise ScryfallValidationException(
                f"'{field_name}' must be an integer.",
                params={field_name: value},
            )
        if value <= 0:
            raise ScryfallValidationException(
                f"'{field_name}' must be a positive integer.",
                params={field_name: value},
            )
        return value
