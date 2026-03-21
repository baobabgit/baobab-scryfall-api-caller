"""Client technique pour appeler les endpoints Catalogs via baobab-web-api-caller."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.client.scryfall_http_client import ScryfallHttpClient
from baobab_scryfall_api_caller.mappers.scryfall_error_translator import ScryfallErrorTranslator


class CatalogsApiClient:
    """Encapsule les appels HTTP du domaine catalogs."""

    def __init__(
        self,
        *,
        web_api_caller: Any,
        error_translator: ScryfallErrorTranslator | None = None,
    ) -> None:
        """Initialise le client technique Catalogs."""
        self._http = ScryfallHttpClient(
            web_api_caller=web_api_caller,
            error_translator=error_translator or ScryfallErrorTranslator(),
        )

    def get(self, *, route: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute un GET et retourne un payload dictionnaire."""
        return self._http.get(route=route, params=params)
