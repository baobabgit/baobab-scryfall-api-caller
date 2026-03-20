"""Parsing des reponses de liste Scryfall vers des modeles internes."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.models.common.pagination_metadata import PaginationMetadata
from baobab_scryfall_api_caller.models.common.scryfall_warning import ScryfallWarning
from baobab_scryfall_api_caller.pagination.scryfall_list_response_validator import (
    ScryfallListResponseValidator,
)

T = TypeVar("T")


class ScryfallListResponseParser:
    """Parse une reponse brute en `ListResponse[T]`."""

    def __init__(self, validator: ScryfallListResponseValidator | None = None) -> None:
        """Initialise le parseur avec un validateur injectable."""
        self.validator = validator or ScryfallListResponseValidator()

    def parse(
        self,
        *,
        raw_response: Any,
        item_mapper: Callable[[dict[str, Any]], T],
    ) -> ListResponse[T]:
        """Valide et parse une reponse de liste Scryfall."""
        validated = self.validator.validate(raw_response)
        data = [item_mapper(raw_item) for raw_item in validated["data"]]
        raw_warnings = validated.get("warnings", [])
        warnings = tuple(ScryfallWarning.from_raw(item) for item in raw_warnings)

        metadata = PaginationMetadata(
            has_more=validated.get("has_more", False),
            next_page=validated.get("next_page"),
            total_cards=validated.get("total_cards"),
            warnings=warnings,
        )

        return ListResponse(
            data=data,
            metadata=metadata,
            object_type=validated.get("object", "list"),
        )
