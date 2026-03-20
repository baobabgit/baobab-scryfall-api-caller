"""Tests de PaginationMetadata."""

from baobab_scryfall_api_caller.exceptions import ScryfallPaginationException
from baobab_scryfall_api_caller.models.common import PaginationMetadata, ScryfallWarning


class TestPaginationMetadata:
    """Valide la coherence des metadonnees de pagination."""

    def test_nominal_metadata(self) -> None:
        """La construction nominale doit conserver les valeurs."""
        metadata = PaginationMetadata(
            has_more=True,
            next_page="https://api.scryfall.com/cards/search?page=2",
            total_cards=123,
            warnings=(ScryfallWarning(message="Warning"),),
        )
        assert metadata.has_more is True
        assert metadata.next_page is not None
        assert metadata.total_cards == 123
        assert len(metadata.warnings) == 1

    def test_has_more_false_without_next_page(self) -> None:
        """has_more=false sans next_page est valide."""
        metadata = PaginationMetadata(has_more=False, next_page=None)
        assert metadata.has_more is False
        assert metadata.next_page is None

    def test_has_more_true_without_next_page_raises(self) -> None:
        """has_more=true sans next_page doit lever une exception de pagination."""
        try:
            PaginationMetadata(has_more=True, next_page=None)
        except ScryfallPaginationException as exception:
            assert "has_more=true" in exception.message
        else:
            assert False, "Expected ScryfallPaginationException"
