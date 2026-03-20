"""Modele principal de carte Scryfall."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_scryfall_api_caller.models.cards.card_face import CardFace


@dataclass(frozen=True)
class Card:  # pylint: disable=too-many-instance-attributes
    """Represente une carte Scryfall mappee en objet metier."""

    id: str
    name: str
    layout: str | None = None
    oracle_id: str | None = None
    mtgo_id: int | None = None
    cardmarket_id: int | None = None
    set_code: str | None = None
    collector_number: str | None = None
    faces: tuple[CardFace, ...] = ()
