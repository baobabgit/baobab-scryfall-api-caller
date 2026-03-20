"""Metadonnees de pagination pour les reponses de liste Scryfall."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_scryfall_api_caller.exceptions import ScryfallPaginationException
from baobab_scryfall_api_caller.models.common.scryfall_warning import ScryfallWarning


@dataclass(frozen=True)
class PaginationMetadata:
    """Porte les informations de pagination d'une reponse Scryfall."""

    has_more: bool
    next_page: str | None = None
    total_cards: int | None = None
    warnings: tuple[ScryfallWarning, ...] = ()

    def __post_init__(self) -> None:
        """Valide la coherence interne des metadonnees."""
        if self.has_more and not self.next_page:
            raise ScryfallPaginationException(
                "List response indicates has_more=true but no next_page was provided.",
                response_detail={"has_more": self.has_more, "next_page": self.next_page},
            )
