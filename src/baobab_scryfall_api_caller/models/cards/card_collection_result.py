"""Resultat type pour POST /cards/collection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from baobab_scryfall_api_caller.models.cards.card import Card


@dataclass(frozen=True)
class CardCollectionResult:
    """Cartes resolues et identifiants non trouves retournes par Scryfall."""

    cards: tuple[Card, ...]
    not_found: tuple[dict[str, Any], ...]
