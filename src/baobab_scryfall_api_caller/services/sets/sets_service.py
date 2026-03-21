"""Service metier Sets (liste et recuperation unitaire)."""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from baobab_scryfall_api_caller.cache.json_response_cache import JsonResponseCache
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.card_mapper import CardMapper
from baobab_scryfall_api_caller.mappers.set_mapper import SetMapper
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.models.sets.set import Set
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.sets.sets_api_client import SetsApiClient
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)

_SET_CODE_PATTERN = re.compile(r"^[a-z0-9]{2,10}$")


class SetsService:
    """Expose les operations Sets V1 (metadonnees d'extensions et cartes par extension)."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: SetsApiClient | None = None,
        set_mapper: SetMapper | None = None,
        card_mapper: CardMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
        response_cache: JsonResponseCache | None = None,
        cacheable_get_predicate: Callable[[str, dict[str, Any] | None], bool] | None = None,
    ) -> None:
        """Initialise le service Sets avec ses dependances."""
        self.api_client = api_client or SetsApiClient(
            web_api_caller=web_api_caller,
            response_cache=response_cache,
            cacheable_get_predicate=cacheable_get_predicate,
        )
        self.set_mapper = set_mapper or SetMapper()
        self.card_mapper = card_mapper or CardMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()

    def list_sets(self, *, page: int | None = None) -> ListResponse[Set]:
        """Liste les sets Scryfall (reponse paginee)."""
        params = ScryfallRequestValidators.optional_page_params(page=page)
        payload = self.api_client.get(route="/sets", params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.set_mapper.map_set,
        )

    def get_by_code(self, set_code: str) -> Set:
        """Recupere un set par son code court Scryfall."""
        normalized = self._require_valid_set_code(set_code=set_code)
        payload = self.api_client.get(route=f"/sets/{normalized}")
        return self.set_mapper.map_set(payload)

    def get_by_id(self, set_id: str) -> Set:
        """Recupere un set par son identifiant UUID Scryfall."""
        normalized = ScryfallRequestValidators.require_uuid_string(
            value=set_id,
            field_name="set_id",
        )
        payload = self.api_client.get(route=f"/sets/{normalized}")
        return self.set_mapper.map_set(payload)

    def list_cards_in_set(
        self,
        set_code: str,
        *,
        page: int | None = None,
    ) -> ListResponse[Card]:
        """Liste paginee des cartes d'un set par code d'extension (`GET /sets/{code}/cards`)."""
        normalized = self._require_valid_set_code(set_code=set_code)
        params = ScryfallRequestValidators.optional_page_params(page=page)
        payload = self.api_client.get(route=f"/sets/{normalized}/cards", params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.card_mapper.map_card,
        )

    def list_cards_in_set_by_id(
        self,
        set_id: str,
        *,
        page: int | None = None,
    ) -> ListResponse[Card]:
        """Cartes d'un set par identifiant UUID Scryfall.

        (`GET /sets/{id}/cards`.)
        """
        normalized = ScryfallRequestValidators.require_uuid_string(
            value=set_id,
            field_name="set_id",
        )
        params = ScryfallRequestValidators.optional_page_params(page=page)
        payload = self.api_client.get(route=f"/sets/{normalized}/cards", params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.card_mapper.map_card,
        )

    @staticmethod
    def _require_valid_set_code(*, set_code: str) -> str:
        if not isinstance(set_code, str):
            raise ScryfallValidationException(
                "'set_code' must be a string.",
                params={"set_code": set_code},
            )
        normalized = set_code.strip().lower()
        if not normalized:
            raise ScryfallValidationException(
                "'set_code' cannot be empty.",
                params={"set_code": set_code},
            )
        if not _SET_CODE_PATTERN.match(normalized):
            raise ScryfallValidationException(
                "'set_code' has an invalid format (expected 2-10 alphanumeric characters).",
                params={"set_code": set_code},
            )
        return normalized
