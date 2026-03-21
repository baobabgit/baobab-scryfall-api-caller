"""Tests de ListResponse."""

from baobab_scryfall_api_caller.models.common import ListResponse, PaginationMetadata
from baobab_scryfall_api_caller.models.common.scryfall_warning import ScryfallWarning


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
        assert response.items is response.data
        assert response.has_more is True
        assert response.next_page == "https://api.scryfall.com/cards/search?page=2"
        assert response.count == 2
        assert len(response) == 2
        assert list(response) == ["a", "b"]
        assert response
        assert not response.is_empty
        assert "len=2" in repr(response)

    def test_empty_list_response(self) -> None:
        """Une liste vide doit etre prise en charge proprement."""
        response = ListResponse[int](
            data=[],
            metadata=PaginationMetadata(has_more=False),
        )
        assert not response.data
        assert response.has_more is False
        assert response.next_page is None
        assert response.is_empty
        assert not response
        assert response.count == 0

    def test_metadata_shortcuts(self) -> None:
        """Raccourcis vers total_cards et warnings."""
        warn = ScryfallWarning(message="m")
        response = ListResponse[str](
            data=["x"],
            metadata=PaginationMetadata(
                has_more=False,
                total_cards=100,
                warnings=(warn,),
            ),
        )
        assert response.total_cards == 100
        assert response.warnings == (warn,)

    def test_empty_data_but_has_more_true_is_truthy_if_items_exist(self) -> None:
        """bool reflete la presence d'elements dans la page courante."""
        response = ListResponse[str](
            data=[],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="https://api.scryfall.com/x",
            ),
        )
        assert not bool(response)
