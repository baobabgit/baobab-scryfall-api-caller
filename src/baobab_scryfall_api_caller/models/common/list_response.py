"""Modele generique de reponse liste pour les endpoints Scryfall."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

from baobab_scryfall_api_caller.models.common.pagination_metadata import PaginationMetadata
from baobab_scryfall_api_caller.models.common.scryfall_warning import ScryfallWarning

T = TypeVar("T")


@dataclass(frozen=True)
class ListResponse(Generic[T]):
    """Represente une reponse liste typable reutilisable sur tous les services."""

    data: list[T]
    metadata: PaginationMetadata
    object_type: str = "list"

    @property
    def has_more(self) -> bool:
        """Expose `has_more` au niveau racine pour un acces simple."""
        return self.metadata.has_more

    @property
    def next_page(self) -> str | None:
        """Expose `next_page` au niveau racine pour un acces simple."""
        return self.metadata.next_page

    @property
    def items(self) -> list[T]:
        """Alias de :attr:`data` pour une lecture orientee « page d'elements »."""
        return self.data

    @property
    def is_empty(self) -> bool:
        """Vrai si la page courante ne contient aucun element."""
        return len(self.data) == 0

    @property
    def total_cards(self) -> int | None:
        """Nombre total d'elements annonce par Scryfall, si present dans la reponse."""
        return self.metadata.total_cards

    @property
    def warnings(self) -> tuple[ScryfallWarning, ...]:
        """Avertissements Scryfall associes a la reponse liste."""
        return self.metadata.warnings

    @property
    def count(self) -> int:
        """Nombre d'elements dans la page courante (equivalent a ``len(response)``)."""
        return len(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __bool__(self) -> bool:
        return len(self.data) > 0

    def __repr__(self) -> str:
        return (
            f"ListResponse(len={len(self.data)}, has_more={self.has_more!r}, "
            f"next_page={self.next_page!r}, object_type={self.object_type!r})"
        )
