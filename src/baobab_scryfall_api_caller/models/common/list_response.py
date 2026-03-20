"""Modele generique de reponse liste pour les endpoints Scryfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from baobab_scryfall_api_caller.models.common.pagination_metadata import PaginationMetadata

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
