"""Tests de ScryfallErrorPayload."""

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.common import ScryfallErrorPayload


class TestScryfallErrorPayload:
    """Valide le mapping des erreurs distantes Scryfall."""

    def test_from_dict_nominal(self) -> None:
        """Le mapping nominal doit conserver les champs principaux."""
        payload = ScryfallErrorPayload.from_dict(
            {
                "status": 404,
                "code": "not_found",
                "details": "Card not found",
            }
        )
        assert payload.status == 404
        assert payload.code == "not_found"
        assert payload.details == "Card not found"

    def test_from_dict_missing_details_raises(self) -> None:
        """L'absence de details doit lever une erreur de format."""
        try:
            ScryfallErrorPayload.from_dict({"status": 500})
        except ScryfallResponseFormatException as exception:
            assert "details" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_from_dict_invalid_type_raises(self) -> None:
        """Une charge non dictionnaire doit etre rejetee."""
        try:
            ScryfallErrorPayload.from_dict("error")
        except ScryfallResponseFormatException as exception:
            assert "dictionary" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"
