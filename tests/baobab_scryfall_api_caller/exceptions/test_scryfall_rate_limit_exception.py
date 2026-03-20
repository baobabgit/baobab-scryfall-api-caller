"""Tests de ScryfallRateLimitException."""

from baobab_scryfall_api_caller.exceptions import (
    ScryfallRateLimitException,
    ScryfallRequestException,
)


class TestScryfallRateLimitException:
    """Valide l'heritage rate limit."""

    def test_inherits_from_request_exception(self) -> None:
        """L'exception de rate-limit doit heriter de ScryfallRequestException."""
        exception = ScryfallRateLimitException("Too many requests", http_status=429)
        assert isinstance(exception, ScryfallRequestException)
        assert exception.http_status == 429
