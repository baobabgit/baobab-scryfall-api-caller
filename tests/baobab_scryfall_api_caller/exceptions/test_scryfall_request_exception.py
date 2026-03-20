"""Tests de ScryfallRequestException."""

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallRequestException,
)


class TestScryfallRequestException:
    """Valide l'heritage et le contrat de base."""

    def test_inherits_from_root_exception(self) -> None:
        """L'exception doit heriter de la racine projet."""
        exception = ScryfallRequestException("Transport error")
        assert isinstance(exception, BaobabScryfallApiCallerException)
