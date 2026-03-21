"""Client technique pour appeler les endpoints Catalogs via baobab-web-api-caller."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from baobab_scryfall_api_caller.cache.json_response_cache import JsonResponseCache
from baobab_scryfall_api_caller.client.scryfall_http_client import ScryfallHttpClient
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.mappers.scryfall_error_translator import ScryfallErrorTranslator


class CatalogsApiClient:
    """Encapsule les appels HTTP du domaine catalogs."""

    def __init__(
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        error_translator: ScryfallErrorTranslator | None = None,
        response_cache: JsonResponseCache | None = None,
        cacheable_get_predicate: Callable[[str, dict[str, Any] | None], bool] | None = None,
    ) -> None:
        """Initialise le client technique Catalogs."""
        self._http = ScryfallHttpClient(
            web_api_caller=web_api_caller,
            error_translator=error_translator or ScryfallErrorTranslator(),
            response_cache=response_cache,
            cacheable_get_predicate=cacheable_get_predicate,
        )

    def get(self, *, route: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute un GET et retourne un payload dictionnaire."""
        return self._http.get(route=route, params=params)
