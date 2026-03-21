"""Modele de catalogue Scryfall (liste de valeurs textuelles)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Catalog:
    """Represente un catalogue Scryfall normalise.

    :ivar catalog_key: Identifiant logique du catalogue (segment d'URL normalise).
    :ivar uri: URI canonique du catalogue renvoyee par Scryfall.
    :ivar total_values: Nombre total de valeurs annonce par Scryfall.
    :ivar values: Valeurs textuelles du catalogue (ordre conserve).
    """

    catalog_key: str
    uri: str
    total_values: int
    values: tuple[str, ...]
