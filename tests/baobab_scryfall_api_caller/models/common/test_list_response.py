"""Tests de ListResponse."""

from baobab_scryfall_api_caller.models.common import ListResponse, PaginationMetadata


class TestListResponse:
    """Valide le modele generique de reponse liste."""

    def test_list_response_nominal(self) -> None:
        """La construction nominale doit exposer les proprietes attendues."""
        response = ListResponse[str](
            data=["a", "b"],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="https://api.scryfall.com/cards/search?page=2",
            ),
        )
        assert response.data == ["a", "b"]
        assert response.has_more is True
        assert response.next_page == "https://api.scryfall.com/cards/search?page=2"

    def test_empty_list_response(self) -> None:
        """Une liste vide doit etre prise en charge proprement."""
        response = ListResponse[int](
            data=[],
            metadata=PaginationMetadata(has_more=False),
        )
        assert not response.data
        assert response.has_more is False
        assert response.next_page is None
