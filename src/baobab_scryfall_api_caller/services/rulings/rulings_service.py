"""Service metier Rulings (rulings associes a une carte)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from baobab_scryfall_api_caller.cache.json_response_cache import JsonResponseCache
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.mappers.ruling_mapper import RulingMapper
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.models.rulings.ruling import Ruling
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.rulings.rulings_api_client import RulingsApiClient
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)


class RulingsService:
    """Expose les operations Rulings V1 (carte par identifiant Scryfall ou cles alternatives)."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: RulingsApiClient | None = None,
        ruling_mapper: RulingMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
        response_cache: JsonResponseCache | None = None,
        cacheable_get_predicate: Callable[[str, dict[str, Any] | None], bool] | None = None,
    ) -> None:
        """Initialise le service Rulings avec ses dependances."""
        self.api_client = api_client or RulingsApiClient(
            web_api_caller=web_api_caller,
            response_cache=response_cache,
            cacheable_get_predicate=cacheable_get_predicate,
        )
        self.ruling_mapper = ruling_mapper or RulingMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()

    def list_for_card_id(
        self,
        card_id: str,
        *,
        page: int | None = None,
    ) -> ListResponse[Ruling]:
        """Recupere les rulings Oracle pour une carte via son identifiant Scryfall.

        :param card_id: Identifiant UUID de la carte (chemin ``/cards/{id}/rulings``).
        :param page: Numero de page optionnel pour la pagination Scryfall.
        :return: Liste paginee de rulings.
        """
        normalized_id = ScryfallRequestValidators.require_uuid_string(
            value=card_id,
            field_name="card_id",
        )
        params = ScryfallRequestValidators.optional_page_params(page=page)
        route = f"/cards/{normalized_id}/rulings"
        payload = self.api_client.get(route=route, params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.ruling_mapper.map_ruling,
        )

    def list_for_card_multiverse_id(
        self,
        multiverse_id: int,
        *,
        page: int | None = None,
    ) -> ListResponse[Ruling]:
        """Rulings pour une carte identifiee par multiverse id.

        (`GET /cards/multiverse/{id}/rulings`.)
        """
        normalized = ScryfallRequestValidators.require_strict_positive_int(
            value=multiverse_id,
            field_name="multiverse_id",
        )
        params = ScryfallRequestValidators.optional_page_params(page=page)
        route = f"/cards/multiverse/{normalized}/rulings"
        payload = self.api_client.get(route=route, params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.ruling_mapper.map_ruling,
        )

    def list_for_card_mtgo_id(
        self,
        mtgo_id: int,
        *,
        page: int | None = None,
    ) -> ListResponse[Ruling]:
        """Rulings pour une carte identifiee par son id MTGO (`GET /cards/mtgo/{id}/rulings`)."""
        normalized = ScryfallRequestValidators.require_strict_positive_int(
            value=mtgo_id,
            field_name="mtgo_id",
        )
        params = ScryfallRequestValidators.optional_page_params(page=page)
        route = f"/cards/mtgo/{normalized}/rulings"
        payload = self.api_client.get(route=route, params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.ruling_mapper.map_ruling,
        )

    def list_for_card_arena_id(
        self,
        arena_id: str,
        *,
        page: int | None = None,
    ) -> ListResponse[Ruling]:
        """Rulings pour une carte identifiee par son id Arena (`GET /cards/arena/{id}/rulings`)."""
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=arena_id,
            field_name="arena_id",
        )
        params = ScryfallRequestValidators.optional_page_params(page=page)
        route = f"/cards/arena/{normalized}/rulings"
        payload = self.api_client.get(route=route, params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.ruling_mapper.map_ruling,
        )
