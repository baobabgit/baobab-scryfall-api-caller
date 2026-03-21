"""Modele de face de carte Scryfall."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_scryfall_api_caller.models.cards.image_uris import ImageUris


@dataclass(frozen=True)
class CardFace:  # pylint: disable=too-many-instance-attributes
    """Represente une face de carte multi-face."""

    name: str
    mana_cost: str | None = None
    type_line: str | None = None
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
    loyalty: str | None = None
    defense: str | None = None
    flavor_text: str | None = None
    artist: str | None = None
    illustration_id: str | None = None
    image_uris: ImageUris | None = None
