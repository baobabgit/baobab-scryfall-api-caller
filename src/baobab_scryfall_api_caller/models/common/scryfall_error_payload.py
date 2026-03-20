"""Structure minimale reutilisable d'une erreur distante Scryfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException


@dataclass(frozen=True)
class ScryfallErrorPayload:
    """Represente une charge d'erreur retournee par Scryfall."""

    status: int | None
    code: str | None
    details: str

    @classmethod
    def from_dict(cls, raw_error: Any) -> "ScryfallErrorPayload":
        """Mappe un objet dictionnaire vers le modele d'erreur."""
        if not isinstance(raw_error, dict):
            raise ScryfallResponseFormatException(
                "Remote error payload must be a dictionary.",
                response_detail=raw_error,
            )

        details = raw_error.get("details")
        if not isinstance(details, str):
            raise ScryfallResponseFormatException(
                "Remote error payload is missing a string 'details' field.",
                response_detail=raw_error,
            )

        status = raw_error.get("status")
        code = raw_error.get("code")
        if status is not None and not isinstance(status, int):
            raise ScryfallResponseFormatException(
                "Remote error payload has an invalid 'status' field.",
                response_detail=raw_error,
            )
        if code is not None and not isinstance(code, str):
            raise ScryfallResponseFormatException(
                "Remote error payload has an invalid 'code' field.",
                response_detail=raw_error,
            )

        return cls(status=status, code=code, details=details)
