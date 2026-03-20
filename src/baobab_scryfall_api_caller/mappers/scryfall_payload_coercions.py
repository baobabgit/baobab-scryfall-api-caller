"""Coercitions de champs communes pour les payloads Scryfall."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException


def as_optional_str(
    value: Any,
    *,
    invalid_message: str,
    response_detail: Any | None = None,
) -> str | None:
    """Convertit une valeur optionnelle en ``str`` ou leve une erreur de format."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    detail = value if response_detail is None else response_detail
    raise ScryfallResponseFormatException(
        invalid_message,
        response_detail=detail,
    )


def as_optional_int(
    value: Any,
    *,
    invalid_message: str,
    response_detail: Any | None = None,
) -> int | None:
    """Convertit une valeur optionnelle en ``int`` ou leve une erreur de format."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    detail = value if response_detail is None else response_detail
    raise ScryfallResponseFormatException(
        invalid_message,
        response_detail=detail,
    )


def as_int(
    value: Any,
    *,
    default: int,
    invalid_message: str,
    response_detail: Any | None = None,
) -> int:
    """Convertit une valeur en ``int`` avec defaut ou leve une erreur de format."""
    if value is None:
        return default
    if isinstance(value, int):
        return value
    detail = value if response_detail is None else response_detail
    raise ScryfallResponseFormatException(
        invalid_message,
        response_detail=detail,
    )


def as_bool(
    value: Any,
    *,
    default: bool,
    invalid_message: str,
    response_detail: Any | None = None,
) -> bool:
    """Convertit une valeur en ``bool`` avec defaut ou leve une erreur de format."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    detail = value if response_detail is None else response_detail
    raise ScryfallResponseFormatException(
        invalid_message,
        response_detail=detail,
    )
