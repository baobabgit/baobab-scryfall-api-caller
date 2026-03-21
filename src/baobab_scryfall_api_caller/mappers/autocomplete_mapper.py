"""Mapper de reponse autocomplete Scryfall vers modele metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.cards.autocomplete_result import AutocompleteResult


class AutocompleteMapper:
    """Mappe une reponse catalogue brute (autocomplete) vers `AutocompleteResult`."""

    def map_autocomplete(self, raw_payload: Any) -> AutocompleteResult:
        """Transforme un payload Scryfall ``catalog`` en resultat d'autocomplete."""
        if not isinstance(raw_payload, dict):
            raise ScryfallResponseFormatException(
                "Autocomplete payload must be a dictionary.",
                response_detail=raw_payload,
            )

        if raw_payload.get("object") != "catalog":
            raise ScryfallResponseFormatException(
                "Autocomplete payload has an invalid 'object' field.",
                response_detail=raw_payload,
            )

        raw_data = raw_payload.get("data")
        if not isinstance(raw_data, list):
            raise ScryfallResponseFormatException(
                "Autocomplete payload has an invalid 'data' field.",
                response_detail=raw_payload,
            )

        suggestions: list[str] = []
        for index, item in enumerate(raw_data):
            if not isinstance(item, str):
                raise ScryfallResponseFormatException(
                    f"Autocomplete payload has a non-string value at index {index}.",
                    response_detail=raw_payload,
                )
            suggestions.append(item)

        total_values: int | None = None
        raw_total = raw_payload.get("total_values")
        if raw_total is not None:
            if not isinstance(raw_total, int) or raw_total < 0:
                raise ScryfallResponseFormatException(
                    "Autocomplete payload has an invalid 'total_values' field.",
                    response_detail=raw_payload,
                )
            total_values = raw_total

        return AutocompleteResult(
            suggestions=tuple(suggestions),
            total_values=total_values,
        )
