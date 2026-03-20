"""Tests de ScryfallValidationException."""

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallValidationException,
)


class TestScryfallValidationException:
    """Valide l'heritage et les metadonnees de validation."""

    def test_inherits_from_root_exception(self) -> None:
        """L'exception de validation doit heriter de la racine."""
        exception = ScryfallValidationException("Invalid input", params={"q": ""})
        assert isinstance(exception, BaobabScryfallApiCallerException)
        assert exception.params == {"q": ""}
