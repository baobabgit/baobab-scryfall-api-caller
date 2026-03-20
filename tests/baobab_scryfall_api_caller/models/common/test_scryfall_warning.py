"""Tests de ScryfallWarning."""

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.common import ScryfallWarning


class TestScryfallWarning:
    """Valide la construction de warnings."""

    def test_from_raw_string(self) -> None:
        """Un warning brut str doit etre accepte."""
        warning = ScryfallWarning.from_raw("Use with care")
        assert warning.message == "Use with care"

    def test_from_raw_dict(self) -> None:
        """Un warning brut dict avec details doit etre accepte."""
        warning = ScryfallWarning.from_raw({"details": "Soft warning"})
        assert warning.message == "Soft warning"

    def test_from_raw_invalid_raises(self) -> None:
        """Un warning non supporte doit lever une exception metier."""
        try:
            ScryfallWarning.from_raw(42)
        except ScryfallResponseFormatException as exception:
            assert "Invalid warning format" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"
