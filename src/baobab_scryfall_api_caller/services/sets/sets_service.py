"""Service metier Sets (liste et recuperation unitaire)."""

from __future__ import annotations

import re
from typing import Any
from uuid import UUID

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.set_mapper import SetMapper
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.models.sets.set import Set
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.sets.sets_api_client import SetsApiClient

_SET_CODE_PATTERN = re.compile(r"^[a-z0-9]{2,10}$")


class SetsService:
    """Expose les operations Sets V1 du perimetre courant."""

    def __init__(
        self,
        *,
        web_api_caller: Any,
        api_client: SetsApiClient | None = None,
        set_mapper: SetMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
    ) -> None:
        """Initialise le service Sets avec ses dependances."""
        self.api_client = api_client or SetsApiClient(web_api_caller=web_api_caller)
        self.set_mapper = set_mapper or SetMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()

    def list_sets(self, *, page: int | None = None) -> ListResponse[Set]:
        """Liste les sets Scryfall (reponse paginee)."""
        params = self._build_page_params(page=page)
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
        normalized = self._require_scryfall_uuid(value=set_id, field_name="set_id")
        payload = self.api_client.get(route=f"/sets/{normalized}")
        return self.set_mapper.map_set(payload)

    @staticmethod
    def _build_page_params(*, page: int | None) -> dict[str, int] | None:
        if page is None:
            return None
        if not isinstance(page, int):
            raise ScryfallValidationException(
                "'page' must be an integer.",
                params={"page": page},
            )
        if page < 1:
            raise ScryfallValidationException(
                "'page' must be a positive integer.",
                params={"page": page},
            )
        return {"page": page}

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

    @staticmethod
    def _require_scryfall_uuid(*, value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ScryfallValidationException(
                f"'{field_name}' must be a string.",
                params={field_name: value},
            )
        stripped = value.strip()
        if not stripped:
            raise ScryfallValidationException(
                f"'{field_name}' cannot be empty.",
                params={field_name: value},
            )
        try:
            canonical = str(UUID(stripped))
        except ValueError as error:
            raise ScryfallValidationException(
                f"'{field_name}' must be a valid UUID.",
                params={field_name: value},
            ) from error
        return canonical
