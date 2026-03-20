"""Modele de face de carte Scryfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CardFace:
    """Represente une face de carte multi-face."""

    name: str
    mana_cost: str | None = None
    type_line: str | None = None
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
