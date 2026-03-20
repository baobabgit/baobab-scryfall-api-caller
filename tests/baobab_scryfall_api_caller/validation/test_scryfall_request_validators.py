"""Tests de ScryfallRequestValidators."""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)


class TestScryfallRequestValidators:
    """Valide les helpers de pagination et UUID."""

    def test_optional_page_params_none(self) -> None:
        """Sans page, aucun parametre de requete."""
        assert ScryfallRequestValidators.optional_page_params(page=None) is None

    def test_optional_page_params_valid(self) -> None:
        """Une page valide produit le dictionnaire attendu."""
        assert ScryfallRequestValidators.optional_page_params(page=2) == {"page": 2}

    def test_optional_page_params_rejects_non_positive(self) -> None:
        """Une page <= 0 doit etre rejetee."""
        try:
            ScryfallRequestValidators.optional_page_params(page=0)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_optional_page_params_rejects_wrong_type(self) -> None:
        """Un type de page non entier doit etre rejete."""
        try:
            ScryfallRequestValidators.optional_page_params(page="2")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_require_uuid_string(self) -> None:
        """Un UUID valide est canonise."""
        uid = "00000000-0000-4000-8000-000000000001"
        assert (
            ScryfallRequestValidators.require_uuid_string(
                value=uid.upper(),
                field_name="x",
            )
            == uid
        )

    def test_require_uuid_invalid(self) -> None:
        """Un UUID invalide doit lever."""
        try:
            ScryfallRequestValidators.require_uuid_string(value="bad", field_name="id")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"
