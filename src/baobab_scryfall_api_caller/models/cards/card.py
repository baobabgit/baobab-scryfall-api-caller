"""Modele principal de carte Scryfall."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_scryfall_api_caller.models.cards.card_face import CardFace
from baobab_scryfall_api_caller.models.cards.image_uris import ImageUris


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
    type_line: str | None = None
    oracle_text: str | None = None
    rarity: str | None = None
    cmc: float | None = None
    colors: tuple[str, ...] = ()
    color_identity: tuple[str, ...] = ()
    lang: str | None = None
    artist: str | None = None
    flavor_text: str | None = None
    image_uris: ImageUris | None = None
    reserved: bool = False
    foil: bool = False
    nonfoil: bool = False
    digital: bool = False
    games: tuple[str, ...] = ()
    legalities: tuple[tuple[str, str], ...] = ()
