"""Representation d'une page locale de resultats Scryfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from baobab_scryfall_api_caller.models.common.list_response import ListResponse

T = TypeVar("T")


@dataclass(frozen=True)
class ScryfallPage(Generic[T]):
    """Represente une page parsee, sans iteration reseau automatique."""

    response: ListResponse[T]

    @property
    def items(self) -> list[T]:
        """Retourne les elements de la page courante."""
        return self.response.data

    @property
    def has_more(self) -> bool:
        """Retourne si une page suivante existe."""
        return self.response.has_more

    @property
    def next_page(self) -> str | None:
        """Retourne l'URL de page suivante si disponible."""
        return self.response.next_page
