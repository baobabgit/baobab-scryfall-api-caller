"""Resultat type pour l'autocompletion de noms de cartes Scryfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AutocompleteResult:
    """Suggestions de noms issues de `GET /cards/autocomplete`."""

    suggestions: tuple[str, ...]
    total_values: int | None = None
