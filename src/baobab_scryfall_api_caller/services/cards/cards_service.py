"""Service metier Cards (premier perimetre)."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.autocomplete_mapper import AutocompleteMapper
from baobab_scryfall_api_caller.mappers.card_mapper import CardMapper
from baobab_scryfall_api_caller.models.cards.autocomplete_result import AutocompleteResult
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.cards.cards_api_client import CardsApiClient
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)


class CardsService:
    """Expose les operations Cards V1 du perimetre courant."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: CardsApiClient | None = None,
        card_mapper: CardMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
        autocomplete_mapper: AutocompleteMapper | None = None,
    ) -> None:
        """Initialise le service Cards avec ses dependances."""
        self.api_client = api_client or CardsApiClient(web_api_caller=web_api_caller)
        self.card_mapper = card_mapper or CardMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()
        self.autocomplete_mapper = autocomplete_mapper or AutocompleteMapper()

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

    def search(self, *, q: str, page: int | None = None) -> ListResponse[Card]:
        """Recherche de cartes via le DSL Scryfall (reponse paginee).

        Le parametre ``q`` est transmis tel quel a l'API (sans reecriture du DSL),
        hormis les validations locales de type et de chaine vide.
        """
        validated_q = ScryfallRequestValidators.require_scryfall_query_string(
            value=q,
            field_name="q",
        )
        params: dict[str, Any] = {"q": validated_q}
        page_params = ScryfallRequestValidators.optional_page_params(page=page)
        if page_params is not None:
            params.update(page_params)
        payload = self.api_client.get(route="/cards/search", params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.card_mapper.map_card,
        )

    def autocomplete(self, *, q: str) -> AutocompleteResult:
        """Propose des noms de cartes correspondant au prefixe ``q``."""
        validated_q = ScryfallRequestValidators.require_scryfall_query_string(
            value=q,
            field_name="q",
        )
        payload = self.api_client.get(
            route="/cards/autocomplete",
            params={"q": validated_q},
        )
        return self.autocomplete_mapper.map_autocomplete(payload)

    def random(self, *, q: str | None = None) -> Card:
        """Recupere une carte aleatoire, optionnellement filtree par DSL ``q``."""
        params: dict[str, str] | None = None
        if q is not None:
            validated_q = ScryfallRequestValidators.require_scryfall_query_string(
                value=q,
                field_name="q",
            )
            params = {"q": validated_q}
        payload = self.api_client.get(route="/cards/random", params=params)
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
