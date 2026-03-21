"""URLs d'illustration Scryfall (formats et recadrages)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageUris:
    """Liens vers les rendus image d'une carte ou d'une face.

    Tous les champs sont optionnels : Scryfall ne fournit pas systematiquement
    chaque variante selon le layout ou la disponibilite.
    """

    small: str | None = None
    normal: str | None = None
    large: str | None = None
    png: str | None = None
    art_crop: str | None = None
    border_crop: str | None = None
