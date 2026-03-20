"""Tests de ScryfallPaginationException."""

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallPaginationException,
)


class TestScryfallPaginationException:
    """Valide l'heritage de l'exception de pagination."""

    def test_inherits_from_root_exception(self) -> None:
        """L'exception de pagination doit heriter de la racine."""
        exception = ScryfallPaginationException(
            "Invalid next page", response_detail={"next_page": None}
        )
        assert isinstance(exception, BaobabScryfallApiCallerException)
        assert exception.response_detail == {"next_page": None}
