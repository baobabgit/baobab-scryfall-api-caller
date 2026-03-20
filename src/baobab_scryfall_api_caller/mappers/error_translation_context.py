"""Contexte de traduction d'erreur vers une exception metier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorTranslationContext:
    """Contient les informations de diagnostic lors d'une traduction d'erreur."""

    message: str | None = None
    category: str | None = None
    http_status: int | None = None
    url: str | None = None
    params: Any | None = None
    payload: Any | None = None
    response_detail: Any | None = None
