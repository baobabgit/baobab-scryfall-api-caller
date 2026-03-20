"""Tests de ScryfallResponseFormatException."""

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallResponseFormatException,
)


class TestScryfallResponseFormatException:
    """Valide l'heritage de l'exception de format."""

    def test_inherits_from_root_exception(self) -> None:
        """L'exception de format doit heriter de la racine."""
        exception = ScryfallResponseFormatException(
            "Unexpected response", response_detail={"foo": "bar"}
        )
        assert isinstance(exception, BaobabScryfallApiCallerException)
        assert exception.response_detail == {"foo": "bar"}
