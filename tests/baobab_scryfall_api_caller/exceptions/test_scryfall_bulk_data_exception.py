"""Tests de ScryfallBulkDataException."""

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallBulkDataException,
)


class TestScryfallBulkDataException:
    """Valide l'heritage de l'exception bulk data."""

    def test_inherits_from_root_exception(self) -> None:
        """L'exception bulk data doit heriter de la racine."""
        exception = ScryfallBulkDataException(
            "Bulk metadata invalid", payload={"type": "all_cards"}
        )
        assert isinstance(exception, BaobabScryfallApiCallerException)
        assert exception.payload == {"type": "all_cards"}
