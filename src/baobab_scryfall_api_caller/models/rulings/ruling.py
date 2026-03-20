"""Modele d'oracle ruling Scryfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ruling:
    """Represente un ruling Oracle associe a une carte.

    :ivar oracle_id: Identifiant Oracle auquel se rapporte le ruling.
    :ivar source: Source du texte (ex. ``wotc``).
    :ivar published_at: Date de publication au format ISO (date).
    :ivar comment: Texte integral du ruling.
    """

    oracle_id: str
    source: str
    published_at: str
    comment: str
