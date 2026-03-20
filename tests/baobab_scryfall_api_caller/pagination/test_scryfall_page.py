"""Tests de ScryfallPage."""

from baobab_scryfall_api_caller.models.common import ListResponse, PaginationMetadata
from baobab_scryfall_api_caller.pagination import ScryfallPage


class TestScryfallPage:
    """Valide la representation d'une page locale."""

    def test_page_properties(self) -> None:
        """Les proprietes de page doivent relayer la reponse."""
        page = ScryfallPage[str](
            response=ListResponse(
                data=["A", "B"],
                metadata=PaginationMetadata(
                    has_more=True,
                    next_page="https://api.scryfall.com/cards/search?page=2",
                ),
            )
        )
        assert page.items == ["A", "B"]
        assert page.has_more is True
        assert page.next_page == "https://api.scryfall.com/cards/search?page=2"

    def test_page_without_next(self) -> None:
        """Une page terminale doit exposer next_page a None."""
        page = ScryfallPage[int](
            response=ListResponse(
                data=[],
                metadata=PaginationMetadata(has_more=False),
            )
        )
        assert not page.items
        assert page.has_more is False
        assert page.next_page is None
