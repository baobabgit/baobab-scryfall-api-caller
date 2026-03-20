"""Validation des structures de liste Scryfall."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallPaginationException,
    ScryfallResponseFormatException,
)


class ScryfallListResponseValidator:
    """Valide un payload brut de type liste avant mapping."""

    def validate(self, raw_response: Any) -> dict[str, Any]:
        """Valide la structure minimale attendue d'une liste Scryfall."""
        if not isinstance(raw_response, dict):
            raise ScryfallResponseFormatException(
                "Scryfall list response must be a dictionary.",
                response_detail=raw_response,
            )

        raw_object = raw_response.get("object")
        if raw_object != "list":
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'object' field.",
                response_detail=raw_response,
            )

        raw_data = raw_response.get("data")
        if not isinstance(raw_data, list):
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'data' field.",
                response_detail=raw_response,
            )

        raw_has_more = raw_response.get("has_more", False)
        if not isinstance(raw_has_more, bool):
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'has_more' field.",
                response_detail=raw_response,
            )

        raw_next_page = raw_response.get("next_page")
        if raw_next_page is not None and not isinstance(raw_next_page, str):
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'next_page' field.",
                response_detail=raw_response,
            )
        if raw_has_more and not raw_next_page:
            raise ScryfallPaginationException(
                "Scryfall list response is missing 'next_page' while 'has_more' is true.",
                response_detail=raw_response,
            )

        raw_total_cards = raw_response.get("total_cards")
        if raw_total_cards is not None and not isinstance(raw_total_cards, int):
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'total_cards' field.",
                response_detail=raw_response,
            )

        raw_warnings = raw_response.get("warnings")
        if raw_warnings is not None and not isinstance(raw_warnings, list):
            raise ScryfallResponseFormatException(
                "Scryfall list response has an invalid 'warnings' field.",
                response_detail=raw_response,
            )

        return raw_response
