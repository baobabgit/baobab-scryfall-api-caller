"""Modele de warning retourne par certaines reponses Scryfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException


@dataclass(frozen=True)
class ScryfallWarning:
    """Represente un avertissement de reponse Scryfall.

    :param message: Message textuel de warning.
    :type message: str
    """

    message: str

    @classmethod
    def from_raw(cls, raw_warning: Any) -> "ScryfallWarning":
        """Construit un warning depuis une structure brute."""
        if isinstance(raw_warning, str):
            return cls(message=raw_warning)
        if isinstance(raw_warning, dict):
            details = raw_warning.get("details")
            if isinstance(details, str):
                return cls(message=details)

        raise ScryfallResponseFormatException(
            "Invalid warning format in Scryfall list response.",
            response_detail=raw_warning,
        )
