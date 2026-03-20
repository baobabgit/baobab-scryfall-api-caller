"""Tests de ScryfallNotFoundException."""

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
)


class TestScryfallNotFoundException:
    """Valide l'heritage specifique de not-found."""

    def test_inherits_from_request_exception(self) -> None:
        """L'exception not-found doit heriter de ScryfallRequestException."""
        exception = ScryfallNotFoundException("Resource not found", http_status=404)
        assert isinstance(exception, ScryfallRequestException)
        assert exception.http_status == 404
